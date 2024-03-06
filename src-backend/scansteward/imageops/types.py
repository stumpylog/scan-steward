from __future__ import annotations

import dataclasses
import enum
from typing import TYPE_CHECKING
from typing import Literal

from scansteward.imageops.errors import ImageOperationMissingRequiredDataError

if TYPE_CHECKING:
    from pathlib import Path


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


@dataclasses.dataclass(frozen=True)
class XmpAreaStruct:
    """
    https://exiftool.org/TagNames/XMP.html#Area
    """

    h: float
    unit: Literal["normalized"]
    w: float
    x: float
    y: float
    d: float | None = None

    def to_json(self) -> dict:
        return {"H": self.h, "W": self.w, "X": self.x, "Y": self.y, "Unit": self.unit}

    @staticmethod
    def from_json(data: dict) -> XmpAreaStruct:
        return XmpAreaStruct(
            h=data["H"],
            w=data["W"],
            x=data["X"],
            y=data["Y"],
            unit=data["Unit"],
            d=data.get("D"),
        )


@dataclasses.dataclass(frozen=True)
class DimensionsStruct:
    """
    https://exiftool.org/TagNames/XMP.html#Dimensions
    """

    H: float
    W: float
    unit: Literal["pixel", "inch"]

    def to_json(self) -> dict:
        return {"W": self.W, "H": self.H, "Unit": self.unit}

    @staticmethod
    def from_json(data: dict) -> DimensionsStruct:
        return DimensionsStruct(H=data["H"], W=data["W"], unit=data["Unit"])


@dataclasses.dataclass(frozen=True)
class RegionStruct:
    """
    https://exiftool.org/TagNames/MWG.html#RegionStruct
    """

    Area: XmpAreaStruct
    Name: str
    Type: Literal["BarCode", "Face", "Focus", "Pet"]
    Description: str | None = None

    def to_json(self) -> dict:
        data = {
            "Area": self.Area.to_json(),
            "Name": self.Name,
            "Type": self.Type,
        }
        if self.Description:
            data["Description"] = self.Description
        return data

    @staticmethod
    def from_json(data: dict) -> RegionStruct:
        return RegionStruct(
            XmpAreaStruct.from_json(data["Area"]),
            Name=data["Name"],
            Type=data["Type"],
            Description=data.get("Description"),
        )


@dataclasses.dataclass(frozen=True)
class RegionInfoStruct:
    """
    https://exiftool.org/TagNames/MWG.html#RegionInfo
    """

    AppliedToDimensions: DimensionsStruct
    RegionList: list[RegionStruct]

    def to_json(self) -> dict:

        return {
            "AppliedToDimensions": self.AppliedToDimensions.to_json(),
            "RegionList": [x.to_json() for x in self.RegionList],
        }

    @staticmethod
    def from_json(data: dict) -> RegionInfoStruct:
        struct = RegionInfoStruct(
            DimensionsStruct.from_json(data["AppliedToDimensions"]),
            [RegionStruct.from_json(x) for x in data["RegionList"]],
        )
        return struct


@dataclasses.dataclass
class HierarchicalSubject:
    value: str
    parent: HierarchicalSubject | None = None
    children: list[HierarchicalSubject] = dataclasses.field(default_factory=list)

    @property
    def is_root(self) -> bool:
        return self.parent is None

    def __getitem__(self, key: str) -> HierarchicalSubject:
        for child in self.children:
            if child.value == key:
                return child
        raise KeyError(key)


class ImageMetadata:
    source_file: Path
    region_info: RegionInfoStruct | None = None
    rotation: RotationEnum | None = None

    def to_json(self) -> dict:
        if self.region_info is None and self.rotation is None:
            raise ImageOperationMissingRequiredDataError
        data = {"SourceFile": str(self.source_file.resolve())}
        if self.region_info:
            data.update(self.region_info.to_json())
        if self.rotation:
            data.update({"Orientation": self.rotation.value})
        return data
