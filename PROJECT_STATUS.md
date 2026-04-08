# Project Status & Execution Guide

## What This Project Is

An **anonymous crime tip-off platform** with AI anomaly detection.
Users upload images or videos → AI classifies the crime type → generates an incident report.

---

## What Has Been Done

### 1. Documentation
- `CLAUDE.md` — full codebase guide for AI assistants
- `README.md` — architecture diagram, API reference, setup instructions

### 2. Infrastructure
- `.gitignore` — excludes secrets, node_modules, cache files
- `requirements.txt` — all Python dependencies pinned
- `.env.example` — template for secrets (copy to `.env` to use)
- `docker-compose.yml` — runs the entire stack with one command

### 3. Backend (FastAPI — `backend/`)
- **ML inference** — loads DenseNet121 model, classifies images into 14 crime types
- **Grad-CAM** — generates heatmaps showing which image regions triggered the AI
- **Claude API** — synthesizes a structured incident report from tip text + ML result
- **Celery worker** — handles slow video processing asynchronously (non-blocking)
- **Logging** — structured JSON logs on every request (structlog)
- **Sentry** — error tracking in production
- **Tests** — 8 pytest tests covering API endpoints and ML preprocessing

### 4. Frontend (Next.js 14 — `frontend/`)
- Landing page, tip submission form, about page
- Form validates inputs (React Hook Form + Zod), submits to backend
- Polls for video job results every 2 seconds
- Result page shows: predicted class, confidence bars, Grad-CAM heatmap, incident report
- 8 component tests (Vitest)

### 5. ML Scripts (`scripts/`)
- `train.py` — reproducible model training tracked in MLflow
- `evaluate.py` — CI quality gate (fails if accuracy drops below 70%)

### 6. CI/CD (`.github/workflows/ci.yml`)
- Linting, type checking, unit tests on every push
- Model quality gate blocks merges if accuracy degrades
- Docker builds for both services
- Staging deploy step (wired for Fly.io)

---

## What Is Still Remaining

### A. Finish Setup (30 minutes — no cost)
These are required before the platform works end-to-end.

| Task | Why needed |
|---|---|
| Add `ANTHROPIC_API_KEY` to `.env` | Without it, no incident reports are generated |
| Start Redis locally | Required for video upload queue |
| Verify model paths | Ensure `MODEL_IMAGE_PATH` points to existing model folder |

### B. Database — Submission History (2–4 hours)
Currently, results are returned and discarded. Nothing is saved.

What to add:
- PostgreSQL database
- A `submissions` table storing: ID, predicted class, confidence, threat level, timestamp
- Each analysis response gets saved before returning

### C. Cloud File Storage (1–2 hours)
Currently Grad-CAM heatmaps are returned as base64 strings inside the API response.
In production, they should be uploaded to cloud storage and returned as a URL.

What to add:
- Cloudflare R2 or AWS S3 bucket
- Upload heatmap PNG after generating it
- Return the public URL instead of base64

### D. Rate Limiting (1 hour)
The API currently has no request limits. A single user could flood it.

What to add:
- Max 10 image analyses per IP per minute
- Max 3 video analyses per IP per minute

### E. Production Deployment (2–3 hours)
The platform only runs locally right now.

What to add:
- Deploy backend API to Fly.io or Railway
- Deploy frontend to Vercel or Fly.io
- Connect a managed Redis (Upstash — free tier)
- Set all secrets in the hosting platform
- Verify HTTPS is working

### F. Real Model Training (4–8 hours, requires dataset)
The current saved models were trained in Jupyter notebooks with no reproducibility.

What to add:
- Download UCF Crime Dataset from Kaggle
- Run `scripts/train.py` to produce a properly tracked model
- Run `scripts/evaluate.py` to verify it meets the 70% threshold
- Replace the existing model files with the new output

---

## Step-by-Step: Run It Today

### Step 1 — Get the code
```bash
git clone https://github.com/askmy-stack/Anonmaly-Detection
cd Anonmaly-Detection
git checkout claude/add-claude-documentation-T2cVn
```

### Step 2 — Set secrets
```bash
cp .env.example .env
# Open .env and set:
# ANTHROPIC_API_KEY=sk-ant-...   ← get from console.anthropic.com
```

### Step 3 — Start everything
```bash
docker compose up --build
# First run takes 3–5 minutes
```

### Step 4 — Open the platform
- Frontend: http://localhost:3000
- API docs: http://localhost:8000/docs
- MLflow: http://localhost:5000

### Step 5 — Submit a test tip
1. Go to http://localhost:3000/form
2. Write a description (min 10 characters)
3. Select Image, upload any photo
4. Click **Submit Anonymous Tip**
5. View the AI classification result

### Step 6 — Run tests
```bash
# Backend
cd backend
pytest tests/ -v

# Frontend
cd frontend
npm install && npm test -- --run
```

---

## Step-by-Step: Deploy to Production

### Step 1 — Deploy backend to Fly.io
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh
flyctl auth login

cd backend
flyctl launch --name anonmaly-api
flyctl secrets set ANTHROPIC_API_KEY=sk-ant-...
flyctl secrets set REDIS_URL=rediss://...   # from upstash.com
flyctl deploy
```

### Step 2 — Deploy frontend to Vercel
```bash
npm install -g vercel
cd frontend
vercel
# Set environment variable in Vercel dashboard:
# NEXT_PUBLIC_API_URL = https://anonmaly-api.fly.dev
```

### Step 3 — Set up managed Redis
1. Go to https://upstash.com
2. Create a free Redis database
3. Copy the `REDIS_URL` from the Upstash dashboard
4. Set it as a secret in Fly.io (`flyctl secrets set REDIS_URL=...`)

### Step 4 — Enable CI secrets on GitHub
Go to: GitHub repo → Settings → Secrets and variables → Actions

| Secret name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic key |
| `FLY_API_TOKEN` | Output of `flyctl auth token` |

CI will now automatically deploy to staging on every merge to main.

---

## Effort Estimate for Full Completion

| Remaining Task | Time | Cost |
|---|---|---|
| Add database (PostgreSQL) | 2–4 hours | Free (local) / ~$5/mo (cloud) |
| Add cloud file storage | 1–2 hours | Free up to 10GB (Cloudflare R2) |
| Add rate limiting | 1 hour | Free |
| Production deployment | 2–3 hours | Free tier available (Fly.io, Vercel, Upstash) |
| Real model training | 4–8 hours | Free (Kaggle GPU) |
| **Total** | **~12–18 hours** | **~$0–$5/month** |

---

## Quick Reference

```
What exists:        Backend API, Frontend, ML models, CI/CD pipeline, Docker setup
What is missing:    Database, cloud storage, rate limiting, production deployment
Time to run locally: 10 minutes (docker compose up --build)
Time to full deploy: 12–18 hours of work
Monthly cost:       $0–$5 (all free tiers available)
```
