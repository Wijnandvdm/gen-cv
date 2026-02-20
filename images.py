from pathlib import Path

from PIL import Image


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def make_white_transparent(image_path: str, threshold: int = 240) -> None:
    img = Image.open(image_path).convert("RGBA")
    data = img.getdata()
    img.putdata([
        (r, g, b, 0) if r >= threshold and g >= threshold and b >= threshold else (r, g, b, a)
        for r, g, b, a in data
    ])
    img.save(image_path)


def potatofy_icons(folder: str, max_size: int = 64, max_colors: int = 64) -> None:
    for path in Path(folder).rglob("*_icon.png"):
        with Image.open(path) as img:
            img.thumbnail((max_size, max_size))
            img = img.convert("P", palette=Image.ADAPTIVE, colors=max_colors)
            img.save(path, optimize=True)


def prepare_icons(root_folder: str = "images") -> None:
    for path in Path(root_folder).rglob("*_icon.png"):
        make_white_transparent(str(path))
    potatofy_icons(root_folder)


def recolor_icon(input_image_path: str, icon_color: tuple[int, int, int]) -> str:
    img = Image.open(f"{input_image_path}").convert("RGBA")
    r, g, b, alpha_channel = img.split()
    new_icon_color = Image.new("RGB", img.size, icon_color)
    new_icon_r, new_icon_g, new_icon_b = new_icon_color.split()
    img = Image.merge("RGBA", (new_icon_r, new_icon_g, new_icon_b, alpha_channel))
    if "images/" in input_image_path:
        output_image_path = input_image_path.replace("images/", "images/recolored_")
    else:
        raise ValueError(f"Input image path must contain 'images/': {input_image_path}")
    img.save(output_image_path)
    return output_image_path
