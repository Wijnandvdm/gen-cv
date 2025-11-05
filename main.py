import sys
from datetime import datetime

from pdf_generator import PDF
from utils import load_config, usage


def main():
    if len(sys.argv) != 2:
        usage()

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
