# BJJVault — Azure Cost Estimate by Phase

Pay-as-you-go, East US / West Europe, USD/month. Based on `ROADMAP.md` phases and SKUs already chosen in `infra/modules/*.bicep`. Ranges wide where cost is usage-driven (AI tokens, video bandwidth), not fixed by SKU.

| Phase | New Azure spend | Monthly est. | Note |
|---|---|---|---|
| 1 Foundation | AKS 1×B2s node + disk, ACR Basic, APIM Consumption, SQL free tier, Static Web App free, App Insights free | **$8–40** | Low end = stop/start node (few hrs/day). High end = node 24/7 (~730hr × $0.043 ≈ $31 + ACR $5 + disk $2). `budget.bicep` cap is $20 — fine if cluster stopped, tight if 24/7. |
| 2 Match Vault | Blob Storage (hot, tens of GB), Event Grid, Functions Consumption | **+$2–5** | Functions/Event Grid free grants cover low volume. Blob cost scales with video GB stored. |
| 3 AI Fight Journal | AI Search (free tier possible, else Basic $75), Azure OpenAI tokens | **+$5–95** | Biggest swing item. Free AI Search tier (50MB/3 idx) may suffice early. OpenAI billed per token — depends entirely on query volume/model. |
| 4 OpenMat Finder | Redis Basic C0 (no free tier, ~$16), Azure Maps (free tier ~5k tx/mo) | **+$16–20** | Redis is the fixed cost here — no free SKU exists. |
| 5 OpenMat Booking | DB growth only, Stripe fees separate (not Azure) | **+$0–5** | May start pushing past SQL free 32GB/100k vCore-sec limit. |
| 6 Seminar Marketplace | Same, Stripe handles payments | **+$0–5** | |
| 7 Gym Portal | **Inflection point**: real traffic outgrows 1-node AKS + free SQL | **+$60–250** | Likely need 2–3 nodes, SQL off free tier (serverless billing kicks in). Cost-minimized architecture stops applying here. |
| 8 Coach Portal | Booking logic, minor storage | **+$5–20** | |
| 9 Video Marketplace | More Blob storage + egress (first 100GB/mo free, then ~$0.087/GB), maybe encoding compute | **+$50–500** | Depends on content volume/viewers — need real traffic numbers to tighten. |
| 10 Streaming Platform | CDN/Front Door + heavy egress, adaptive bitrate transcoding | **+$200–2000+** | Netflix-of-BJJ cost profile — no honest number without a traffic model (concurrent viewers × avg bitrate × hours). |
| 11 Competition Ecosystem | Mostly API/DB work, external integrations | **+$5–20** | Light infra add. |
| 12 Multi-Tenant SaaS | App Gateway v2 + WAF (~$125–250 baseline), Private Endpoints (~$7.30 each), elastic pool SQL, hub-spoke VNet | **+$300–800 baseline** | Grows with tenant count — platform overhead floor, not ceiling. |

Cumulative: Phase 1-6 stays near $20/month budget if disciplined (stop cluster, free tiers). Phase 7+ blows past $20/month by design — real users/video/AI need real spend.

---

## Free-tier maximization checklist (Phase 1-6)

Goal: stay near $0-20/month as long as possible.

- **AKS**: `az aks stop` when not actively developing/testing. Node billed hourly only while running — biggest lever you have. Control plane (Free tier) always $0.
- **Azure SQL**: stay under free-tier caps — 100K vCore-seconds/month + 32GB storage. `autoPauseDelay` already set to 60min in `sql.bicep` — DB auto-pauses when idle, resumes on connect. Watch query volume; sustained load burns vCore-seconds fast.
- **ACR**: Basic tier is flat $5/month regardless of use — no free tier exists for ACR. Only lever: delete unused image tags to stay under 10GB included storage (avoid overage).
- **APIM Consumption**: free for first 1M calls/month, then ~$3.50/million. Stays $0 at personal-project volume.
- **Static Web App**: Free tier is genuinely free — no action needed, just don't add custom domains/features that need Standard tier.
- **App Insights**: free up to 5GB ingestion/month. AKS Container Insights (omsagent) can eat into this — consider disabling verbose logging or sampling if approaching cap.
- **Blob Storage (Phase 2)**: Hot tier ~$0.018/GB/month — cheap at low volume. Move stale/old match videos to Cool tier (~$0.01/GB) if rarely accessed.
- **Azure Functions / Event Grid (Phase 2)**: Consumption plan grants (1M executions + 400K GB-s Functions, 100K ops Event Grid) cover this phase's expected volume — stays $0.
- **Azure AI Search (Phase 3)**: use Free tier (50MB, 3 indexes, shared) as long as it fits — only upgrade to Basic ($75/mo) when you actually hit the index size/count limit, not preemptively.
- **Azure OpenAI (Phase 3)**: no free tier — pick smallest capable model (mini/nano variants), cap max tokens per request, cache repeated queries. This is the first genuinely unavoidable variable cost.
- **Budget alerts**: `budget.bicep` already wired to email at 50%/90%/forecasted 100% of the cap. Bump `budgetAmount` param when you deliberately cross a phase boundary (e.g. Phase 4 adding Redis) so alerts stay meaningful instead of constantly firing.

## Where free tier runs out

Redis (Phase 4) and Azure OpenAI (Phase 3) have **no free SKU** — first real fixed/variable costs regardless of discipline. Phase 7 is the real ceiling: single AKS node + free SQL cannot carry real user traffic, and that's a scale problem, not a tier problem.
