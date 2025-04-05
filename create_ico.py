from PIL import Image
import os

def create_ico():
    # Get the absolute path to the assets directory
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    png_path = os.path.join(assets_dir, 'scheduler.png')
    ico_path = os.path.join(assets_dir, 'scheduler.ico')

    # Open PNG image
    img = Image.open(png_path)
    # Resize to standard icon sizes
    img = img.resize((32, 32), Image.Resampling.LANCZOS)
    # Save as ICO
    img.save(ico_path, format='ICO')
    print(f"Created ICO file at: {ico_path}")

if __name__ == "__main__":
    create_ico()