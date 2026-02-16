from pathlib import Path
from PIL import Image

ICON_MAX_SIZE = 64      # max width/height
MAX_COLORS = 64         # fewer colors = more potato

folder = Path("images")

for path in folder.glob("*_icon.png"):
    with Image.open(path) as img:
        # Resize while keeping aspect ratio
        img.thumbnail((ICON_MAX_SIZE, ICON_MAX_SIZE))

        # Convert to indexed color (8-bit palette)
        img = img.convert("P", palette=Image.ADAPTIVE, colors=MAX_COLORS)

        # Save optimized
        img.save(f"potatofied_{path}", optimize=True)

    print(f"Potato-fied: {path.name}")
