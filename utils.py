import sys
from pathlib import Path

import yaml
from PIL import Image

from models import CVConfig


def usage():
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


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def make_white_transparent(image_path, threshold=240):
    img = Image.open(image_path).convert("RGBA")
    data = img.getdata()
    img.putdata([
        (r, g, b, 0) if r >= threshold and g >= threshold and b >= threshold else (r, g, b, a)
        for r, g, b, a in data
    ])
    img.save(image_path)


def potatofy_icons(folder, max_size=64, max_colors=64):
    for path in Path(folder).rglob("*_icon.png"):
        with Image.open(path) as img:
            img.thumbnail((max_size, max_size))
            img = img.convert("P", palette=Image.ADAPTIVE, colors=max_colors)
            img.save(path, optimize=True)


def prepare_icons(root_folder="images"):
    for path in Path(root_folder).rglob("*_icon.png"):
        make_white_transparent(str(path))
    potatofy_icons(root_folder)


def recolor_icon(input_image_path, icon_color):
    # Open the image
    img = Image.open(f"{input_image_path}").convert("RGBA")

    # Separate the image into individual channels
    r, g, b, alpha_channel = img.split()

    # Create a new image with the desired icon color
    new_icon_color = Image.new("RGB", img.size, icon_color)
    new_icon_r, new_icon_g, new_icon_b = new_icon_color.split()

    # Composite the new color with the alpha channel of the original image
    img = Image.merge("RGBA", (new_icon_r, new_icon_g, new_icon_b, alpha_channel))

    # check if the image contains the string images/ in its path
    if "images/" in input_image_path:
        output_image_path = input_image_path.replace("images/", "images/recolored_")
    else:
        raise ValueError(f"Input image path must contain 'images/': {input_image_path}")
            
    # Save the result
    img.save(output_image_path)
    return output_image_path
