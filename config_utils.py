import yaml
from pathlib import Path
from models import CVConfig

def load_config(name: str) -> CVConfig:
    """Load and validate CV YAML config into a CVConfig object."""
    config_path = Path("config") / f"{name}.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    return CVConfig(**raw["cv"])
