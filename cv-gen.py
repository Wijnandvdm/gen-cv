from fpdf import FPDF
import yaml
import sys

# Check if the correct number of arguments are provided
if len(sys.argv) != 2:
    print("Wrong input. Instead use: python3 cv-gen.py template")
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
left_band_color = (config['cv']['layout']['red'], config['cv']['layout']['green'], config['cv']['layout']['blue'])

class PDF(FPDF):
    def add_profile_picture(self):
        # Add profile picture
        self.image('profile_picture.png', 10, 10, 40)
    
    def header(self):
        self.set_fill_color(*left_band_color)
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
        # Set current position
        x = 10
        y = 50
        self.set_xy(x = x, y = y)
        # Loop through education details in the YAML file
        for details in config['cv']['personal-info'].values():
            y += 10
            # Set current position
            self.set_xy(x = x, y = y)
            # Add education details to the PDF
            self.cell(0, 10, details, 0, 1)
        # Add line break
        self.ln(10)
        current_y = self.get_y()
        return current_y

def add_section(section_title, section_details, current_y):
    pdf.set_font(font, 'B', header_font_size)
    x = x_coordinate_bar + 10
    y = current_y
    pdf.set_xy(x=x, y=y)
    pdf.cell(0, 10, section_title, 0, 1)
    
    # Add a colored line underneath the section header
    pdf.set_draw_color(*left_band_color)
    pdf.line(x, y + 10, x + 190, y + 10)
    
    pdf.set_font(font, '', details_font_size)
    for details in section_details:
        y += 10
        pdf.set_xy(x=x, y=y)
        pdf.cell(0, 10, details, 0, 1)
    pdf.ln(10)
    return pdf.get_y()

pdf = PDF()
pdf.add_page()
pdf.add_profile_picture()
pdf.personal_info()

# Add "Education" section
education_details = config['cv']['education'].values()
current_y = add_section("Education", education_details, 20)  # Starting from y=20

# Add "Work Experience" section
experience_details = config['cv']['experience'].values()
add_section("Work Experience", experience_details, current_y)

pdf.output(f'{name}_cv.pdf', 'F')
print("CV created succesfully!")