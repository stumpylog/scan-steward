from __future__ import annotations

import enum
from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from pydantic import FilePath
from pydantic import field_serializer


@enum.unique
class RotationEnum(enum.IntEnum):
    """
    https://exiftool.org/TagNames/EXIF.html
    """

    HORIZONTAL = 1
    MIRROR_HORIZONTAL = 2
    ROTATE_180 = 3
    MIRROR_VERTICAL = 4
    MIRROR_HORIZONTAL_AND_ROTATE_270_CW = 5
    ROTATE_90_CW = 6
    MIRROR_HORIZONTAL_AND_ROTATE_90_CW = 7
    ROTATE_270_CW = 8


class XmpAreaStruct(BaseModel):
    """
    https://exiftool.org/TagNames/XMP.html#Area
    """

    H: float
    Unit: Literal["normalized"]
    W: float
    X: float
    Y: float
    D: float | None = None


class DimensionsStruct(BaseModel):
    """
    https://exiftool.org/TagNames/XMP.html#Dimensions
    """

    H: float
    W: float
    Unit: Literal["pixel", "inch"]


class RegionStruct(BaseModel):
    """
    https://exiftool.org/TagNames/MWG.html#RegionStruct
    """

    Area: XmpAreaStruct
    Name: str
    Type: Literal["BarCode", "Face", "Focus", "Pet"]
    Description: str | None = None


class RegionInfoStruct(BaseModel):
    """
    https://exiftool.org/TagNames/MWG.html#RegionInfo
    """

    AppliedToDimensions: DimensionsStruct
    RegionList: list[RegionStruct]


class KeywordStruct(BaseModel):
    """
    https://exiftool.org/TagNames/MWG.html#KeywordStruct
    """

    Keyword: str
    Applied: bool | None = None
    Children: list[KeywordStruct] = Field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.Keyword) + hash(self.Applied)


KeywordStruct.model_rebuild()


class KeywordInfoModel(BaseModel):
    """
    https://exiftool.org/TagNames/MWG.html#KeywordInfo
    """

    Hierarchy: list[KeywordStruct]


class ImageMetadata(BaseModel):
    SourceFile: FilePath
    RegionInfo: RegionInfoStruct | None = None
    Orientation: RotationEnum | None = None
    LastKeywordXMP: list[str] | None = None
    TagsList: list[str] | None = None
    CatalogSets: list[str] | None = None
    HierarchicalSubject: list[str] | None = None
    KeywordInfo: KeywordInfoModel | None = None

    @field_serializer("SourceFile")
    def serialize_source_file(self, source_file: FilePath, _info) -> str:
        return str(source_file.resolve())
