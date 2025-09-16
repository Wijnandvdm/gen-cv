from fpdf import FPDF
from models import CVConfig, Section
from utils import recolor_icon


class PDF(FPDF):
    def __init__(self, config: CVConfig):
        super().__init__()
        self.config = config
        self.layout = config.layout
        # Precompute colors as RGB tuples
        self.first_theme_color = self.hex_to_rgb(self.layout.first_color)
        self.second_theme_color = self.hex_to_rgb(self.layout.second_color)

    # ------------------------
    # Helpers
    # ------------------------
    def hex_to_rgb(self, hex_color: str) -> tuple[int, int, int]:
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def draw_text_cell(self, width, text, style="normal", font_size=12, url=""):
        styles = {"bold": "B", "normal": "", "multiline": "multiline"}
        font_style = styles.get(style, "")
        self.set_font(self.layout.font, font_style if font_style != "multiline" else "", font_size)

        if style == "multiline":
            x_before = self.get_x()
            self.multi_cell(width, 5, txt=text)
            self.set_x(x_before)  # reset X so we don't "stick" to the left margin
        else:
            # Use ln=1 to ensure we drop to the next line if width==0
            self.cell(width, 10, text, ln=1 if width == 0 else 0, link=url)


    # ------------------------
    # Page elements
    # ------------------------
    def header(self):
        self.set_fill_color(*self.first_theme_color)
        self.rect(0, 0, self.layout.width_bar, self.layout.height_bar, "F")

        # Move to the right of the sidebar
        self.set_xy(self.layout.width_bar + 10, 10)

        # Title
        self.draw_text_cell(
            width=0,
            text="Curriculum Vitae",
            style="bold",
            font_size=self.layout.title_font_size,
        )
        self.ln(20)


    def personal_info(self):
        """Draws personal info block (picture, details, online presence, languages) with unified spacing."""
        x = 10
        y = self.layout.image_size + 10

        # Profile picture
        self.image("images/profile_picture.png", 10, 10, self.layout.image_size)

        # Personal details
        self.set_xy(x, y)
        self.set_text_color(*self.second_theme_color)
        for detail in self.config.personal_info:
            y += self.layout.spacing.line_gap
            self.set_xy(x, y)
            self.draw_text_cell(
                width=0,
                text=detail.item,
                style="normal",
                font_size=self.layout.details_font_size,
            )

        # Online presence icons
        y += self.layout.spacing.line_gap
        for icon in self.config.online_presence:
            x += self.layout.spacing.line_gap
            self.set_xy(x, y)
            recolored_icon = recolor_icon(icon.icon_path, self.second_theme_color)
            self.image(
                recolored_icon,
                icon.icon_x_coordinate,
                y,
                icon.icon_size,
                link=str(icon.link),
            )

        # Languages
        y += self.layout.spacing.section_gap + icon.icon_size
        x = 10
        self.set_xy(x, y)
        self.draw_text_cell(
            width=0,
            text="Languages",
            style="bold",
            font_size=self.layout.header_font_size,
        )

        for lang in self.config.languages:
            y += self.layout.spacing.line_gap
            self.set_xy(x, y)
            self.draw_text_cell(
                width=30,
                text=lang.language,
                style="normal",
                font_size=self.layout.details_font_size,
            )
            self.draw_text_cell(
                width=0,
                text=lang.proficiency,
                style="bold",
                font_size=self.layout.header_font_size,
            )

        # Reset font color
        self.set_text_color(0, 0, 0)
        return self.get_y()


    def add_section(self, section_key: str, current_y: int):
        section: Section = self.config.sections[section_key]
        x = self.layout.width_bar + 10
        y = current_y + self.layout.spacing.section_gap  # spacing comes BEFORE

        self.set_xy(x, y)

        # Page break check
        if self.get_y() > 240:
            self.add_page()
            y = 20
            self.set_xy(x, y)

        # Section header
        self.draw_text_cell(
            width=0,
            text=section.title,
            style="bold",
            font_size=self.layout.header_font_size,
        )
        self.set_draw_color(*self.first_theme_color)
        self.line(x, y + self.layout.spacing.line_gap, x + 190, y + self.layout.spacing.line_gap)
        y += self.layout.spacing.section_gap

        # Section content
        for item in section.section_content:
            y += self.layout.spacing.line_gap
            self.set_xy(x, y)

            if item.content:
                self.draw_text_cell(
                    width=0,
                    text=item.content,
                    style="multiline",
                    font_size=self.layout.details_font_size,
                )
                y = self.get_y()

            elif isinstance(item.details, str):
                self.draw_text_cell(
                    width=0,
                    text=item.details,
                    style="normal",
                    font_size=self.layout.details_font_size,
                )

            elif item.details:
                # Time-frame
                self.draw_text_cell(
                    width=30,
                    text=item.time_frame or "",
                    style="bold",
                    font_size=self.layout.details_font_size,
                )

                # Title + link
                self.draw_text_cell(
                    width=0,
                    text=item.details.title or "",
                    style="bold",
                    font_size=self.layout.details_font_size,
                    url=str(item.details.link) or "",
                )

                # Description
                if item.details.description:
                    for desc in item.details.description:
                        self.set_xy(x, self.get_y())
                        self.draw_text_cell(
                            width=30, text="", font_size=self.layout.details_font_size
                        )
                        self.draw_text_cell(
                            width=0,
                            text=desc,
                            style="multiline",
                            font_size=self.layout.details_font_size,
                        )
                        y = self.get_y()

                # Image
                if item.details.image_path:
                    y += self.layout.spacing.line_gap
                    self.set_xy(x, y)
                    self.image(
                        item.details.image_path,
                        item.details.image_x_coordinate or x,
                        y,
                        item.details.image_size or 40,
                        link=item.details.image_link or "",
                    )
                    y += item.details.image_y_coordinate or 0

            self.set_xy(x, y)

        return self.get_y()
