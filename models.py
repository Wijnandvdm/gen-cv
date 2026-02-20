from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, HttpUrl


class Spacing(BaseModel):
    section_gap: int
    line_gap: int
    after_title_gap: int


class Bullets(BaseModel):
    base_indent: int = Field(alias="base-indent")
    size: float


class Layout(BaseModel):
    starting_x: int = Field(alias="starting-x")
    starting_y: int = Field(alias="starting-y")
    new_page_y: int = Field(alias="new-page-y")
    outlined_x: int = Field(alias="outlined-x")
    font: str
    title_font_size: int = Field(alias="title-font-size")
    header_font_size: int = Field(alias="header-font-size")
    details_font_size: int = Field(alias="details-font-size")
    image_path: str = Field(alias="image-path")
    image_size: int = Field(alias="image-size")
    first_color: str = Field(alias="first-color")
    second_color: str = Field(alias="second-color")
    width_bar: int = Field(alias="width-bar")
    height_bar: int = Field(alias="height-bar")
    timeline_width: int = Field(alias="timeline-width")
    header_icon_size: int = Field(alias="header-icon-size")
    spacing: Spacing
    bullets: Bullets


class OnlinePresence(BaseModel):
    icon_path: str = Field(alias="icon-path")
    icon_size: int = Field(alias="icon-size")
    icon_x_coordinate: int = Field(alias="icon-x-coordinate")
    link: HttpUrl


class PersonalInfo(BaseModel):
    item: str
    icon_size: Optional[int] = Field(default=None, alias="icon-size")
    icon_x_coordinate: Optional[int] = Field(default=None, alias="icon-x-coordinate")


class Language(BaseModel):
    language: str
    proficiency: str


class SectionItemDetails(BaseModel):
    title: Optional[str]
    description: Optional[List[str]] = None
    link: Optional[HttpUrl] = None
    image_path: Optional[str] = Field(default=None, alias="image-path")
    image_x_coordinate: Optional[int] = Field(default=None, alias="image-x-coordinate")
    image_y_coordinate: Optional[int] = Field(default=None, alias="image-y-coordinate")
    image_size: Optional[int] = Field(default=None, alias="image-size")
    image_link: Optional[str] = Field(default=None, alias="image-link")
    bullets: Optional[List[str]] = None


class SectionItem(BaseModel):
    time_frame: Optional[str] = Field(default=None, alias="time-frame")
    details: Optional[SectionItemDetails] = None
    content: Optional[str] = None


class Section(BaseModel):
    title: str
    icon: Optional[str] = Field(default=None, alias="icon-path")
    section_content: List[SectionItem] = Field(alias="section-content")


class ToolItem(BaseModel):
    title: str
    icon_path: str = Field(alias="icon-path")


class ToolCategory(BaseModel):
    label: str
    tools: Dict[str, ToolItem]


class ToolingSection(BaseModel):
    title: str
    icon: Optional[str] = Field(default=None, alias="icon-path")
    tool_icon_size: int = Field(alias="tool-icon-size")
    tool_slot_width: int = Field(alias="tool-slot-width")
    categories: Dict[str, ToolCategory]


class CVConfig(BaseModel):
    layout: Layout
    online_presence: List[OnlinePresence] = Field(alias="online-presence")
    personal_info: List[PersonalInfo] = Field(alias="personal-info")
    languages: List[Language]
    sections: Dict[str, Union[Section, ToolingSection]]
