# servers/admin_panel/config/env_loader.py

import json
from pathlib import Path

CONFIG_JSON_PATH = Path(__file__).parent / "config.json"


def load_config_for(service_name: str) -> dict:
    """
    Carga variables globales + específicas del servicio desde config.json
    """
    with open(CONFIG_JSON_PATH) as f:
        full_config = json.load(f)

    global_vars = full_config.get("global", {})
    service_vars = full_config.get(service_name, {})
    return {**global_vars, **service_vars}
