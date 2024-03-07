from __future__ import annotations

import dataclasses
import enum
from typing import Literal

from pydantic import BaseModel
from pydantic import FilePath


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


class HierarchicalSubject(BaseModel):
    value: str
    parent: HierarchicalSubject | None = None
    children: list[HierarchicalSubject] = dataclasses.field(default_factory=list)

    @property
    def is_root(self) -> bool:
        return self.parent is None


HierarchicalSubject.model_rebuild()


class ImageMetadata(BaseModel):
    SourceFile: FilePath
    RegionInfo: RegionInfoStruct | None = None
    Orientation: RotationEnum | None = None

    def model_dump(self, *args, **kwargs):
        result = super().model_dump(*args, **kwargs)
        result["SourceFile"] = str(self.SourceFile.resolve())
        return result
