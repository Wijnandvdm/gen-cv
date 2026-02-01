from fpdf import FPDF
import re

from models import CVConfig, Section
from utils import hex_to_rgb, recolor_icon


class PDF(FPDF):
    def __init__(self, config: CVConfig):
        super().__init__()
        self.config = config
        self.layout = config.layout
        self.first_theme_color = hex_to_rgb(self.layout.first_color)
        self.second_theme_color = hex_to_rgb(self.layout.second_color)
        # self.page_number = 1

    def draw_text_cell(self, width, text, style="normal", font_size=12, url=""):
        styles = {"bold": "B", "normal": "", "multiline": "multiline"}
        font_style = styles.get(style, "")
        print(f"font_style: {font_style}")
        self.set_font(
            self.layout.font, "" if style == "multiline" else font_style, font_size
        )

        if style == "multiline":
            x_before = self.get_x()
            self.multi_cell(width, 5, txt=text)
            self.set_x(x_before)
        else:
            self.cell(width, 10, text, ln=1 if width == 0 else 0, link=url)

    def header(self):
        self.set_fill_color(*self.first_theme_color)
        self.rect(0, 0, self.layout.width_bar, self.layout.height_bar, "F")
        self.set_xy(self.layout.width_bar + 10, 10)
        self.draw_text_cell(
            0, "Curriculum Vitae", style="bold", font_size=self.layout.title_font_size
        )
        self.ln(self.layout.spacing.after_title_gap)

    def personal_info(self):
        x, y = 10, self.layout.image_size + 10
        self.image("images/profile_picture.png", 10, 10, self.layout.image_size)

        self.set_text_color(*self.second_theme_color)
        for detail in self.config.personal_info:
            y = y + self.layout.spacing.line_gap
            self.set_xy(x, y)
            self.draw_text_cell(0, detail.item, font_size=self.layout.details_font_size)

        # Online presence
        y = y + self.layout.spacing.line_gap
        for icon in self.config.online_presence:
            x += self.layout.spacing.line_gap
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
        self.draw_text_cell(
            0, "Languages", style="bold", font_size=self.layout.header_font_size
        )

        for lang in self.config.languages:
            y = y + self.layout.spacing.line_gap
            self.set_xy(10, y)
            self.draw_text_cell(
                30, lang.language, font_size=self.layout.details_font_size
            )
            self.draw_text_cell(
                0,
                lang.proficiency,
                style="bold",
                font_size=self.layout.header_font_size,
            )

        self.set_text_color(0, 0, 0)
        return y

    def ensure_page_space(
        self, x: int, y: int, threshold: int = 240, reset_y: int = 20
    ) -> int:
        """Ensure there's space left, otherwise create a new page and reset Y."""
        if self.get_y() > threshold:
            self.add_page()
            y = reset_y
            self.set_xy(x, y)
        return y

    # def ensure_page_space(self):
    #     """Ensure there's space left, otherwise create a new page and reset Y."""
        # self.page_number = self.page_no()
        # if self.page_number != self.page_no():
        #     self.page_number = self.page_number + 1
        #     print(f"Creating new page: {self.page_number}")
        #     print(f"current y is: {self.get_y()}")
        #     self.add_page()
        #     print(f"new page y is: {self.get_y()}")
        #     current_y = self.get_y() + 20
        #     self.set_xy(self.layout.width_bar + 10, current_y)
        # else:
        #     print(f"Continuing on page: {self.page_number} with y {self.get_y()}")


    def add_section(self, section_key: str, current_y: int):
        section: Section = self.config.sections[section_key]
        x = self.layout.width_bar + 10
        y = current_y + self.layout.spacing.section_gap
        self.set_xy(x, y)
        y = self.ensure_page_space(x, y)

        # Header
        self.draw_text_cell(
            0, section.title, style="bold", font_size=self.layout.header_font_size
        )
        self.set_draw_color(*self.first_theme_color)
        self.line(
            x,
            y + self.layout.spacing.line_gap,
            x + 190,
            y + self.layout.spacing.line_gap,
        )
        y = y + self.layout.spacing.section_gap

        # Content
        for item in section.section_content:
            y = y + self.layout.spacing.line_gap
            self.set_xy(x, y)

            if item.content:
                self.draw_text_cell(
                    0,
                    item.content,
                    style="multiline",
                    font_size=self.layout.details_font_size,
                )
                y = self.get_y()

            elif isinstance(item.details, str):
                self.draw_text_cell(
                    0, item.details, font_size=self.layout.details_font_size
                )

            elif item.details:
                self.draw_text_cell(
                    30,
                    item.time_frame or "",
                    font_size=self.layout.details_font_size,
                    style="bold",
                )
                self.draw_text_cell(
                    0,
                    item.details.title or "",
                    style="bold",
                    font_size=self.layout.details_font_size,
                    url=str(item.details.link) if item.details.link else "",
                )

                if item.details.description:
                    for desc in item.details.description:
                        self.set_xy(x, self.get_y())

                        # Empty lines should create spacing
                        if not desc or not desc.strip():
                            self.draw_text_cell(0, "", style="multiline", font_size=self.layout.details_font_size)
                            y = self.get_y()
                            continue

                        # Detect bullet-like patterns (e.g., '- item', '* item') and optional indentation
                        m = re.match(r"^(?P<indent>\s*)([-*+])\s+(?P<text>.+)$", desc)
                        if m:
                            indent_spaces = len(m.group('indent'))
                            # base indent (after the time-frame column)
                            base_indent = 30
                            # increase indent for nested bullets (2 spaces per nest)
                            nested_level = indent_spaces // 2
                            extra_indent = nested_level * 8

                            # Draw small filled bullet
                            bullet_x = x + base_indent + extra_indent + 2
                            bullet_y = self.get_y() + 2
                            self.set_fill_color(*self.first_theme_color)
                            # ellipse(x_center, y_center, rx, ry, style='F') - center at +1
                            self.ellipse(bullet_x + 1.5, bullet_y + 1.5, 1.5, 1.5, 'F')

                            # Draw the text after the bullet
                            self.set_xy(x + base_indent + extra_indent + 8, self.get_y())
                            self.draw_text_cell(
                                0,
                                m.group('text'),
                                style="multiline",
                                font_size=self.layout.details_font_size,
                            )
                        else:
                            # regular description line
                            self.draw_text_cell(30, "", font_size=self.layout.details_font_size)
                            self.draw_text_cell(
                                0,
                                desc,
                                style="multiline",
                                font_size=self.layout.details_font_size,
                            )

                        y = self.get_y()

                if item.details.image_path:
                    y = y + self.layout.spacing.line_gap
                    self.image(
                        item.details.image_path,
                        item.details.image_x_coordinate or x,
                        y,
                        item.details.image_size or 40,
                        link=item.details.image_link if item.details.image_link else "",
                    )
                    y += item.details.image_y_coordinate or 0

            self.set_xy(x, y)

        return y
