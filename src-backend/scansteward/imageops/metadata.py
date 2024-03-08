import logging
import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import orjson as json

from scansteward.imageops.constants import EXIF_TOOL_EXE
from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.models import KeywordInfoModel
from scansteward.imageops.models import KeywordStruct
from scansteward.imageops.utils import now_string

logger = logging.getLogger(__name__)


def process_separated_list(parent: KeywordStruct, remaining: list[str]):
    """
    Given a list of strings, build a tree structure from them, rooted at the given parent
    """
    if not remaining:
        return
    new_parent = KeywordStruct(Keyword=remaining[0])

    parent.Children.append(new_parent)
    process_separated_list(new_parent, remaining[1:])


def remove_duplicate_children(root: KeywordStruct):
    """
    Removes duplicated children, which may exist as multiple fields above contain the same data
    """
    if not root.Children:
        return
    for child in root.Children:
        remove_duplicate_children(child)
    root.Children = list(set(root.Children))


def combine_keyword_structures(metadata: ImageMetadata) -> ImageMetadata:
    """
    Reads the various other possible keyword values, and generates a tree from them,
    then combines with anything existing and removes duplicates
    """
    keywords: list[KeywordStruct] = []

    if metadata.KeywordInfo and metadata.KeywordInfo.Hierarchy:
        keywords.extend(metadata.KeywordInfo.Hierarchy)

    # Check for other keywords which might get set as a flat structure
    # Parse them into KeywordStruct trees
    roots: dict[str, KeywordStruct] = {}
    for key, separation in [
        (metadata.HierarchicalSubject, "|"),
        (metadata.CatalogSets, "|"),
        (metadata.TagsList, "/"),
        (metadata.LastKeywordXMP, "/"),
    ]:
        if not key:
            continue
        for line in key:
            if TYPE_CHECKING:
                assert isinstance(line, str)
            values_list = line.split(separation)
            root_value = values_list[0]
            if root_value not in roots:
                roots[root_value] = KeywordStruct(Keyword=values_list[0])
            root = roots[root_value]
            process_separated_list(root, values_list[1:])

    keywords.extend(list(roots.values()))

    for keyword in keywords:
        remove_duplicate_children(keyword)

    # Assign the parsed flat keywords in as well
    if not metadata.KeywordInfo:
        metadata.KeywordInfo = KeywordInfoModel(Hierarchy=keywords)
    else:
        metadata.KeywordInfo.Hierarchy = keywords
    return metadata


def expand_keyword_structures(metadata: ImageMetadata) -> ImageMetadata:
    """
    Expands the KeywordInfo.Hierarchy to also set the HierarchicalSubject, CatalogSets, TagsList and LastKeywordXMP
    """
    if any([metadata.HierarchicalSubject, metadata.TagsList, metadata.LastKeywordXMP]):
        logger.warn(f"{metadata.SourceFile.name}: One of the flat tags is set, but will be cleared")
    list_of_lists: list[list[str]] = []

    if not metadata.KeywordInfo:
        return metadata

    def flatten_children(internal_root: KeywordStruct, current_words: list):
        if not internal_root.Children:
            current_words.append(internal_root.Keyword)
        this_child_words = [internal_root.Keyword]
        for internal_child in internal_root.Children:
            flatten_children(internal_child, this_child_words)
            current_words.extend(this_child_words)
            this_child_words = [internal_root.Keyword]

    for root in metadata.KeywordInfo.Hierarchy:
        current_child_words = [root.Keyword]
        for child in root.Children:
            flatten_children(child, current_child_words)
            list_of_lists.append(current_child_words)
            current_child_words = [root.Keyword]

    # Directly overwrite everything
    metadata.HierarchicalSubject = ["|".join(x) for x in list_of_lists]
    metadata.CatalogSets = metadata.HierarchicalSubject
    metadata.TagsList = ["/".join(x) for x in list_of_lists]
    metadata.LastKeywordXMP = metadata.TagsList

    for keyword in metadata.KeywordInfo.Hierarchy:
        remove_duplicate_children(keyword)

    return metadata


