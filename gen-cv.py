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
x_coordinate_bar = config['cv']['layout']['x-coordinate-bar']
first_theme_color = (config['cv']['layout']['first-color']['red'], config['cv']['layout']['first-color']['green'], config['cv']['layout']['first-color']['blue'])
second_theme_color = (config['cv']['layout']['second-color']['red'], config['cv']['layout']['second-color']['green'], config['cv']['layout']['second-color']['blue'])

class PDF(FPDF):
    def add_profile_picture(self):
        # Add profile picture
        self.image('profile_picture.png', 10, 10, 40)
    
    def header(self):
        self.set_fill_color(*first_theme_color)
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
        x = x_coordinate_bar + 10
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
        x = x_coordinate_bar + 10
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
            time_range = f"{item['time-frame']}"
            job_title = f"{item['details']['title']}"
            self.cell(30, 10, time_range)
            self.cell(0, 10, job_title)
            # time_range_and_details = f"{item['time-frame']}     {item['details']['title']}, {item['details']['company']}"
            # self.cell(0, 10, time_range_and_details, 0, 1)

            # Add description
            y += 5  # Adjust for space
            self.set_xy(x=x, y=y)
            self.cell(30, 10, "")
            self.multi_cell(0, 10, item['details']['description'])
            self.ln(5)  # Add extra line for spacing

            # Add additional details
            y += 5  # Adjust for space
            # self.set_xy(x=x, y=y)
            self.multi_cell(0, 10, item['details'].get('AdditionalDetails', ''))

            # Add extra space between experiences
            y += 10

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