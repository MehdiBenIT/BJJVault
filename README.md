# BJJVault

Phase 1 of the BJJ Platform roadmap (see [ROADMAP.md](ROADMAP.md)): auth, athlete profile, training journal, competition journal — built for real on Azure, cost-minimized.

## Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | React + Vite, hosted on **Azure Static Web Apps (Free tier)** | Genuinely free static hosting, no need to burn AKS capacity on the frontend |
| API Gateway | **APIM Consumption tier** | Pay-per-call, no fixed monthly cost, first 1M calls/month free |
| Backend | FastAPI in Docker, on **AKS** (1x Standard_B2s node, Free control-plane tier) | Matches the AZ-305 learning goal; stop the cluster when idle to cut compute cost to ~zero |
| Database | **Azure SQL free tier** (serverless Gen5, `useFreeLimit`) | 100,000 vCore-seconds + 32GB storage/month, free forever, one per subscription |
| Images | Azure Container Registry (Basic) | Cheapest ACR tier |
| Observability | Application Insights + Log Analytics | Free up to 5GB ingestion/month |
| IaC | Bicep | Native, no extra tooling |
| CI/CD | GitHub Actions (OIDC login, no stored client secret) | |

## Cost reality check

Nothing here is 100% free except the Static Web App and the SQL free-tier database. The real ongoing costs:

- **AKS node (Standard_B2s)**: ~15-20€/month if left running 24/7. **Stop it when you're not using it** — `az aks stop --resource-group bjjvault-dev-rg --name bjjvault-dev-aks` stops the VMs (no compute charge while stopped, you still pay a few cents/month for the OS disk). `az aks start` brings it back in ~2-3 minutes.
- **Standard Load Balancer** (created by the `backend-deployment.yaml` Kubernetes `Service` of type `LoadBalancer`): ~15-18€/month if left running. Stopping the AKS cluster does not delete this — if you want it fully gone between sessions, `kubectl delete -f k8s/backend-deployment.yaml` before stopping, and re-apply on your next session.
- **APIM Consumption**: ~0€ at hobby-project call volumes.
- A `Microsoft.Consumption/budgets` alert (`infra/modules/budget.bicep`) is included — deploy it once so you get emailed at 50%/90%/100% of a monthly cap instead of finding out later.

If you want this to cost literally nothing between work sessions: stop AKS and delete the LoadBalancer service when you're done for the day, redeploy when you pick it back up. The GitHub Actions `deploy` workflow already does `az aks start` automatically on every deploy.

## Local development

Backend:

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Frontend expects the API at `http://localhost:8000` by default (override with `VITE_API_BASE_URL`).

## Google / Apple OAuth setup

- **Google**: create an OAuth 2.0 Client ID (Web application) in Google Cloud Console. Authorized redirect URI: `<OAUTH_REDIRECT_BASE_URL>/auth/google/callback`. Set `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`.
- **Apple**: create a Services ID + Sign in with Apple key in the Apple Developer portal. The frontend needs Apple's JS SDK to obtain an `identity_token`, which is then POSTed to `/auth/apple/login` (backend endpoint already implemented; frontend button not wired up yet — see Phase 1 follow-ups below).

## Deploying to Azure

One-time, per environment:

1. `az login`
2. Fill in `infra/main.parameters.dev.json` (or pass `sqlAdminPassword` / `apimPublisherEmail` as CLI overrides — don't commit real secrets).
3. Set up GitHub Actions OIDC federated credentials for a service principal scoped to your subscription (or resource group), and add these repo secrets:
   - `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`
   - `SQL_ADMIN_PASSWORD`, `APIM_PUBLISHER_EMAIL`
   - `AZURE_STATIC_WEB_APPS_API_TOKEN` (from the Static Web App resource once created — first deploy will need this added after `infra` job creates it)
   - `APIM_GATEWAY_URL` (from the `infra` job's output, once known)
4. Push to `main` or run the `deploy` workflow manually.

Manual first-time deploy (if you'd rather not wire up GitHub Actions yet):

```bash
az group create --name bjjvault-dev-rg --location westeurope
az deployment group create \
  --resource-group bjjvault-dev-rg \
  --template-file infra/main.bicep \
  --parameters infra/main.parameters.dev.json \
  --parameters sqlAdminPassword='<your-password>' apimPublisherEmail='<your-email>'
```

Then build/push the backend image and apply the K8s manifests:

```bash
az acr build --registry <acrLoginServer-from-output> --image bjjvault-backend:latest backend
az aks get-credentials --resource-group bjjvault-dev-rg --name bjjvault-dev-aks
cp k8s/backend-secret.example.yaml k8s/backend-secret.yaml   # fill in real values
kubectl apply -f k8s/backend-secret.yaml
ACR_LOGIN_SERVER=<acrLoginServer> IMAGE_TAG=latest envsubst < k8s/backend-deployment.yaml | kubectl apply -f -
```

Once the `LoadBalancer` Service has a public IP (`kubectl get svc bjjvault-backend`), update the APIM API's `serviceUrl` to point at it (either redeploy `main.bicep` with `backendUrl` set, or edit it in the Azure Portal).

Set up the monthly budget alert once:

```bash
az deployment sub create \
  --location westeurope \
  --template-file infra/modules/budget.bicep \
  --parameters namePrefix=bjjvault-dev alertEmail='<your-email>'
```

## Phase 1 follow-ups (not yet done)

- Apple Sign In button on the frontend (backend endpoint is ready, needs Apple JS SDK wiring)
- Alembic migrations (models currently rely on `Base.metadata.create_all` at startup, fine for Phase 1, not for schema changes later)
- Real ingress / TLS in front of the AKS LoadBalancer instead of a bare public IP
