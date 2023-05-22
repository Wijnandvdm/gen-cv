from fpdf import FPDF
import yaml

# import config yaml
with open('config/wijnand.yaml', 'r') as f:
    config = yaml.safe_load(f)

class PDF(FPDF):
    def header(self):
        # Add logo image
        # self.image('logo.png', 10, 10, 33)
        self.set_fill_color(23, 54, 93)
        self.WIDTH = 210
        self.HEIGHT = 297
        self.rect(0, 0, 60, self.HEIGHT, 'F')
        # Set font and size for the header text
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Curriculum Vitae', 0, 0, 'C')
        # Line break
        self.ln(20)

    def personal_info(self):
        # Set font for the personal info
        self.set_font('Arial', '', 12)
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
        self.set_font('Arial', 'B', 14)
        # Add section title
        self.cell(0, 10, 'Education', 0, 1)
        # Set font for the education details
        self.set_font('Arial', '', 12)
        # Loop through education details in the YAML file
        for details in config['cv']['education'].values():
            # Add education details to the PDF
            self.cell(0, 10, details, 0, 1)
        # Add line break
        self.ln(10)

    def work_experience(self):
        # Set font for the work experience section
        self.set_font('Arial', 'B', 14)
        # Add section title
        self.cell(0, 10, 'Work Experience', 0, 1)
        # Set font for the work experience details
        self.set_font('Arial', '', 12)
        # Add work experience details
        self.cell(0, 10, 'Job Title, Company Name, Year', 0, 1)
        # Add line break
        self.ln(10)

pdf = PDF()
pdf.add_page()
pdf.personal_info()
pdf.education()
pdf.work_experience()
pdf.output('cv.pdf', 'F')
print("CV created succesfully!")