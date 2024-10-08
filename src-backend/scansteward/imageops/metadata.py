import logging
import subprocess
import tempfile
from collections import defaultdict
from datetime import UTC
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import orjson as json

from scansteward.imageops.constants import EXIF_TOOL_EXE
from scansteward.imageops.errors import ImagePathNotFileError
from scansteward.imageops.errors import NoImageMetadataError
from scansteward.imageops.errors import NoImagePathsError
from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.models import KeywordInfoModel
from scansteward.imageops.models import KeywordStruct

logger = logging.getLogger(__name__)


def now_string() -> str:
    """
    Formats the current time how exiftool likes to see it
    """
    return datetime.now(tz=UTC).strftime("%Y:%m:%d %H:%M:%S.%fZ")


def process_separated_list(parent: KeywordStruct, remaining: list[str]):
    """
    Given a list of strings, build a tree structure from them, rooted at the given parent

    Example:
        Root|Child|ChildChild
        Root|OtherChild

        becomes

        Root -->
          Child -->
            ChildChild
          OtherChild
    """
    if not remaining:
        # TODO(trenton): Should this set Applied?  Leaf nodes are assumed to be applied
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


def combine_same_keywords(root: KeywordStruct) -> KeywordStruct:
    if not root.Children:
        return root

    # Group children by their "Keyword"
    groups: dict[str, list[KeywordStruct]] = defaultdict(list)
    for child in root.Children:
        groups[child.Keyword].append(child)

    merged_children: list[KeywordStruct] = []
    for keyword in groups:
        nodes = groups[keyword]
        if len(nodes) == 1:
            merged_children.append(combine_same_keywords(nodes[0]))
        else:
            # Merge children of nodes with the same keyword
            merged_node = KeywordStruct(Keyword=keyword)
            all_children = []
            for node in nodes:
                if node.Children:
                    all_children.extend(node.Children)

            if all_children:
                merged_node.Children = all_children
                # Recursively merge the children of the merged node
                merged_children.append(combine_same_keywords(merged_node))
            else:
                merged_children.append(merged_node)

    root.Children = merged_children
    return root


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
        combine_same_keywords(keyword)

    # Assign the parsed flat keywords in as well
    if not keywords:
        return metadata
    if not metadata.KeywordInfo:
        metadata.KeywordInfo = KeywordInfoModel(Hierarchy=keywords)
    else:
        metadata.KeywordInfo.Hierarchy = keywords
    return metadata


def expand_keyword_structures(metadata: ImageMetadata) -> ImageMetadata:
    """
    Expands the KeywordInfo.Hierarchy to also set the HierarchicalSubject, CatalogSets, TagsList and LastKeywordXMP
    """
    if any([metadata.HierarchicalSubject, metadata.CatalogSets, metadata.TagsList, metadata.LastKeywordXMP]):
        logger.warning(f"{metadata.SourceFile.name}: One of the flat tags is set, but will be cleared")

    if not metadata.KeywordInfo:
        return metadata

    for keyword in metadata.KeywordInfo.Hierarchy:
        remove_duplicate_children(keyword)

    def flatten_children(internal_root: KeywordStruct, current_words: list[str]):
        if not internal_root.Children:
            current_words.append(internal_root.Keyword)
        this_child_words = [internal_root.Keyword]
        for internal_child in internal_root.Children:
            flatten_children(internal_child, this_child_words)
            current_words.extend(this_child_words)
            this_child_words = [internal_root.Keyword]

    list_of_lists: list[list[str]] = []

    for root in metadata.KeywordInfo.Hierarchy:
        current_child_words = [root.Keyword]
        for child in root.Children:
            flatten_children(child, current_child_words)
            list_of_lists.append(current_child_words)
            current_child_words = [root.Keyword]

    # Directly overwrite everything
    metadata.HierarchicalSubject = ["|".join(x) for x in list_of_lists]
    metadata.CatalogSets = ["|".join(x) for x in list_of_lists]

    metadata.TagsList = ["/".join(x) for x in list_of_lists]
    metadata.LastKeywordXMP = ["/".join(x) for x in list_of_lists]

    return metadata


def read_image_metadata(
    image_path: Path,
) -> ImageMetadata:
    """
    Reads the requested metadata for a single image file
    """
    return bulk_read_image_metadata([image_path])[0]


