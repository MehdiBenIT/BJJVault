import { googleLoginUrl } from "../api/client";

export default function Login() {
  return (
    <div className="page login-page">
      <h1>BJJVault</h1>
      <p>Your training and competition journal.</p>
      <a className="btn google-btn" href={googleLoginUrl()}>
        Continue with Google
      </a>
    </div>
  );
}
