from fpdf import FPDF

from models import Layout, Section, SectionItem, ToolingSection


class SectionRenderers(FPDF):
    """Mixin that provides section render methods. Stubs below declare the PDF base methods used here."""

    layout: Layout
    outlined_x: int

    def draw_section_header(self, title: str, necessary_page_space: int = 30, icon_path: str | None = None) -> None: ...
    def draw_text_cell(self, width: int, text: str, bold: bool = False, multiline: bool = False, font_size: int = 12, url: str = "") -> None: ...
    def draw_timeline_row(self, item: SectionItem, bold_title: bool = True, url: str = "") -> None: ...
    def draw_bullets(self, lines: list[str], x: int) -> None: ...
    def ensure_page_space(self, needed_height: int) -> bool: ...

    def render_profile(self, section: Section) -> None:
        self.draw_section_header(section.title, icon_path=section.icon)
        for item in section.section_content:
            self.ensure_page_space(40)
            self.set_x(self.outlined_x)
            self.draw_text_cell(0, item.content or "", multiline=True, font_size=self.layout.details_font_size)
            self.ln(self.layout.spacing.line_gap)

    def render_experience_tldr(self, section: Section) -> None:
        self.draw_section_header(section.title, necessary_page_space=20, icon_path=section.icon)
        for item in section.section_content:
            self.ensure_page_space(20)
            self.draw_timeline_row(item)
            if item.details and item.details.bullets:
                self.draw_bullets(lines=item.details.bullets, x=self.outlined_x)
            self.ln(self.layout.spacing.section_gap)

    def render_experience(self, section: Section) -> None:
        self.draw_section_header(section.title, necessary_page_space=50, icon_path=section.icon)
        for item in section.section_content:
            self.ensure_page_space(0)
            self.draw_timeline_row(item)
            if item.details and item.details.description:
                self.draw_bullets(lines=item.details.description, x=self.outlined_x)
            self.ln(self.layout.spacing.section_gap)

    def render_certifications(self, section: Section) -> None:
        self.draw_section_header(section.title, icon_path=section.icon)
        for item in section.section_content:
            self.ensure_page_space(15)
            url = str(item.details.link) if item.details and item.details.link else ""
            self.draw_timeline_row(item, bold_title=False, url=url)

    def render_projects(self, section: Section) -> None:
        self.draw_section_header(section.title, necessary_page_space=70, icon_path=section.icon)
        for item in section.section_content:
            if item.details is None:
                continue
            self.ensure_page_space(item.details.image_size or 0)
            self.draw_timeline_row(item, url=str(item.details.link) if item.details.link else "")
            self.ln(2)
            img_x = item.details.image_x_coordinate or self.outlined_x
            img_y = self.get_y()
            self.image(
                item.details.image_path or "",
                img_x,
                img_y,
                item.details.image_size or 0,
                link=item.details.image_link or "",
            )
            self.set_y(img_y + (item.details.image_y_coordinate or 0))

    def render_tooling(self, section: ToolingSection) -> None:
        self.draw_section_header(section.title, icon_path=section.icon)
        slot_w, icon_s = section.tool_slot_width, section.tool_icon_size
        for category in section.categories.values():
            self.set_x(self.outlined_x)
            self.draw_text_cell(0, category.label, bold=True, font_size=self.layout.details_font_size)
            icon_y = self.get_y()
            self.set_font(self.layout.font, "", self.layout.details_font_size)
            for i, tool in enumerate(category.tools.values()):
                x = self.outlined_x + i * slot_w
                self.image(tool.icon_path, x + (slot_w - icon_s) / 2, icon_y, icon_s)
                self.set_xy(x, icon_y + icon_s + 1)
                self.cell(slot_w, 4, tool.title, align="C")
                self.set_y(icon_y)
            self.ln(icon_s + 5 + self.layout.spacing.section_gap)

    def render_education(self, section: Section) -> None:
        self.draw_section_header(section.title, icon_path=section.icon)
        for item in section.section_content:
            self.ensure_page_space(15)
            self.draw_timeline_row(item, bold_title=False)
