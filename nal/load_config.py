import json
import os


def load_config(path=""):
    path = path or "user/config.json"
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
