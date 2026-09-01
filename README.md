# eClipseBord

FastAPI + Streamlit dashboard for exploring NASA's Five Millennium Catalogs of lunar and solar eclipses. Built for the FastlyDep lab assignment — dockerized locally, deployed to Azure with Terraform.

## Stack

- **Backend:** FastAPI, serves eclipse data as JSON (`/lunar/data`, `/solar/data`)
- **Frontend:** Streamlit, Gamma vs. duration/magnitude scatter plots, eclipse type distribution
- **Infra:** Docker Compose locally, Azure Container App (backend) + Azure Web App (frontend), provisioned with Terraform

## Run locally

```bash
cd backend && uv sync
cd src/backend && uv run uvicorn api:app --reload
```

```bash
cd frontend && uv sync
cd src/frontend && uv run streamlit run app.py
```

Or with Docker Compose, from the repo root:

```bash
docker compose up --build
```

## Deploy to Azure

```bash
cd infra
terraform init
terraform apply
```

Then build and push the images to the Azure Container Registry Terraform just created:

```bash
docker login <acr-name>.azurecr.io
docker compose build
docker compose push
```

`terraform destroy` when done — the App Service plan has a fixed hourly cost.

LLM generated Readme
