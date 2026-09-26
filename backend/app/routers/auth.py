from authlib.integrations.starlette_client import OAuth
from authlib.jose import JsonWebKey, jwt as jose_jwt
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.user import TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

APPLE_KEYS_URL = "https://appleid.apple.com/auth/keys"


def get_or_create_user(db: Session, provider: str, subject: str, email: str, display_name: str) -> User:
    user = db.query(User).filter(User.oauth_provider == provider, User.oauth_subject == subject).first()
    if user:
        return user

    user = db.query(User).filter(User.email == email).first()
    if user:
        return user

    user = User(
        email=email,
        display_name=display_name or email.split("@")[0],
        oauth_provider=provider,
        oauth_subject=subject,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = f"{settings.oauth_redirect_base_url}/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    userinfo = token.get("userinfo")
    if not userinfo or not userinfo.get("email"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Google account has no email")

    user = get_or_create_user(
        db,
        provider="google",
        subject=userinfo["sub"],
        email=userinfo["email"],
        display_name=userinfo.get("name", ""),
    )
    access_token = create_access_token(subject=user.id)
    return RedirectResponse(f"{settings.frontend_base_url}/auth/callback?token={access_token}")


class AppleLoginRequest(BaseModel):
    identity_token: str
    display_name: str | None = None


@router.post("/apple/login", response_model=TokenResponse)
async def apple_login(payload: AppleLoginRequest, db: Session = Depends(get_db)):
    import httpx

    async with httpx.AsyncClient() as client:
        keys_response = await client.get(APPLE_KEYS_URL)
    jwk_set = JsonWebKey.import_key_set(keys_response.json())

    try:
        claims = jose_jwt.decode(payload.identity_token, jwk_set)
        claims.validate()
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Apple identity token") from exc

    if claims.get("aud") != settings.apple_client_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token audience mismatch")

    email = claims.get("email")
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Apple account has no email")

    user = get_or_create_user(
        db,
        provider="apple",
        subject=claims["sub"],
        email=email,
        display_name=payload.display_name or "",
    )
    access_token = create_access_token(subject=user.id)
    return TokenResponse(access_token=access_token, user=user)
