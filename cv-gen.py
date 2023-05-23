from fpdf import FPDF
import yaml
import sys

# Check if the correct number of arguments are provided
if len(sys.argv) != 2:
    print("Usage: python3 cv-gen.py yourname")
    sys.exit(1)

# Get the config file name from the command-line argument
name = sys.argv[1]

# import config yaml
with open(f'config/{name}.yaml', 'r') as f:
    config = yaml.safe_load(f)

font = config['cv']['layout']['font']

class PDF(FPDF):
    def header(self):
        # Add logo image
        # self.image('logo.png', 10, 10, 33)
        self.set_fill_color(config['cv']['layout']['red'], config['cv']['layout']['green'], config['cv']['layout']['blue'])
        self.WIDTH = 210
        self.HEIGHT = 297
        self.rect(0, 0, 60, self.HEIGHT, 'F')
        # Set font and size for the header text
        self.set_font(font, 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Curriculum Vitae', 0, 0, 'C')
        # Line break
        self.ln(20)

    def personal_info(self):
        # Set font for the personal info
        self.set_font(font, '', 12)
        # Add name
        self.cell(0, 10, config['cv']['personal-info']['name'], 0, 1)
        # Add address
        self.cell(0, 10, config['cv']['personal-info']['address'], 0, 1)
        # Add phone number
        self.cell(0, 10, config['cv']['personal-info']['phone-number'], 0, 1)
        # Add email address
        self.cell(0, 10, config['cv']['personal-info']['email-address'], 0, 1)
        # Add line break
        self.ln(10)

    def education(self):
        # Set font for the education section
        self.set_font(font, 'B', 14)
        # Add section title
        self.cell(0, 10, 'Education', 0, 1)
        # Set font for the education details
        self.set_font(font, '', 12)
        # Loop through education details in the YAML file
        for details in config['cv']['education'].values():
            # Add education details to the PDF
            self.cell(0, 10, details, 0, 1)
        # Add line break
        self.ln(10)

    def work_experience(self):
        # Set font for the work experience section
        self.set_font(font, 'B', 14)
        # Add section title
        self.cell(50, 10, 'Work Experience', 100, 1)
        # Set font for the work experience details
        self.set_font(font, '', 12)
        # Loop through work experience details in the YAML file
        for details in config['cv']['experience'].values():
            # Add experience details to the PDF
            self.cell(0, 10, details, 0, 1)
        # Add line break
        self.ln(10)

pdf = PDF()
pdf.add_page()
pdf.personal_info()
pdf.education()
pdf.work_experience()
pdf.output(f'{name}_cv.pdf', 'F')
print("CV created succesfully!")