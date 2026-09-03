# eClipseBord
### Azure Python Fullstack Lab

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Azure](https://img.shields.io/badge/Azure-Cloud_Deployed-0078D4?logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/)

A fullstack application for interactive analysis and visualization of solar and lunar eclipses, based on NASA's Five Millennium Catalogs. The project separates backend and frontend into independent modules, packages them with Docker, and deploys them to Microsoft Azure via Terraform.

---

## Table of Contents

- [Overview & Architecture](#overview--architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Local Setup & Development](#local-setup--development)
- [Running with Docker](#running-with-docker)
- [Deploying to Azure](#deploying-to-azure)
- [API Documentation](#api-documentation)
- [Tech Stack](#tech-stack)

---

## Overview & Architecture

The application consists of two independent services:

1. **Backend (FastAPI):**
   - Reads and cleans data from NASA's catalogs (`lunar.csv` and `solar.csv`).
   - Provides a RESTful API with automatic OpenAPI/Swagger documentation.
   - Converts NaN values correctly before sending data as JSON over HTTP.

2. **Frontend (Streamlit):**
   - An interactive web UI (eClipseBord) that fetches data from the backend API via `httpx`.
   - Separate views per dataset (lunar, solar), plus shared components for what's identical between them.
   - KPI cards (`st.metric`), interactive charts, and a searchable data table.

```text
       ┌───────────────────────┐
       │   Browser / Client    │
       └──────────┬────────────┘
                  │  Port 8501
                  ▼
       ┌───────────────────────┐
       │   Streamlit Frontend  │  (eClipseBord UI)
       └──────────┬────────────┘
                  │  HTTP / REST (httpx)
                  │  Port 8000
                  ▼
       ┌───────────────────────┐
       │    FastAPI Backend    │  (Uvicorn ASGI)
       └──────────┬────────────┘
                  │  Pandas I/O
                  ▼
       ┌───────────────────────┐
       │  CSV Data (NASA)      │  (backend/data/lunar.csv, solar.csv)
       └───────────────────────┘
```

In Azure, the backend is deployed as a **Container App** and the frontend as a **Web App for Containers**, both provisioned with Terraform.

---

## Features

* **Separated architecture:** the frontend has no direct file access to the data sources, everything is fetched through API calls.
* **Lunar eclipses:** KPI overview (total count, average Gamma), relationship analysis between Gamma and total eclipse duration, distribution across eclipse types.
* **Solar eclipses:** same structure as lunar, with Gamma plotted against magnitude instead of duration.
* **Robust error handling:** a failed API call (`httpx.RequestError`/`HTTPStatusError`) shows a clear error message in the UI instead of crashing the app.
* **Cloud-ready:** the backend URL is controlled via the `BACKEND_URL` environment variable, defaulting to `http://127.0.0.1:8000` locally — no configuration needed to run it on your own machine.

---

## Project Structure

```text
azure_python_fullstack_lab/
├── backend/
│   ├── data/
│   │   ├── lunar.csv
│   │   └── solar.csv
│   ├── src/backend/
│   │   ├── api.py                  # Endpoints
│   │   ├── constants.py
│   │   └── data_processing.py      # Loading & cleaning with Pandas
│   └── pyproject.toml
├── frontend/
│   ├── images/
│   │   ├── lunar_eclipse.jpg
│   │   └── solar_eclipse.jpg
│   ├── src/frontend/
│   │   ├── app.py                  # Entry point (routing & API calls)
│   │   ├── .streamlit/config.toml  # Theme
│   │   └── views/
│   │       ├── lunar.py
│   │       ├── solar.py
│   │       ├── gamma.py            # Shared Gamma metric
│   │       └── eclipse_type.py     # Shared eclipse type chart
│   └── pyproject.toml
├── dockerfiles/
│   ├── backend.dockerfile
│   └── frontend.dockerfile
├── infra/                          # Terraform: resource group, ACR, Container App, Web App
│   ├── acr.tf
│   ├── api.tf
│   ├── web_app.tf
│   ├── resource-group.tf
│   ├── providers.tf
│   ├── variables.tf
│   └── outputs.tf
├── eda/
│   └── eda.ipynb
├── .gitignore
├── .python-version
├── docker-compose.yaml
├── pyproject.toml                  # uv workspace (backend + frontend as members)
└── uv.lock
```

---

## Prerequisites

* **Python:** 3.13 or later
* **Package manager:** [uv](https://docs.astral.sh/uv/) — the project has no `requirements.txt`, everything installs through uv.
* **Docker Desktop** (optional, for running in containers)
* **Terraform** and **Azure CLI** (only needed for deployment)

---

## Local Setup & Development

### 1. Clone the project

```bash
git clone https://github.com/rickard-garnau/azure_python_fullstack_lab.git
cd azure_python_fullstack_lab
```

### 2. Start the backend

```bash
cd backend
uv sync
cd src/backend
uv run uvicorn api:app --reload
```

The backend responds at [http://127.0.0.1:8000](http://127.0.0.1:8000), Swagger docs are at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 3. Start the frontend (in a new terminal)

```bash
cd frontend
uv sync
cd src/frontend
uv run streamlit run app.py
```

The app opens at [http://localhost:8501](http://localhost:8501). No `.env` file needed — the frontend falls back to `http://127.0.0.1:8000` if `BACKEND_URL` isn't set.

---

## Running with Docker

From the repo root:

```bash
docker compose up --build
```

This builds and starts both services on the same network, with the frontend automatically pointed at `http://backend:8000`.

---

## Deploying to Azure

```bash
cd infra
terraform init
terraform apply
```

This creates the resource group, Container Registry, Container App (backend), and Web App (frontend) — and sets `BACKEND_URL` on the Web App automatically, no manual configuration needed.

Build and push the images to the registry Terraform just created:

```bash
docker login <acr-name>.azurecr.io
docker compose build
docker compose push
```

Run `terraform destroy` when you're done testing — the Web App's App Service plan has a fixed hourly cost regardless of usage.

---

## API Documentation

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/lunar/data` | Returns NASA's lunar eclipse data as JSON |
| `GET` | `/solar/data` | Returns NASA's solar eclipse data as JSON |

---

## Tech Stack

* **Language:** Python 3.13
* **Backend:** FastAPI, Uvicorn, Pandas
* **Frontend:** Streamlit, Pandas, HTTPX
* **DevOps & Cloud:** Docker, Docker Compose, Terraform, Azure Container Registry, Azure Container App, Azure Web App

---

*This README was generated with LLM assistance and reviewed against the actual repository contents before use.*
