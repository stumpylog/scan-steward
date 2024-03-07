import logging
import subprocess
from pathlib import Path

from scansteward.imageops.constants import EXIF_TOOL_EXE
from scansteward.imageops.metadata import bulk_read_image_metadata
from scansteward.imageops.metadata import bulk_write_image_metadata
from scansteward.imageops.metadata import write_image_metadata
from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.models import KeywordInfoModel
from scansteward.imageops.models import KeywordStruct

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

    def flatten_children(root: KeywordStruct, current_words: list) -> list[str]:
        if not root.Children:
            return current_words
        for child in root.Children:
            current_words.append(child.Keyword)
            flatten_children(child, current_words)
        return current_words

    for root in metadata.KeywordInfo.Hierarchy:
        this_branch_words = [root.Keyword]
        flatten_children(root, this_branch_words)
        list_of_lists.append(this_branch_words)

    # Directly overwrite everything
    metadata.HierarchicalSubject = ["|".join(x) for x in list_of_lists]
    metadata.CatalogSets = metadata.HierarchicalSubject
    metadata.TagsList = ["/".join(x) for x in list_of_lists]
    metadata.LastKeywordXMP = metadata.TagsList

    for keyword in metadata.KeywordInfo.Hierarchy:
        remove_duplicate_children(keyword)

    return metadata


def read_keywords(image_path: Path) -> ImageMetadata:
    return bulk_read_keywords([image_path])[0]


def bulk_read_keywords(images: list[Path]) -> list[ImageMetadata]:
    return [combine_keyword_structures(x) for x in bulk_read_image_metadata(images, read_tags=True)]


def bulk_clear_existing_keywords(images: list[Path]) -> None:
    cmd = [
        EXIF_TOOL_EXE,
        "-struct",
        "-json",
        "-n",  # Disable print conversion, use machine readable
        "-HierarchicalKeywords=",
        "-LastKeywordXMP=",
        "-TagsList=",
        "-HierarchicalSubject=",
        "-CatalogSets=",
    ]
    for image in images:
        cmd.append(str(image.resolve()))
    proc = subprocess.run(cmd, check=False, capture_output=True)
    if proc.returncode != 0:
        for line in proc.stderr.decode("utf-8").splitlines():
            logger.error(f"exiftool: {line}")
    for line in proc.stdout.decode("utf-8").splitlines():
        logger.info(f"exiftool : {line}")

    # Do this after logging anything
    proc.check_returncode()


def write_keywords(metadata: ImageMetadata, *, clear_existing: bool = False) -> None:
    if clear_existing:
        bulk_clear_existing_keywords([metadata.SourceFile])
    return write_image_metadata(expand_keyword_structures(metadata))


def bulk_write_image_keywords(metadata: list[ImageMetadata], *, clear_existing: bool = False) -> None:
    if clear_existing:
        bulk_clear_existing_keywords([x.SourceFile for x in metadata])
    return bulk_write_image_metadata(metadata)
