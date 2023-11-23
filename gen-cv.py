from fpdf import FPDF
import yaml
import sys
import utils

# Check if the correct number of arguments are provided
if len(sys.argv) != 2:
    print("Wrong input. Instead use: python3 gen-cv.py template")
    sys.exit(1)

# Example usage
utils.check_package("fpdf")

# Get the config file name from the command-line argument
name = sys.argv[1]

# import config yaml
with open(f'config/{name}.yaml', 'r') as f:
    config = yaml.safe_load(f)

font = config['cv']['layout']['font']
header_font_size = config['cv']['layout']['header-font-size']
details_font_size = config['cv']['layout']['details-font-size']
width_bar = config['cv']['layout']['width-bar']
height_bar = config['cv']['layout']['height-bar']
first_theme_color = (config['cv']['layout']['first-color']['red'], config['cv']['layout']['first-color']['green'], config['cv']['layout']['first-color']['blue'])
second_theme_color = (config['cv']['layout']['second-color']['red'], config['cv']['layout']['second-color']['green'], config['cv']['layout']['second-color']['blue'])

class PDF(FPDF):
    def make_a_cell(self, width, text, bold, font_size):
        if bold == True:
            self.set_font("Arial", 'B', font_size)
        elif bold == False:
            self.set_font("Arial", '', font_size)
        else:
            print("Wrong input supplied")
        self.cell(width, 10, text, 0 , 0)

    def add_profile_picture(self):
        self.image('profile_picture.png', 10, 10, 40)
    
    def header(self):
        self.set_fill_color(*first_theme_color)
        self.rect(0, 0, width_bar, height_bar, 'F')
        self.make_a_cell(width=width_bar, text="",bold=False,font_size=0)
        self.make_a_cell(width=0,text="Curriculum Vitae", bold=True,font_size=15)
        # Line break
        self.ln(20)

    def personal_info(self):
        # Set font for the personal info
        self.set_font(font, '', details_font_size)
        # Set font color
        self.set_text_color(*second_theme_color)
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

        # Print languages and proficiency
        self.set_font(font, 'B', header_font_size)
        self.cell(0, 10, 'Languages', 0, 1)
        self.set_font(font, '', details_font_size)
        
        for language in config['cv']['languages']:
            y += 10
            self.set_xy(x=x, y=y+20)
            language_and_proficiency = f"{language['name']} {language['proficiency']}"
            self.cell(0, 10, language_and_proficiency, 0, 1)

        # Add line break
        self.ln(10)
        # Reset font color
        self.set_text_color(0,0,0)

        return self.get_y()

    def add_education_section(self, section_title, section_timeframe, section_details, current_y):
        self.set_font(font, 'B', header_font_size)
        x = width_bar + 10
        y = current_y
        self.set_xy(x=x, y=y)
        self.cell(0, 10, section_title, 0, 1)
        
        # Add a colored line underneath the section header
        self.set_draw_color(*first_theme_color)
        self.line(x, y + 10, x + 190, y + 10)
        
        self.set_font(font, '', details_font_size)
        for time_range, details in zip(section_timeframe, section_details):
            y += 10
            self.set_xy(x=x, y=y)
            self.cell(30, 10, time_range)
            self.cell(0, 10, details)
        self.ln(10)
        return self.get_y()
    
    def add_work_experience_section(self, current_y):
        self.set_font(font, 'B', header_font_size)
        x = width_bar + 10
        y = current_y
        self.set_xy(x=x, y=y)
        self.cell(0, 10, 'Work Experience', 0, 1)
        
        
        # Set font for work experience
        self.set_font(font, '', details_font_size)
        # Set current position

        self.set_xy(x=x, y=y)
        # Add a colored line underneath the section header
        self.set_draw_color(*first_theme_color)
        self.line(x, y + 10, x + 190, y + 10)
        # Add "Work Experience" section
        for item in config['cv']['experience']:
            y += 10
            self.set_xy(x=x, y=y)
            self.cell(30, 10, f"{item['time-frame']}")
            self.cell(0, 10, f"{item['details']['title']}")

            # Add description
            for description in item['details']['description']:
                y += 5  # Adjust for space
                self.set_xy(x=x, y=y)
                self.cell(30, 10, "")
                self.cell(0, 10, description)
                self.ln(5)  # Add extra line for spacing
        return y

pdf = PDF()
pdf.add_page()
pdf.add_profile_picture()
pdf.personal_info()

# Add "Education" section
education_time_frames = [item['time-frame'] for item in config['cv']['education']]
education_details = [item['details'] for item in config['cv']['education']]
current_y = pdf.add_education_section("Education", education_time_frames, education_details, 20)  # Starting from y=20

# Add "Work Experience" section
current_y = pdf.add_work_experience_section(current_y)

pdf.output(f'{name}_cv.pdf', 'F')
print("CV created succesfully!")