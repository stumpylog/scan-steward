from __future__ import annotations

import orjson as json
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Literal

EXIF_TOOL_EXE = shutil.which("exiftool")
if TYPE_CHECKING:
    assert EXIF_TOOL_EXE is not None


@dataclass(frozen=True)
class XmpAreaStruct:
    """
    https://exiftool.org/TagNames/XMP.html#Area
    """

    d: float
    h: float
    unit: Literal["normalized"]
    w: float
    x: float
    y: float

    def to_json(self) -> dict:
        return {"H": self.h, "W": self.w, "X": self.x, "Y": self.y, "Unit": self.unit},


@dataclass(frozen=True)
class DimensionsStruct:
    """
    https://exiftool.org/TagNames/XMP.html#Dimensions
    """

    H: float
    W: float
    unit: Literal["pixel", "inch"]

    def to_json(self) -> dict:
        return {"W": self.W, "H": self.H, "Unit": self.unit}


@dataclass(frozen=True)
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

    def to_json(self) -> dict:
        return {
            "AppliedToDimensions": self.AppliedToDimensions.to_json(),
            "RegionList": [x.to_json() for x in self.RegionList],
        }


class ImageMetadata:
    source_file: Path
    region_info: RegionInfoStruct

    def to_json(self) -> dict:
        return ({"SourceFile": str(self.source_file.resolve()), "RegionInfo": self.region_info.to_json()},)


def read_face_structs(image_path: Path) -> list[RegionInfoStruct]:
    # exiftool -struct -json -xmp:all "2024-01-22-0006.jpg"
    raise NotImplementedError


def write_face_structs(metadata: ImageMetadata) -> None:
    with tempfile.TemporaryDirectory() as json_dir:
        json_path = Path(json_dir).resolve() / "temp.json"
        json_path.write_bytes(json.dumps(metadata.to_json()))
        subprocess.run(
            [
                EXIF_TOOL_EXE,
                "-overwrite_original",
                "-XMP:MetadataDate=now",
                "-wm",
                "cg",
                f"-json={json_path}",
                str(metadata.source_file.resolve()),
            ],
            check=False,
        )


def bulk_write_face_structs(metadata: list[ImageMetadata]) -> None:
    with tempfile.TemporaryDirectory() as json_dir:
        json_path = Path(json_dir).resolve() / "temp.json"
        data = [x.to_json() for x in metadata]
        img_files = [str(x.source_file.resolve() for x in metadata)]
        json_path.write_bytes(json.dumps(data))
        subprocess.run(
            [
                EXIF_TOOL_EXE,
                "-overwrite_original",
                "-XMP:MetadataDate=now",
                "-wm",
                "cg",
                f"-json={json_path}",
            ] + img_files,
            check=False,
        )
