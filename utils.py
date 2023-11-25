import importlib

def check_package(package_name):
    print("Checking requirements...")
    print(f"        Checking if package {package_name} is installed...")
    try:
        importlib.import_module(package_name)
        print(f"        {package_name} is installed, proceeding...")
    except ImportError:
        print(f"{package_name} is not installed.")
        print(f"Please execute the following command in your terminal: pip install {package_name}")
