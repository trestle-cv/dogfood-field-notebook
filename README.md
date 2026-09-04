# Field Notebook

Field Notebook is a quiet, field-journal application built with **Python + FastAPI**, Nift, and Trestle. It records typed environmental observations and exercises Trestle solely through its public HTTP API. FastAPI owns validation and the narrow browser boundary; Trestle owns durable records.

## Local development

Requirements: Python 3.11+, Nift, and a running Trestle server.

```sh
# Start Trestle first
curl -fsSL https://trestle.cv/install.sh | sh
~/.local/bin/trestle --data-dir "$PWD/.dogfood/trestle" --port 7333

# In this repository
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
export TRESTLE_URL=http://127.0.0.1:7333
export TRESTLE_ADMIN_EMAIL=admin@example.test
export TRESTLE_ADMIN_PASSWORD='choose-a-real-password'
python scripts/bootstrap.py
nift build
uvicorn app.main:app --reload --host 127.0.0.1 --port 4182
```

Open <http://127.0.0.1:4182>. Run `nift build-auto` alongside Uvicorn while editing Nift content/templates. CSS and JavaScript are maintained directly in `public/assets`.

## Quality and safety

Run `pytest`. Interactive API documentation is at `/api/docs`. Bootstrap creates `fn_observations`, writes a copy-once service token to `.field-notebook.json`, and sets owner-only permissions. Never commit that file; revoke the credential before sharing a configured checkout. In production, use TLS, an explicit secret manager, a private Trestle endpoint, and a process supervisor.
