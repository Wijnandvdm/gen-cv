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
header_font_size = config['cv']['layout']['header-font-size']
details_font_size = config['cv']['layout']['details-font-size']
x_coordinate_bar = config['cv']['layout']['x-coordinate-bar']

class PDF(FPDF):
    def header(self):
        # Add logo image
        # self.image('logo.png', 10, 10, 33)
        self.set_fill_color(config['cv']['layout']['red'], config['cv']['layout']['green'], config['cv']['layout']['blue'])
        self.WIDTH = 210
        self.HEIGHT = 297
        self.rect(0, 0, x_coordinate_bar, self.HEIGHT, 'F')
        # Set font and size for the header text
        self.set_font(font, 'B', 15)
        # Move to the right
        self.cell(x_coordinate_bar)
        # Title
        self.cell(0, 10, 'Curriculum Vitae', 0, 0)
        # Line break
        self.ln(20)

    def personal_info(self):
        # Set font for the personal info
        self.set_font(font, '', details_font_size)
        # Add name
        self.cell(60, 10, config['cv']['personal-info']['name'], 0, 1)
        # Add address
        self.cell(60, 10, config['cv']['personal-info']['address'], 0, 1)
        # Add phone number
        self.cell(60, 10, config['cv']['personal-info']['phone-number'], 0, 1)
        # Add email address
        self.cell(60, 10, config['cv']['personal-info']['email-address'], 0, 1)
        # Add line break
        self.ln(10)

    def education(self):
        # Set font for the education section
        self.set_font(font, 'B', header_font_size)
        # Set current position
        x = x_coordinate_bar + 10
        y = 20
        self.set_xy(x = x, y = y)
        # Add section title
        self.cell(0, 10, 'Education', 0, 1)
        # Set font for the education details
        self.set_font(font, '', details_font_size)
        # Loop through education details in the YAML file
        for details in config['cv']['education'].values():
            y += 10
            # Set current position
            self.set_xy(x = x, y = y)
            # Add education details to the PDF
            self.cell(0, 10, details, 0, 1)
        # Add line break
        self.ln(10)
        current_y = self.get_y()
        return current_y

    def work_experience(self, current_y):
        # Set font for the work experience section
        self.set_font(font, 'B', header_font_size)
        # Set current position
        x = x_coordinate_bar + 10
        y = current_y
        self.set_xy(x = x, y = y)
        # Add section title
        self.cell(0, 10, 'Work Experience', 0, 1)
        # Set font for the work experience details
        self.set_font(font, '', details_font_size)
        # Loop through work experience details in the YAML file
        for details in config['cv']['experience'].values():
            y += 10
            # Set current position
            self.set_xy(x = x, y = y)
            # Add experience details to the PDF
            self.cell(0, 10, details, 0, 1)
        # Add line break
        self.ln(10)

pdf = PDF()
pdf.add_page()
pdf.personal_info()
pdf.education()
current_y=pdf.education()
pdf.work_experience(current_y=current_y)
pdf.output(f'{name}_cv.pdf', 'F')
print("CV created succesfully!")