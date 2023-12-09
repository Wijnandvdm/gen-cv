import importlib
import sys
from PIL import Image

def usage():
    print("""Script has not been called correctly. 
Instead use: python3 gen-cv.py template""")
    sys.exit(1)

def check_requirements():
    print("Checking requirements...")
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
    for requirement in requirements:
        print(f"    Checking if package {requirement} is installed...")
        try:
            importlib.import_module(requirement)
            print(f"    {requirement} is installed, proceeding...")
        except ImportError:
            print(f"{requirement} is not installed.")
            print(f"Please execute the following command in your terminal: pip install -r requirements.txt")
            sys.exit(1)

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