def read_image_metadata(
    image_path: Path,
    *,
    read_regions: bool = False,
    read_orientation: bool = False,
    read_tags: bool = False,
    read_title: bool = False,
    read_description: bool = False,
) -> ImageMetadata:
    """
    Reads the requested metadata for a single image file
    """
    return bulk_read_image_metadata(
        [image_path],
        read_regions=read_regions,
        read_orientation=read_orientation,
        read_tags=read_tags,
        read_title=read_title,
        read_description=read_description,
    )[0]


def bulk_read_image_metadata(
    images: list[Path],
    *,
    read_regions: bool = False,
    read_orientation: bool = False,
    read_tags: bool = False,
    read_title: bool = False,
    read_description: bool = False,
) -> list[ImageMetadata]:
    """
    Reads the requested metadata for the given list of files.  This does a single subprocess call for
    all images at once, resulting in a more efficient method than looping through
    """

    # Something must be asked for
    if not any([read_regions, read_orientation, read_tags, read_title, read_description]):
        msg = "One of read_* is required but not provided"
        logger.error(msg)
        raise ValueError(msg)
    if not images:
        msg = "No image paths were provided"
        logger.error(msg)
        raise ValueError(msg)

    actual_images = []
    for image_path in images:
        if not image_path.exists():
            msg = f"{image_path} does not exist"
            logger.error(msg)
            raise FileExistsError(image_path)
        elif not image_path.is_file():
            msg = f"{image_path} is not a file"
            logger.error(msg)
            raise ValueError(msg)
        actual_images.append(image_path.resolve())

    cmd = [
        EXIF_TOOL_EXE,
        "-struct",
        "-json",
        "-n",  # Disable print conversion, use machine readable
    ]
    # Add the request for the requested flags
    if read_regions:
        cmd.append("-RegionInfo")
    if read_orientation:
        cmd.append("-Orientation")
    if read_tags:
        cmd.extend(
            ["-HierarchicalKeywords", "-LastKeywordXMP", "-TagsList", "-HierarchicalSubject", "-CatalogSets"],
        )
    if read_title:
        cmd.append("-Title")
    if read_description:
        cmd.append("-Description")
    # Add the actual images
    cmd.extend(actual_images)

    # And run the command
    logger.debug(f"Running commend '{cmd}'")
    proc = subprocess.run(cmd, check=False, capture_output=True)
    if proc.returncode != 0:
        for line in proc.stderr.decode("utf-8").splitlines():
            logger.error(f"exiftool: {line}")
        for line in proc.stdout.decode("utf-8").splitlines():
            logger.info(f"exiftool : {line}")

    # Do this after logging anything
    proc.check_returncode()
    all_metadata = [ImageMetadata.model_validate(x) for x in json.loads(proc.stdout.decode("utf-8"))]
    if read_tags:
        return [combine_keyword_structures(x) for x in all_metadata]
    return all_metadata


def write_image_metadata(metadata: ImageMetadata) -> None:
    """
    Updates the given SourceFile with the given metadata.  If a field has not been set,
    there will be no change to it.
    """
    return bulk_write_image_metadata([metadata])


def bulk_write_image_metadata(metadata: list[ImageMetadata]) -> None:
    """
    Updates the given SourceFiles with the given metadata.  If a field has not been set,
    there will be no change to it.
    This does a single subprocess call, resulting is faster execution than looping
    """
    with tempfile.TemporaryDirectory() as json_dir:
        json_path = Path(json_dir).resolve() / "temp.json"
        data = [
            expand_keyword_structures(x).model_dump(exclude_none=True, exclude_unset=True) for x in metadata
        ]
        json_path.write_bytes(json.dumps(data))
        cmd = [
            EXIF_TOOL_EXE,
            "-struct",
            "-n",  # Disable print conversion, use machine readable
            "-overwrite_original",
            f"-ModifyDate={now_string()}",
            "-writeMode",
            "wcg",  # Create new tags/groups as necessary, overwrite existing
            f"-json={json_path}",
        ]
        # * unpacking doesn't resolve for the command
        for x in metadata:
            cmd.append(x.SourceFile.resolve())  # noqa: PERF401
        proc = subprocess.run(cmd, check=False, capture_output=True)

        if proc.returncode != 0:
            for line in proc.stderr.decode("utf-8").splitlines():
                logger.error(f"exiftool: {line}")
            for line in proc.stdout.decode("utf-8").splitlines():
                logger.info(f"exiftool : {line}")

        proc.check_returncode()
