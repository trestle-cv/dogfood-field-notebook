import json, os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from .models import ObservationIn
from .trestle import Trestle, observation_path

ROOT = Path(__file__).resolve().parents[1]
try:
    stored = json.loads((ROOT / ".field-notebook.json").read_text())
except (FileNotFoundError, ValueError):
    stored = {}
client = Trestle(os.getenv("TRESTLE_URL", stored.get("trestleURL", "http://127.0.0.1:7333")), os.getenv("TRESTLE_SERVICE_TOKEN", stored.get("serviceToken", "")))
app = FastAPI(title="Field Notebook", docs_url="/api/docs", redoc_url=None)

@app.get("/healthz")
async def health(): return {"status": "ok"}

@app.get("/api/observations")
async def list_observations():
    try: return await client.request(observation_path() + "?limit=100")
    except RuntimeError as error: raise HTTPException(502, str(error)) from error

@app.post("/api/observations", status_code=201)
async def create_observation(observation: ObservationIn):
    try: return await client.request(observation_path(), "POST", {"values": observation.dict()})
    except RuntimeError as error: raise HTTPException(502, str(error)) from error

app.mount("/", StaticFiles(directory=ROOT / "public", html=True), name="site")
