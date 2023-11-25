import utils
import sys
utils.check_requirements()
from fpdf import FPDF
import yaml

# Check if the correct number of arguments are provided
if len(sys.argv) != 2:
    utils.usage()

# Get the config file name from the command-line argument
name = sys.argv[1]

# import config yaml
with open(f'config/{name}.yaml', 'r') as f:
    config = yaml.safe_load(f)

font = config['cv']['layout']['font']
title_font_size = config['cv']['layout']['title-font-size']
header_font_size = config['cv']['layout']['header-font-size']
details_font_size = config['cv']['layout']['details-font-size']
image_size = config['cv']['layout']['image-size']
width_bar = config['cv']['layout']['width-bar']
height_bar = config['cv']['layout']['height-bar']

class PDF(FPDF):
    def make_a_cell(self, width, text, bold, font_size, url):
        if bold == True:
            self.set_font(font, 'B', font_size)
        elif bold == False:
            self.set_font(font, '', font_size)
        else:
            print("Wrong input supplied")
        self.cell(width, 10, text, 0 , 0, link=url)

    def add_profile_picture(self):
        self.image('profile_picture.png', 10, 10, image_size)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def header(self):
        self.set_fill_color(*first_theme_color)
        self.rect(0, 0, width_bar, height_bar, 'F')
        self.make_a_cell(width=width_bar, text="",bold=False,font_size=0,url="")
        self.make_a_cell(width=0,text="Curriculum Vitae", bold=True,font_size=title_font_size,url="")
        # Line break
        self.ln(20)

    def personal_info(self):
        x = 10
        y = image_size + 10
        self.set_xy(x = x, y = y)
        # Set font color
        self.set_text_color(*second_theme_color)
        # Loop through education details in the YAML file
        for details in config['cv']['personal-info'].values():
            y += 10
            # Set current position
            self.set_xy(x = x, y = y)
            # Add education details to the PDF
            self.make_a_cell(width=0,text=details, bold=False,font_size=details_font_size,url="")
        # Add line break
        self.ln(20)

        # Print languages and proficiency
        self.make_a_cell(width=0,text="Languages", bold=True,font_size=header_font_size,url="")
        for language in config['cv']['languages']:
            y += 10
            self.set_xy(x=x, y=y+20)            
            self.make_a_cell(width=30, text=f"{language['name']}",bold=False,font_size=details_font_size,url="")
            self.make_a_cell(width=0,text=f"{language['proficiency']}", bold=True,font_size=header_font_size,url="")
        # Reset font color
        self.set_text_color(0,0,0)
        return self.get_y()
    
    def add_section(self, section_title, section_details, current_y):
        x = width_bar + 10
        y = current_y
        self.set_xy(x=x, y=y)
        # Add section title
        self.make_a_cell(width=0,text=section_title, bold=True,font_size=header_font_size,url="")
        # Add a colored line underneath the section header
        self.set_draw_color(*first_theme_color)
        self.line(x, y + 10, x + 190, y + 10)
        for item in config['cv'][f'{section_details}']:
            y += 10
            self.set_xy(x=x, y=y)
            # Check if 'link' exists in the 'details' section
            if 'details' in item and 'link' in item['details']:
                self.make_a_cell(width=30,text=f"{item['time-frame']}", bold=False,font_size=details_font_size,url="")
                self.make_a_cell(width=0,text=f"{item['details']['title']}", bold=False,font_size=details_font_size,url=f"{item['details']['link']}")
            else:
                self.make_a_cell(width=30,text=f"{item['time-frame']}", bold=False,font_size=details_font_size,url="")
                self.make_a_cell(width=0,text=f"{item['details']['title']}", bold=False,font_size=details_font_size,url="")
            # Check if 'description' exists in the 'experience-details' section
            if f'{section_details}' in config['cv'] and all('description' in item['details'] for item in config['cv'][f'{section_details}']):
                # Add description
                for description in item['details']['description']:
                    y += 5  # Adjust for space
                    self.set_xy(x=x, y=y)
                    self.make_a_cell(width=30,text="", bold=False,font_size=details_font_size,url="")
                    self.make_a_cell(width=0,text=description, bold=False,font_size=details_font_size,url="")
        self.ln(10)
        return self.get_y()

pdf = PDF()
first_theme_color = pdf.hex_to_rgb(config['cv']['layout']['first-color'])
second_theme_color = pdf.hex_to_rgb(config['cv']['layout']['second-color'])
pdf.add_page()
pdf.add_profile_picture()
pdf.personal_info()

current_y = pdf.add_section("Education", "education", 20) # Starting from y=20
current_y = pdf.add_section("Work Experience", "experience", current_y)
current_y = pdf.add_section("Certifications", "certifications", current_y)

pdf.output(f'{name}_cv.pdf', 'F')
print("CV created succesfully!")