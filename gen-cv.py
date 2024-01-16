import utils
import sys
utils.check_requirements()
from fpdf import FPDF
import yaml

# Check if the correct number of arguments are provided
if len(sys.argv) != 2:
    utils.usage()
else:
    name = sys.argv[1]

# import config yaml
with open(f'config/{name}.yaml', 'r') as f:
    config = yaml.safe_load(f)

class PDF(FPDF):
    def make_a_cell(self, width, text, bold, font_size, url, multi_line_cell):
        if bold == True:
            self.set_font(font, 'B', font_size)
            self.cell(width, 10, text, 0 , 0, link=url)
        elif multi_line_cell == True:
            self.set_font(font, '', font_size)
            self.multi_cell(width, 5, txt=text) 
        elif bold == False:
            self.set_font(font, '', font_size)
            self.cell(width, 10, text, 0 , 0, link=url)
        else:
            print("Wrong input supplied")
        
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def header(self):
        self.set_fill_color(*first_theme_color)
        self.rect(0, 0, width_bar, height_bar, 'F')
        self.make_a_cell(width=width_bar, text="",bold=False,font_size=0,url="",multi_line_cell=False)
        self.make_a_cell(width=0,text="Curriculum Vitae",bold=True,font_size=title_font_size,url="",multi_line_cell=False)
        # Line break
        self.ln(20)

    def personal_info(self):
        self.image('images/profile_picture.png', 10, 10, image_size)
        x = 10
        y = image_size + 10
        self.set_xy(x = x, y = y)
        self.set_text_color(*second_theme_color)
        for detail in config['cv']['personal-info']:
            y += 10
            self.set_xy(x = x, y = y)
            self.make_a_cell(width=0,text=f"{detail['item']}",bold=False,font_size=details_font_size,url="",multi_line_cell=False)
            if 'icon-path' in detail:
                y += 10
                recolored_icon_path = utils.recolor_icon(f"{detail['icon-path']}",second_theme_color)
                self.image(recolored_icon_path, int(f"{detail['icon-x-coordinate']}"), y, int(f"{detail['icon-size']}"))
        # Add online presence
        y += 15
        for icon in config['cv']['online-presence']:
            x += 10
            self.set_xy(x = x, y = y)
            recolored_icon_path = utils.recolor_icon(f"{icon['icon-path']}",second_theme_color)
            self.image(recolored_icon_path, int(f"{icon['icon-x-coordinate']}"), y, int(f"{icon['icon-size']}"), link=f"{icon['link']}")
        y += 10
        x = 10
        self.set_xy(x = x, y = y)
        # Add languages and proficiency
        self.make_a_cell(width=0,text="Languages",bold=True,font_size=header_font_size,url="",multi_line_cell=False)
        for language in config['cv']['languages']:
            y += 5
            self.set_xy(x=x, y=y+2)            
            self.make_a_cell(width=30, text=f"{language['language']}",bold=False,font_size=details_font_size,url="",multi_line_cell=False)
            self.make_a_cell(width=0,text=f"{language['proficiency']}",bold=True,font_size=header_font_size,url="",multi_line_cell=False)
        # Reset font color
        self.set_text_color(0,0,0)
        return self.get_y()
    
    def add_section(self, section_details, current_y):
        x = width_bar + 10
        y = current_y
        self.set_xy(x=x, y=y)
        self.make_a_cell(width=0,text=config['cv']['sections'][f'{section_details}']['title'],bold=True,font_size=header_font_size,url="",multi_line_cell=False)
        # Add a colored line underneath the section header
        self.set_draw_color(*first_theme_color)
        self.line(x, y + 10, x + 190, y + 10)
        for item in config['cv']['sections'][f'{section_details}']['section-content']:
            y += 10
            self.set_xy(x=x, y=y)
            # Check if 'content' exists in the section
            if 'content' in item:
                y += 2
                self.set_xy(x=x, y=y)
                self.make_a_cell(width=0,text=f"{item['content']}",bold=False,font_size=details_font_size,url="",multi_line_cell=True)
                y = self.get_y() - 10
            # Check if 'link' exists in the 'details' section
            elif 'details' in item and 'link' in item['details']:
                self.make_a_cell(width=30,text=f"{item['time-frame']}",bold=False,font_size=details_font_size,url="",multi_line_cell=False)
                self.make_a_cell(width=0,text=f"{item['details']['title']}",bold=True,font_size=details_font_size,url=f"{item['details']['link']}",multi_line_cell=False)
            elif 'details' in item and 'image-path' in item['details']:
                self.make_a_cell(width=30,text=f"{item['time-frame']}",bold=False,font_size=details_font_size,url="",multi_line_cell=False)
                self.make_a_cell(width=0,text=f"{item['details']['title']}",bold=True,font_size=details_font_size,url=f"{item['details']['image-link']}",multi_line_cell=False)
                y += 10
                self.set_xy(x=x, y=y)
                self.image(f"{item['details']['image-path']}", int(f"{item['details']['image-x-coordinate']}"), y, int(f"{item['details']['image-size']}"), link=f"{item['details']['image-link']}")
                y += int(f"{item['details']['image-y-coordinate']}")
                self.set_xy(x=x, y=y)
            elif 'details' in item:
                self.make_a_cell(width=30,text=f"{item['time-frame']}",bold=False,font_size=details_font_size,url="",multi_line_cell=False)
                self.make_a_cell(width=0,text=f"{item['details']['title']}",bold=True,font_size=details_font_size,url="",multi_line_cell=False)
            # Check if 'description' exists in the 'experience-details' section
            if all('description' in item['details'] for item in config['cv']['sections'][f'{section_details}']['section-content']):
                # Add description
                for description in item['details']['description']:
                    y += 10  # Adjust for space
                    self.set_xy(x=x, y=y)
                    self.make_a_cell(width=30,text="",bold=False,font_size=details_font_size,url="",multi_line_cell=False)
                    self.make_a_cell(width=0,text=description,bold=False,font_size=details_font_size,url="",multi_line_cell=True)
                    y = self.get_y()
        y += 10  # Add extra space after the section
        self.set_xy(x=x, y=y)
        return self.get_y()

pdf = PDF()
font = config['cv']['layout']['font']
title_font_size = config['cv']['layout']['title-font-size']
header_font_size = config['cv']['layout']['header-font-size']
details_font_size = config['cv']['layout']['details-font-size']
image_size = config['cv']['layout']['image-size']
width_bar = config['cv']['layout']['width-bar']
height_bar = config['cv']['layout']['height-bar']
first_theme_color = pdf.hex_to_rgb(config['cv']['layout']['first-color'])
second_theme_color = pdf.hex_to_rgb(config['cv']['layout']['second-color'])
pdf.add_page()
pdf.personal_info()
current_y = 20 # Starting from y=20
for item in config['cv']['sections']:
    current_y = pdf.add_section(item, current_y)

pdf.output(f'{name}_cv.pdf', 'F')
print("CV created succesfully!")