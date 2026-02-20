import sys
from datetime import datetime

from pdf_generator import PDF
from utils import load_config, prepare_icons, usage


def main():
    if len(sys.argv) != 2:
        usage()

    name = sys.argv[1]
    prepare_icons()
    config = load_config(name)

    pdf = PDF(config)
    pdf.add_page()
    pdf.personal_info()
    pdf.set_xy(pdf.layout.width_bar + 10, pdf.starting_y)

    for section_key in config.sections:
        pdf.add_section(section_key)

    print("Pages:", pdf.page_no())

    pdf.output(f"cv_{datetime.now().year}_{name}.pdf", "F")
    print("CV created successfully!")


if __name__ == "__main__":
    main()
