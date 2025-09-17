import importlib
import sys
from PIL import Image

def usage():
    print("""Script has not been called correctly. 
Instead use: uv run python main.py wijnand_van_der_meijs""")
    sys.exit(1)

def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def recolor_icon(input_image_path, icon_color):
    # Open the image
    img = Image.open(f"images/{input_image_path}").convert("RGBA")

    # Separate the image into individual channels
    r, g, b, alpha_channel = img.split()

    # Create a new image with the desired icon color
    new_icon_color = Image.new("RGB", img.size, icon_color)
    new_icon_r, new_icon_g, new_icon_b = new_icon_color.split()

    # Composite the new color with the alpha channel of the original image
    img = Image.merge("RGBA", (new_icon_r, new_icon_g, new_icon_b, alpha_channel))

    output_image_path = f"images/recolored_{input_image_path}"
    # Save the result
    img.save(output_image_path)
    return output_image_path