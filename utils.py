import importlib
import sys

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
