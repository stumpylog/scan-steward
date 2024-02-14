from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass(frozen=True)
class XmpAreaStruct:
    """
    https://exiftool.org/TagNames/XMP.html#Area
    """

    d: float
    h: float
    unit: str
    w: float
    x: float
    y: float


@dataclass(frozen=True)
class DimensionsStruct:
    """
    https://exiftool.org/TagNames/XMP.html#Dimensions
    """

    H: float
    unit: str
    W: float


@dataclass(frozen=True)
class RegionStruct:
    """
    https://exiftool.org/TagNames/MWG.html#RegionStruct
    """

    Area: XmpAreaStruct
    Description: str
    Name: str
    Type: Literal["BarCode", "Face", "Focus", "Pet"]


@dataclass(frozen=True)
class RegionInfoStruct:
    """
    https://exiftool.org/TagNames/MWG.html#RegionInfo
    """

    AppliedToDimensions: DimensionsStruct
    RegionList: list[RegionStruct]

    @staticmethod
    def from_json() -> RegionInfoStruct:
        raise NotImplementedError

    def to_json(self) -> TODO:
        raise NotImplementedError


def read_face_structs(image_path: Path) -> list[RegionInfoStruct]:
    raise NotImplementedError


def write_face_structs(image_path: Path, structs: list[RegionInfoStruct]) -> None:
    raise NotImplementedError
