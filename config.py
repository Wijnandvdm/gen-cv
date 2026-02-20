import sys
from pathlib import Path

import yaml

from models import CVConfig


def usage() -> None:
    print("""Script has not been called correctly.
Instead use: uv run python main.py wijnand_van_der_meijs""")
    sys.exit(1)


def load_config(name: str) -> CVConfig:
    """Load and validate CV YAML config into a CVConfig object."""
    config_path = Path("config") / f"{name}.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    return CVConfig(**raw["cv"])