def bulk_read_image_metadata(
    images: list[Path],
) -> list[ImageMetadata]:
    """
    Reads the requested metadata for the given list of files.  This does a single subprocess call for
    all images at once, resulting in a more efficient method than looping through
    """

    if not images:
        msg = "No image paths were provided"
        logger.error(msg)
        raise NoImagePathsError(msg)

    cmd = [
        EXIF_TOOL_EXE,
        "-use",
        "MWG",
        "-struct",
        "-json",
        "-n",  # Disable print conversion, use machine readable formats
        "-ImageHeight",
        "-ImageWidth",
        # Face regions
        "-RegionInfo",
        "-MWG:Orientation",
        # Tags
        "-MWG:HierarchicalKeywords",
        "-XMP-microsoft:LastKeywordXMP",
        "-XMP-digiKam:TagsList",
        "-XMP-lr:HierarchicalSubject",
        "-XMP-mediapro:CatalogSets",
        # Other
        "-MWG:Description",
        "-Title",
        # Location
        "-MWG:Country",
        "-MWG:State",
        "-MWG:City",
        "-MWG:Location",
    ]

    # Add the actual images
    for image_path in images:
        if not image_path.exists():
            msg = f"{image_path} does not exist"
            logger.error(msg)
            raise FileNotFoundError(image_path)
        if not image_path.is_file():
            msg = f"{image_path} is not a file"
            logger.error(msg)
            raise ImagePathNotFileError(msg)
        cmd.append(str(image_path.resolve()))

    # And run the command
    logger.debug(f"Running command '{' '.join(cmd)}'")
    proc = subprocess.run(cmd, check=False, capture_output=True)
    if proc.returncode != 0:
        for line in proc.stderr.decode("utf-8").splitlines():
            logger.error(f"exiftool: {line}")
        for line in proc.stdout.decode("utf-8").splitlines():
            logger.info(f"exiftool : {line}")

    # Do this after logging anything
    proc.check_returncode()
    return [
        combine_keyword_structures(y)
        for y in [ImageMetadata.model_validate(x) for x in json.loads(proc.stdout.decode("utf-8"))]
    ]


def write_image_metadata(metadata: ImageMetadata, *, clear_existing_metadata: bool = False) -> None:
    """
    Updates the given SourceFile with the given metadata.  If a field has not been set,
    there will be no change to it.
    """
    return bulk_write_image_metadata([metadata], clear_existing_metadata=clear_existing_metadata)


def bulk_write_image_metadata(
    metadata: list[ImageMetadata],
    *,
    clear_existing_metadata: bool = False,
) -> None:
    """
    Updates the given SourceFiles with the given metadata.  If a field has not been set,
    there will be no change to it.
    This does a single subprocess call, resulting is faster execution than looping
    """
    if not metadata:
        msg = "No image paths were provided"
        logger.error(msg)
        raise NoImageMetadataError(msg)

    if clear_existing_metadata:
        bulk_clear_existing_metadata([x.SourceFile for x in metadata])

    with tempfile.TemporaryDirectory() as json_dir:
        json_path = Path(json_dir).resolve() / "temp.json"
        data = [expand_keyword_structures(x).model_dump(exclude_none=True, exclude_unset=True) for x in metadata]

        json_path.write_bytes(json.dumps(data))
        cmd = [
            EXIF_TOOL_EXE,
            "-use",
            "MWG",
            "-struct",
            "-n",  # Disable print conversion, use machine readable
            "-overwrite_original",
            f"-MWG:ModifyDate={now_string()}",
            "-writeMode",
            "wcg",  # Create new tags/groups as necessary, overwrite existing
            f"-json={json_path}",
        ]
        # * unpacking doesn't resolve for the command?
        for x in metadata:
            cmd.append(str(x.SourceFile.resolve()))  # noqa: PERF401
        logger.debug(f"Running command '{' '.join(cmd)}'")
        proc = subprocess.run(cmd, check=False, capture_output=True)

    for line in proc.stderr.decode("utf-8").splitlines():
        logger.debug(f"exiftool stderr: {line}")
    for line in proc.stdout.decode("utf-8").splitlines():
        logger.debug(f"exiftool stdout: {line}")

        proc.check_returncode()


def clear_existing_metadata(image: Path) -> None:
    return bulk_clear_existing_metadata([image])


def bulk_clear_existing_metadata(images: list[Path]) -> None:
    logger.debug("Clearing existing metadata")
    cmd = [
        EXIF_TOOL_EXE,
        "-overwrite_original",
        "-use",
        "MWG",
        "-v1",
        # Face regions
        "-XMP-mwg-rs:RegionInfo=",
        # Obvious
        "-MWG:Orientation=",
        # Tags
        "-XMP-mwg-kw:KeywordInfo=",
        "-XMP-acdsee:Categories=",
        "-HierarchicalKeywords=",
        "-XMP-microsoft:LastKeywordXMP=",
        "-XMP-digiKam:TagsList=",
        "-XMP-lr:HierarchicalSubject=",
        "-XMP-mediapro:CatalogSets=",
        # Other metadata
        "-Title=",
        "-MWG:Description=",
        "-XMP-dc:Description=",
        "-EXIF:ImageDescription=",
        "-IPTC:Caption-Abstract=",
        "-XMP-dc:Description-x-default=",
        "-IFD0:ImageDescription=",
        "-IPTC:Caption-Abstract=",
    ]
    for image in images:
        cmd.append(str(image.resolve()))  # noqa: PERF401

    logger.debug(f"Running command '{' '.join(cmd)}'")
    proc = subprocess.run(cmd, check=False, capture_output=True)

    for line in proc.stderr.decode("utf-8").splitlines():
        logger.debug(f"exiftool stderr: {line}")
    for line in proc.stdout.decode("utf-8").splitlines():
        logger.debug(f"exiftool stdout: {line}")

    # Do this after logging anything
    proc.check_returncode()
