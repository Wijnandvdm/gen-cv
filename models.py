from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, HttpUrl


class Spacing(BaseModel):
    section_gap: int
    line_gap: int
    after_title_gap: int


class Layout(BaseModel):
    font: str
    title_font_size: int = Field(alias="title-font-size")
    header_font_size: int = Field(alias="header-font-size")
    details_font_size: int = Field(alias="details-font-size")
    image_size: int = Field(alias="image-size")
    first_color: str = Field(alias="first-color")
    second_color: str = Field(alias="second-color")
    width_bar: int = Field(alias="width-bar")
    height_bar: int = Field(alias="height-bar")
    spacing: Spacing


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


class SectionItem(BaseModel):
    time_frame: Optional[str] = Field(default=None, alias="time-frame")
    details: Union[str, SectionItemDetails, None] = None
    content: Optional[str] = None


class Section(BaseModel):
    title: str
    section_content: List[SectionItem] = Field(alias="section-content")


class CVConfig(BaseModel):
    layout: Layout
    online_presence: List[OnlinePresence] = Field(alias="online-presence")
    personal_info: List[PersonalInfo] = Field(alias="personal-info")
    languages: List[Language]
    sections: Dict[str, Section]
