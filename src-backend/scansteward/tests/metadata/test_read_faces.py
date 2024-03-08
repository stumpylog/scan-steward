import shutil
from pathlib import Path

from scansteward.imageops.faces import bulk_read_faces
from scansteward.imageops.faces import bulk_write_faces
from scansteward.imageops.faces import read_faces
from scansteward.imageops.faces import write_faces
from scansteward.imageops.models import DimensionsStruct
from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.models import RegionInfoStruct
from scansteward.imageops.models import RegionStruct
from scansteward.imageops.models import XmpAreaStruct

SAMPLE_ONE_DIMENSIONS = DimensionsStruct(H=683.0, W=1024.0, Unit="pixel")

SAMPLE_ONE_REGION = RegionStruct(
    Area=XmpAreaStruct(H=0.0585652, W=0.0292969, X=0.317383, Y=0.303075, Unit="normalized", D=None),
    Name="Barack Obama",
    Type="Face",
    Description=None,
)

SAMPLE_TWO_DIMENSIONS = DimensionsStruct(H=2333.0, W=3500.0, Unit="pixel")

SAMPLE_TWO_REGION = RegionStruct(
    Area=XmpAreaStruct(H=0.216459, W=0.129714, X=0.492857, Y=0.277968, Unit="normalized", D=None),
    Name="Barack Obama",
    Type="Face",
    Description=None,
)

SAMPLES_DIMENSIONS = [SAMPLE_ONE_DIMENSIONS, SAMPLE_TWO_DIMENSIONS]
SAMPLES_REGIONS = [SAMPLE_ONE_REGION, SAMPLE_TWO_REGION]


class TestReadImageFaces:

    def test_read_image_with_faces(self, sample_one_jpeg: Path):

        metadata = read_faces(sample_one_jpeg)

        assert metadata.SourceFile == sample_one_jpeg
        assert metadata.RegionInfo is not None
        # Check the dimensions of the image are read correctly
        assert metadata.RegionInfo.AppliedToDimensions == SAMPLE_ONE_DIMENSIONS
        assert len(metadata.RegionInfo.RegionList) == 1

        region = metadata.RegionInfo.RegionList[0]

        assert region == SAMPLE_ONE_REGION

    def test_bulk_read_image_faces(self, sample_one_jpeg: Path, sample_two_jpeg):
        img_paths = [sample_one_jpeg, sample_two_jpeg]

        metadata = bulk_read_faces(img_paths)

        assert len(metadata) == 2

        for metadata_item, expected in zip(metadata, [sample_one_jpeg, sample_two_jpeg], strict=False):
            assert metadata_item.SourceFile == expected

        for metadata_item, expected in zip(metadata, SAMPLES_DIMENSIONS, strict=False):
            assert metadata_item.RegionInfo is not None
            assert metadata_item.RegionInfo.AppliedToDimensions == expected

        for metadata_item, expected in zip(metadata, SAMPLES_REGIONS, strict=False):
            assert metadata_item.RegionInfo is not None
            assert len(metadata_item.RegionInfo.RegionList) == 1
            assert metadata_item.RegionInfo.RegionList[0] == expected


class TestWriteImageFaces:
    def test_write_image_face(self, temporary_directory: Path, sample_one_jpeg: Path):

        result = Path(shutil.copy(sample_one_jpeg, temporary_directory / sample_one_jpeg.name))

        new_region = SAMPLE_ONE_REGION.model_copy()
        new_region.Name = "Billy Bob"

        metadata = ImageMetadata(
            SourceFile=result,
            RegionInfo=RegionInfoStruct(AppliedToDimensions=SAMPLE_ONE_DIMENSIONS, RegionList=[new_region]),
        )

        write_faces(metadata)

        changed_metadata = read_faces(result)

        assert changed_metadata.SourceFile == result
        assert changed_metadata.RegionInfo is not None
        # Check the dimensions of the image are read correctly
        assert changed_metadata.RegionInfo.AppliedToDimensions == SAMPLE_ONE_DIMENSIONS
        assert len(changed_metadata.RegionInfo.RegionList) == 1

        region = changed_metadata.RegionInfo.RegionList[0]

        assert region == new_region

    def test_bulk_write_faces(self, temporary_directory: Path, sample_one_jpeg: Path):

        result = Path(shutil.copy(sample_one_jpeg, temporary_directory / sample_one_jpeg.name))

        new_region = SAMPLE_ONE_REGION.model_copy()
        new_region.Name = "Billy Bob"

        metadata = ImageMetadata(
            SourceFile=result,
            RegionInfo=RegionInfoStruct(AppliedToDimensions=SAMPLE_ONE_DIMENSIONS, RegionList=[new_region]),
        )

        bulk_write_faces([metadata])

        changed_metadata = read_faces(result)

        assert changed_metadata.SourceFile == result
        assert changed_metadata.RegionInfo is not None
        # Check the dimensions of the image are read correctly
        assert changed_metadata.RegionInfo.AppliedToDimensions == SAMPLE_ONE_DIMENSIONS
        assert len(changed_metadata.RegionInfo.RegionList) == 1

        region = changed_metadata.RegionInfo.RegionList[0]

        assert region == new_region
