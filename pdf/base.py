from fpdf import FPDF

from images import hex_to_rgb, recolor_icon
from models import CVConfig, SectionItem
from .renderers import SectionRenderers


class PDF(FPDF, SectionRenderers):
    def __init__(self, config: CVConfig) -> None:
        super().__init__()
        self.config = config
        self.layout = config.layout
        self.first_theme_color = hex_to_rgb(self.layout.first_color)
        self.second_theme_color = hex_to_rgb(self.layout.second_color)
        self.starting_y = 20
        self.outlined_x = self.layout.width_bar + 10

    def draw_text_cell(self, width: int, text: str, bold: bool = False, multiline: bool = False, font_size: int = 12, url: str = "") -> None:
        self.set_font(self.layout.font, "B" if bold else "", font_size)
        if multiline:
            x = self.get_x()
            self.multi_cell(width, 5, txt=text)
            self.set_x(x)
        else:
            self.cell(width, 10, text, ln=1 if width == 0 else 0, link=url)

    def draw_section_header(self, title: str, necessary_page_space: int = 30, icon_path: str | None = None) -> None:
        self.ensure_page_space(necessary_page_space)
        self.set_x(self.outlined_x)
        if icon_path:
            recolored_icon_path = recolor_icon(icon_path, self.first_theme_color)
            self.image(recolored_icon_path, self.get_x(), self.get_y() + 2, self.layout.header_icon_size)
            self.set_x(self.get_x() + self.layout.header_icon_size + 2)
        self.set_text_color(*self.first_theme_color)
        self.draw_text_cell(0, title, bold=True, font_size=self.layout.header_font_size)
        self.set_text_color(0, 0, 0)
        self.set_draw_color(*self.first_theme_color)
        self.line(self.outlined_x, self.get_y(), self.outlined_x + 190, self.get_y())
        self.ln(self.layout.spacing.section_gap)

    def header(self) -> None:
        self.set_fill_color(*self.first_theme_color)
        self.rect(0, 0, self.layout.width_bar, self.layout.height_bar, "F")
        self.set_xy(self.outlined_x, 10)
        self.set_text_color(*self.first_theme_color)
        self.draw_text_cell(0, "Curriculum Vitae", bold=True, font_size=self.layout.title_font_size)
        self.set_text_color(0, 0, 0)
        self.ln(self.layout.spacing.after_title_gap)

    def personal_info(self) -> None:
        x, y = self.layout.starting_x, self.layout.image_size + 10
        self.image(self.layout.image_path, self.layout.starting_x, self.layout.starting_y, self.layout.image_size)

        self.set_text_color(*self.second_theme_color)
        for detail in self.config.personal_info:
            y = y + 10
            self.set_xy(x, y)
            self.draw_text_cell(0, detail.item, font_size=self.layout.details_font_size)

        y = y + 10
        for icon in self.config.online_presence:
            recolored = recolor_icon(icon.icon_path, self.second_theme_color)
            self.image(recolored, icon.icon_x_coordinate, y, icon.icon_size, link=str(icon.link))

        y = y + self.layout.spacing.section_gap + icon.icon_size
        self.set_xy(self.layout.starting_x, y)
        self.draw_text_cell(0, "Languages", bold=True, font_size=self.layout.header_font_size)

        for lang in self.config.languages:
            y = y + self.layout.spacing.line_gap
            self.set_xy(self.layout.starting_x, y)
            self.draw_text_cell(self.layout.timeline_width, lang.language, font_size=self.layout.details_font_size)
            self.draw_text_cell(0, lang.proficiency, bold=True, font_size=self.layout.header_font_size)
        self.set_text_color(0, 0, 0)

    def ensure_page_space(self, needed_height: int) -> bool:
        """Ensure there's space left; if not, create a new page and reset X/Y."""
        remaining = self.h - self.get_y() - self.b_margin
        if needed_height > remaining:
            self.add_page()
            self.set_xy(self.outlined_x, self.starting_y)
            return True
        return False

    def draw_bullets(self, lines: list[str], x: int) -> None:
        """Draws lines with or without bullets. Bullet lines must start with '* '."""
        for line in lines:
            self.ensure_page_space(8)
            self.set_x(x)
            if line.startswith("* "):
                text = line[2:]
                bullet_x = x + self.layout.bullets.base_indent
                bullet_y = self.get_y() + (5 - self.layout.bullets.size) / 2
                self.ellipse(bullet_x, bullet_y, self.layout.bullets.size, self.layout.bullets.size, "F")
                self.set_x(bullet_x + self.layout.bullets.size + 3)
                self.draw_text_cell(0, text, multiline=True, font_size=self.layout.details_font_size)
            else:
                self.set_x(self.get_x() + self.layout.timeline_width)
                self.draw_text_cell(0, line, multiline=True, font_size=self.layout.details_font_size)

    def draw_timeline_row(self, item: SectionItem, bold_title: bool = True, url: str = "") -> None:
        self.set_x(self.outlined_x)
        self.draw_text_cell(self.layout.timeline_width, item.time_frame or "", bold=True, font_size=self.layout.details_font_size)
        self.draw_text_cell(0, item.details.title, bold=bold_title, font_size=self.layout.details_font_size, url=url)

    def add_section(self, section_key: str) -> None:
        getattr(self, f"render_{section_key}")(self.config.sections[section_key])
