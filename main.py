from config_utils import load_config
from pdf_generator import PDF
from datetime import datetime
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <config_name>")
        sys.exit(1)

    name = sys.argv[1]
    config = load_config(name)

    pdf = PDF(config)
    pdf.add_page()
    pdf.personal_info()

    current_y = 20
    for section_key in config.sections:
        current_y = pdf.add_section(section_key, current_y)

    current_year = datetime.now().year
    pdf.output(f"cv_{current_year}_{name}.pdf", "F")
    print("CV created successfully!")

if __name__ == "__main__":
    main()
