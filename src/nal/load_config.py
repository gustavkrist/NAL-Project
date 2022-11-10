import json
import os
from typing import Any, Dict


def load_config(path: str = "") -> Dict[str, Any]:
    path = path or os.environ.get("NAL_CONFIG_PATH", "user/config.json")
    config = None
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                pass
    if config is None:
        config = {
            "data_location": "data/extracted/",
            "cache_location": "data/cache/",
            "save": False,
            "cache": True,
        }
    return config
