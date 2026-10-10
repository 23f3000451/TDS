import os
from pathlib import Path

import yaml
from dotenv import dotenv_values
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/problem-b", tags=["Problem B"])


# ---------- Layer 1: defaults (hardcoded) ----------
DEFAULTS = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000",
}

print(f"DEFAULTS: {DEFAULTS}")

VALID_KEYS = set(DEFAULTS.keys())


# ---------- Layer 2: config.<env>.yaml ----------
def load_yaml_layer() -> dict:
    env = os.getenv("APP_ENV", "development")
    path = Path(f"config.{env}.yaml")
    if not path.exists():
        return {}
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    print(f"YAML CONFIG: {data}")
    return {k: v for k, v in data.items() if k in VALID_KEYS}



# ---------- Layer 3: .env file ----------
def load_dotenv_layer() -> dict:
    path = Path(".env")
    if not path.exists():
        return {}
    raw = dotenv_values(path)
    print(f".ENV CONFIG: {raw}")
    out = {}
    for k, v in raw.items():
        if k is None or v is None:
            continue
        key = k[4:].lower() if k.startswith("APP_") else k.lower()
        if key == "num_workers":
            key = "workers"
        if key in VALID_KEYS:
            out[key] = v
    print(f"DOTENV CONFIG: {out}")
    return out


# ---------- Layer 4: OS env (APP_* prefix) ----------
def load_os_env_layer() -> dict:
    out = {}
    for k, v in os.environ.items():
        if not k.startswith("APP_"):
            continue
        key = k[4:].lower()
        if key == "num_workers":
            key = "workers"
        if key in VALID_KEYS:
            out[key] = v
    print(f"OS ENV CONFIG: {out}")
    return out


# ---------- Type coercion ----------
def coerce(key: str, value):
    if key in ("port", "workers"):
        try:
            return int(value)
        except (TypeError, ValueError):
            return value
    if key == "debug":
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in ("true", "1", "yes", "on")
    return str(value)


# ---------- Merge ----------
def build_config(cli_overrides: dict) -> dict:
    merged = dict(DEFAULTS)
    for layer in (load_yaml_layer(), load_dotenv_layer(), load_os_env_layer()):
        merged.update(layer)

    for k, v in cli_overrides.items():
        if k in VALID_KEYS or k == "num_workers":
            if k == "num_workers":
                k = "workers"
            merged[k] = v

    return {k: coerce(k, merged[k]) for k in VALID_KEYS}


# ---------- Endpoint ----------
@router.get("/effective-config")
def effective_config(set: list[str] = Query(default=[])):
    cli = {}
    for item in set:
        if "=" in item:
            k, v = item.split("=", 1)
            cli[k.strip()] = v.strip()

    cfg = build_config(cli)
    cfg["api_key"] = "****"  # ALWAYS masked
    return JSONResponse(content=cfg)


# ---------- Existing hello endpoint (keep it) ----------
@router.get("/hello")
def hello_b():
    return {"message": "Hello from Problem B"}