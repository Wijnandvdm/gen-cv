from fpdf import FPDF
from models import CVConfig, Section
from utils import recolor_icon, hex_to_rgb


class PDF(FPDF):
    def __init__(self, config: CVConfig):
        super().__init__()
        self.config = config
        self.layout = config.layout
        self.first_theme_color = hex_to_rgb(self.layout.first_color)
        self.second_theme_color = hex_to_rgb(self.layout.second_color)

    def draw_text_cell(self, width, text, style="normal", font_size=12, url=""):
        styles = {"bold": "B", "normal": "", "multiline": "multiline"}
        font_style = styles.get(style, "")
        self.set_font(self.layout.font, "" if style == "multiline" else font_style, font_size)

        if style == "multiline":
            x_before = self.get_x()
            self.multi_cell(width, 5, txt=text)
            self.set_x(x_before)
        else:
            self.cell(width, 10, text, ln=1 if width == 0 else 0, link=url)

    def next_line(self, y, step=None):
        """Move Y down by line_gap or custom step."""
        return y + (step or self.layout.spacing.line_gap)

    def next_section(self, y):
        """Move Y down by section_gap."""
        return y + self.layout.spacing.section_gap

    def header(self):
        self.set_fill_color(*self.first_theme_color)
        self.rect(0, 0, self.layout.width_bar, self.layout.height_bar, "F")
        self.set_xy(self.layout.width_bar + 10, 10)
        self.draw_text_cell(0, "Curriculum Vitae", style="bold", font_size=self.layout.title_font_size)
        self.ln(self.layout.spacing.after_title_gap)

    def personal_info(self):
        x, y = 10, self.layout.image_size + 10
        self.image("images/profile_picture.png", 10, 10, self.layout.image_size)

        self.set_text_color(*self.second_theme_color)
        for detail in self.config.personal_info:
            y = self.next_line(y)
            self.set_xy(x, y)
            self.draw_text_cell(0, detail.item, font_size=self.layout.details_font_size)

        # Online presence
        y = self.next_line(y)
        for icon in self.config.online_presence:
            x += self.layout.spacing.line_gap
            recolored = recolor_icon(icon.icon_path, self.second_theme_color)
            self.image(recolored, icon.icon_x_coordinate, y, icon.icon_size, link=str(icon.link))

        # Languages
        y = self.next_section(y + icon.icon_size)
        self.set_xy(10, y)
        self.draw_text_cell(0, "Languages", style="bold", font_size=self.layout.header_font_size)

        for lang in self.config.languages:
            y = self.next_line(y)
            self.set_xy(10, y)
            self.draw_text_cell(30, lang.language, font_size=self.layout.details_font_size)
            self.draw_text_cell(0, lang.proficiency, style="bold", font_size=self.layout.header_font_size)

        self.set_text_color(0, 0, 0)
        return y

    def ensure_page_space(self, x: int, y: int, threshold: int = 240, reset_y: int = 20) -> int:
        """Ensure there's space left, otherwise create a new page and reset Y."""
        if self.get_y() > threshold:
            self.add_page()
            y = reset_y
            self.set_xy(x, y)
        return y


    def add_section(self, section_key: str, current_y: int):
        section: Section = self.config.sections[section_key]
        x = self.layout.width_bar + 10
        y = self.next_section(current_y)
        self.set_xy(x, y)
        y = self.ensure_page_space(x, y)

        # Header
        self.draw_text_cell(0, section.title, style="bold", font_size=self.layout.header_font_size)
        self.set_draw_color(*self.first_theme_color)
        self.line(x, y + self.layout.spacing.line_gap, x + 190, y + self.layout.spacing.line_gap)
        y = self.next_section(y)

        # Content
        for item in section.section_content:
            y = self.next_line(y)
            self.set_xy(x, y)

            if item.content:
                self.draw_text_cell(0, item.content, style="multiline", font_size=self.layout.details_font_size)
                y = self.get_y()

            elif isinstance(item.details, str):
                self.draw_text_cell(0, item.details, font_size=self.layout.details_font_size)

            elif item.details:
                self.draw_text_cell(30, item.time_frame or "", font_size=self.layout.details_font_size, style="bold")
                self.draw_text_cell(0, item.details.title or "", style="bold", font_size=self.layout.details_font_size, url=str(item.details.link) or "")

                if item.details.description:
                    for desc in item.details.description:
                        self.set_xy(x, self.get_y())
                        self.draw_text_cell(30, "", font_size=self.layout.details_font_size)
                        self.draw_text_cell(0, desc, style="multiline", font_size=self.layout.details_font_size)
                        y = self.get_y()

                if item.details.image_path:
                    y = self.next_line(y)
                    self.image(item.details.image_path,
                               item.details.image_x_coordinate or x,
                               y,
                               item.details.image_size or 40,
                               link=item.details.image_link or "")
                    y += item.details.image_y_coordinate or 0

            self.set_xy(x, y)

        return y