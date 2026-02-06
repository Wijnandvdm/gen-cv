import re

from fpdf import FPDF

from models import CVConfig
from utils import hex_to_rgb, recolor_icon


class PDF(FPDF):
    def __init__(self, config: CVConfig):
        super().__init__()
        self.config = config
        self.layout = config.layout
        self.first_theme_color = hex_to_rgb(self.layout.first_color)
        self.second_theme_color = hex_to_rgb(self.layout.second_color)
        self.starting_y = 20
        self.page_break_trigger = 270

    def draw_text_cell(self, width, text, bold=False, multiline=False, font_size=12, url=""):
        self.set_font(self.layout.font, "B" if bold else "", font_size)
        if multiline:
            x = self.get_x()
            self.multi_cell(width, 5, txt=text)
            self.set_x(x)
        else:
            self.cell(width, 10, text, ln=1 if width == 0 else 0, link=url)

    def header(self):
        self.set_fill_color(*self.first_theme_color)
        self.rect(0, 0, self.layout.width_bar, self.layout.height_bar, "F")
        self.set_xy(self.layout.width_bar + 10, 10)
        self.draw_text_cell(0, "Curriculum Vitae", bold=True, font_size=self.layout.title_font_size)
        self.ln(self.layout.spacing.after_title_gap)

    def personal_info(self):
        x, y = 10, self.layout.image_size + 10
        self.image("images/profile_picture.png", 10, 10, self.layout.image_size)

        self.set_text_color(*self.second_theme_color)
        for detail in self.config.personal_info:
            y = y + 10
            self.set_xy(x, y)
            self.draw_text_cell(0, detail.item, font_size=self.layout.details_font_size)

        # Online presence
        y = y + 10
        for icon in self.config.online_presence:
            recolored = recolor_icon(icon.icon_path, self.second_theme_color)
            self.image(
                recolored,
                icon.icon_x_coordinate,
                y,
                icon.icon_size,
                link=str(icon.link),
            )

        # Languages
        y = y + self.layout.spacing.section_gap + icon.icon_size
        self.set_xy(10, y)
        self.draw_text_cell(0, "Languages", bold=True, font_size=self.layout.header_font_size)

        for lang in self.config.languages:
            y = y + self.layout.spacing.line_gap
            self.set_xy(10, y)
            self.draw_text_cell(30, lang.language, font_size=self.layout.details_font_size)
            self.draw_text_cell(
                0,
                lang.proficiency,
                bold=True,
                font_size=self.layout.header_font_size,
            )

        self.set_text_color(0, 0, 0)

    def ensure_page_space(self, needed_height: int) -> bool:
        """Ensure there's space left; if not, create a new page and reset X/Y.

        Uses the actual remaining space on the page (considering bottom margin) instead
        of a fixed trigger. Returns True when a page was added.
        """
        # remaining printable vertical space on this page
        remaining = self.h - self.get_y() - self.b_margin
        if needed_height >= remaining:
            self.add_page()
            # place cursor at the start of the right column/header area
            self.set_xy(self.layout.width_bar + 10, self.starting_y)
            return True
        return False

    def add_section(self, section_key):
        section = self.config.sections[section_key]

        if section_key == "profile":
            self.render_profile(section)
        elif section_key == "experience":
            self.render_experience(section)
        elif section_key == "certifications":
            self.render_certifications(section)
        elif section_key == "projects":
            self.render_projects(section)
        elif section_key == "education":
            self.render_education(section)

    def render_profile(self, section):
        x = self.layout.width_bar + 10

        # header
        self.ensure_page_space(30)
        self.set_xy(x, self.get_y())
        self.draw_text_cell(0, section.title, bold=True, font_size=self.layout.header_font_size)

        # single text blob
        for item in section.section_content:
            self.ensure_page_space(40)
            self.set_xy(x, self.get_y())
            self.draw_text_cell(0, item.content, multiline=True, font_size=self.layout.details_font_size)
            self.ln(self.layout.spacing.line_gap)

    def render_experience(self, section):
        x = self.layout.width_bar + 10

        # header
        self.ensure_page_space(0)
        self.set_xy(x, self.get_y())
        self.draw_text_cell(0, section.title, bold=True, font_size=self.layout.header_font_size)

        for item in section.section_content:
            # time frame + title must stay together
            self.ensure_page_space(0)
            self.set_xy(x, self.get_y())

            self.draw_text_cell(30, item.time_frame or "", bold=True, font_size=self.layout.details_font_size)
            self.draw_text_cell(0, item.details.title, bold=True, font_size=self.layout.details_font_size)

            if item.details.description:
                for desc in item.details.description:
                    self.ensure_page_space(0)
                    self.set_xy(x, self.get_y())

                    if not desc.strip():
                        self.ln(self.layout.spacing.line_gap)
                        continue

                    m = re.match(r"^(?P<indent>\s*)([-*+])\s+(?P<text>.+)$", desc)
                    if m:
                        indent = len(m.group("indent")) // 2
                        base_indent = 30
                        extra = indent * 8

                        bullet_x = x + base_indent + extra + 2
                        bullet_y = self.get_y() + 2
                        self.set_fill_color(*self.first_theme_color)
                        self.ellipse(bullet_x + 1.5, bullet_y + 1.5, 1.5, 1.5, "F")

                        self.set_xy(x + base_indent + extra + 8, self.get_y())
                        self.draw_text_cell(0, m.group("text"), multiline=True, font_size=self.layout.details_font_size)
                    else:
                        self.draw_text_cell(30, "", font_size=self.layout.details_font_size)
                        self.draw_text_cell(0, desc, multiline=True, font_size=self.layout.details_font_size)

            self.ln(self.layout.spacing.section_gap)

    def render_certifications(self, section):
        x = self.layout.width_bar + 10

        self.ensure_page_space(30)
        self.set_xy(x, self.get_y())
        self.draw_text_cell(0, section.title, bold=True, font_size=self.layout.header_font_size)
        self.ln(self.layout.spacing.section_gap)

        for item in section.section_content:
            self.ensure_page_space(15)
            self.set_xy(x, self.get_y())

            self.draw_text_cell(30, item.time_frame, bold=True, font_size=self.layout.details_font_size)
            self.draw_text_cell(
                0,
                item.details.title,
                font_size=self.layout.details_font_size,
                url=str(item.details.link) if item.details.link else "",
            )

    def render_projects(self, section):
        x = self.layout.width_bar + 10

        self.ensure_page_space(70)
        self.set_xy(x, self.get_y())
        self.draw_text_cell(0, section.title, bold=True, font_size=self.layout.header_font_size)
        self.ln(self.layout.spacing.section_gap)

        for item in section.section_content:
            img_size = item.details.image_size or 40

            # header + image must stay together
            self.ensure_page_space(img_size)

            self.set_xy(x, self.get_y())
            self.draw_text_cell(30, item.time_frame or "", bold=True, font_size=self.layout.details_font_size)
            self.draw_text_cell(
                0, item.details.title, bold=True, font_size=self.layout.details_font_size, url=item.details.link or ""
            )

            self.ln(2)

            img_x = item.details.image_x_coordinate or x
            img_y = self.get_y()

            self.image(item.details.image_path, img_x, img_y, img_size, link=item.details.image_link or "")
            self.set_y(img_y + item.details.image_y_coordinate)

    def render_education(self, section):
        x = self.layout.width_bar + 10

        self.ensure_page_space(30)
        self.set_xy(x, self.get_y())
        self.draw_text_cell(
            0,
            section.title,
            bold=True,
            font_size=self.layout.header_font_size,
        )
        self.ln(self.layout.spacing.section_gap)

        for item in section.section_content:
            self.ensure_page_space(15)
            self.set_xy(x, self.get_y())

            self.draw_text_cell(30, item.time_frame, bold=True, font_size=self.layout.details_font_size)
            self.draw_text_cell(0, item.details.title, font_size=self.layout.details_font_size)
