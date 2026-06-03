# Productionization: GCP Cloud Run & Google Batch

Convert a working Python scraper into a production-ready service deployed on GCP.

## Activation Triggers

Load this workflow when user requests:
- "Productionize this scraper"
- "Deploy to Cloud Run"
- "Run on Google Batch"
- "Containerize the scraper"
- "Schedule the scraper"

---

## Development vs Production

**During development**, `proxy-mcp` provides reconnaissance and traffic analysis:
- MITM traffic interception for API discovery
- Stealth browser for protected sites
- Session recording for replay

**For production**, use Python + `httpx` / `playwright-python` / `crawlee-python`
packaged in a Docker container and deployed to:
- **Cloud Run** — HTTP-triggered or scheduled runs (one-off, low ops overhead)
- **Google Batch** — parallel jobs, large-scale multi-account runs, GCS output

---

## Step 1: Choose Deployment Target

| Criteria | Cloud Run | Google Batch |
|----------|-----------|--------------|
| Trigger type | HTTP request / Cloud Scheduler | API / Pub/Sub / DAG |
| Parallelism | Auto-scaling instances | Explicit job/task array |
| Memory/CPU control | Moderate (up to 32 GB / 8 vCPU) | High (custom machine type) |
| Playwright support | Yes (use Chromium in image) | Yes |
| GCS output | Mount via FUSE or stream | Mount as volume |
| Best for | Lightweight scrapers, cron jobs | Multi-account batch runs |

---

## Step 2: Project Structure

```
my-scraper/
├── src/
│   └── my_scraper/
│       ├── __init__.py
│       ├── __main__.py        ← Click CLI entry point
│       ├── scraper.py
│       └── config.py
├── config/
│   └── config.yaml
├── Dockerfile.production
├── cloudbuild.yaml
├── pyproject.toml             ← Poetry or setup.cfg
└── tests/
```

---

## Step 3: Dockerfile

```dockerfile
FROM python:3.11-slim

# Install system deps for Playwright/Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget gnupg ca-certificates fonts-liberation \
    libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 \
    libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry==1.8.3
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --only main

# Install Playwright Chromium browser
RUN poetry run playwright install chromium --with-deps

COPY . .
RUN poetry install --only main

ENTRYPOINT ["poetry", "run", "python", "-m", "my_scraper"]
```

---

## Step 4: Cloud Run Deployment

### Trigger via HTTP (single run)

```python
# src/my_scraper/__main__.py
import click
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.post("/scrape")
async def scrape(keywords: list[str]):
    results = await run_scraper(keywords)
    return {"count": len(results)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

### Cloud Scheduler + Cloud Run (cron)

```yaml
# cloud_scheduler_job.yaml
name: daily-scrape
schedule: "0 2 * * *"   # 02:00 daily
timeZone: Asia/Jakarta
httpTarget:
  uri: https://my-scraper-xxxx-uc.a.run.app/scrape
  httpMethod: POST
  body: '{"keywords": ["keyword1", "keyword2"]}'
  headers:
    Content-Type: application/json
  oidcToken:
    serviceAccountEmail: scraper-sa@project.iam.gserviceaccount.com
```

### Deploy

```bash
# Build and push image
gcloud builds submit --config cloudbuild.yaml

# Deploy to Cloud Run
gcloud run deploy my-scraper \
    --image asia-southeast2-docker.pkg.dev/PROJECT/repo/my-scraper:latest \
    --region asia-southeast2 \
    --memory 2Gi \
    --cpu 2 \
    --timeout 3600 \
    --no-allow-unauthenticated \
    --set-env-vars SCRAPER_OUTPUT_DIR=/app/data/output
```

---

## Step 5: Google Batch Deployment

Best for multi-account or large-scale parallel runs.

### Job spec (Python client)

```python
from google.cloud import batch_v1

def create_scrape_job(
    project: str,
    region: str,
    image: str,
    keywords: list[str],
    account_id: str,
) -> batch_v1.Job:
    client = batch_v1.BatchServiceClient()

    job = batch_v1.Job()
    job.task_groups = [
        batch_v1.TaskGroup(
            task_count=1,
            task_spec=batch_v1.TaskSpec(
                runnables=[
                    batch_v1.Runnable(
                        container=batch_v1.Runnable.Container(
                            image_uri=image,
                            commands=["-k", ",".join(keywords)],
                            options="--init",
                        )
                    )
                ],
                environment=batch_v1.Environment(
                    secret_variables={
                        "SCRAPER_LOGIN": f"projects/{project}/secrets/scraper-login/versions/latest",
                        "SCRAPER_PASSWORD": f"projects/{project}/secrets/scraper-password-{account_id}/versions/latest",
                    }
                ),
                max_retry_count=2,
                max_run_duration="7200s",
            ),
        )
    ]

    # Mount GCS bucket for output
    job.task_groups[0].task_spec.volumes = [
        batch_v1.Volume(
            gcs=batch_v1.GCS(remote_path=f"my-bucket/output/{account_id}"),
            mount_path="/app/data/output",
        )
    ]

    job.allocation_policy = batch_v1.AllocationPolicy(
        instances=[
            batch_v1.AllocationPolicy.InstancePolicyOrTemplate(
                policy=batch_v1.AllocationPolicy.InstancePolicy(
                    machine_type="e2-standard-2",
                )
            )
        ]
    )

    return client.create_job(
        parent=f"projects/{project}/locations/{region}",
        job=job,
        job_id=f"scrape-{account_id}-{int(time.time())}",
    )
```

---

## Step 6: cloudbuild.yaml

```yaml
steps:
  - name: gcr.io/cloud-builders/docker
    args:
      - build
      - -f
      - Dockerfile.production
      - -t
      - asia-southeast2-docker.pkg.dev/$PROJECT_ID/repo/my-scraper:$COMMIT_SHA
      - -t
      - asia-southeast2-docker.pkg.dev/$PROJECT_ID/repo/my-scraper:latest
      - .

  - name: gcr.io/cloud-builders/docker
    args:
      - push
      - --all-tags
      - asia-southeast2-docker.pkg.dev/$PROJECT_ID/repo/my-scraper

images:
  - asia-southeast2-docker.pkg.dev/$PROJECT_ID/repo/my-scraper:$COMMIT_SHA
  - asia-southeast2-docker.pkg.dev/$PROJECT_ID/repo/my-scraper:latest
```

---

## Step 7: Local Testing

```bash
# Run locally via Poetry
poetry run python -m my_scraper -k "keyword1,keyword2"

# Run via Docker (mirrors production)
docker build -f Dockerfile.production -t my-scraper:dev .
docker run --rm \
    -e SCRAPER_LOGIN="user@example.com" \
    -e SCRAPER_PASSWORD="secret" \
    -v $(pwd)/data:/app/data/output \
    my-scraper:dev -k "keyword1"
```

---

## Quick Reference

| Task | Command / File |
|------|----------------|
| Build image | `gcloud builds submit --config cloudbuild.yaml` |
| Deploy Cloud Run | `gcloud run deploy my-scraper …` |
| Submit Batch job | `batch_v1.BatchServiceClient().create_job(…)` |
| Schedule via cron | Cloud Scheduler → Cloud Run HTTP endpoint |
| Secrets | GCP Secret Manager `secretVariables` in Batch spec |
| Output storage | GCS volume mount at `/app/data/output` |
| Local Docker test | `docker run --rm -e … my-scraper:dev` |

---

Back to main workflow: `../SKILL.md`
