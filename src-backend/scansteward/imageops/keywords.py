import subprocess
import tempfile
from pathlib import Path

import orjson as json
from imageops.models import HierarchicalSubject

from scansteward.imageops.constants import EXIF_TOOL_EXE


def read_keywords(image_path: Path) -> list[HierarchicalSubject]:
    proc = subprocess.run(
        [
            EXIF_TOOL_EXE,  # type: ignore
            "-struct",
            "-json",
            "-xmp:all",
            "-n",  # Disable print conversion, use machine readable
            str(image_path.resolve()),
        ],
        check=True,
        capture_output=True,
    )
    data = json.loads(proc.stdout.decode("utf-8"))[0]
    if "HierarchicalSubject" not in data:
        return []

    def process(parent: HierarchicalSubject, remaining: list[str]):
        if not remaining:
            return
        new_parent = HierarchicalSubject(remaining[0], parent=parent)
        parent.children.append(new_parent)
        process(new_parent, remaining[1:])

    roots: dict[str, HierarchicalSubject] = {}
    for line in data["HierarchicalSubject"]:
        values_list = line.split("|")
        root_value = values_list[0]
        if root_value not in roots:
            roots[root_value] = HierarchicalSubject(values_list[0])
        root = roots[root_value]
        process(root, values_list[1:])

    return list(roots.values())


def set_keywords(image_path: Path, keywords: list[HierarchicalSubject]) -> None:

    keywords_list = []

    def listbuilder(sub_tree: HierarchicalSubject, current_list: list[str]):
        if not sub_tree.children:
            keywords_list.append([*current_list, sub_tree.value])
        for child in sub_tree.children:
            listbuilder(child, [*current_list, sub_tree.value])

    for root_keyword in keywords:
        listbuilder(root_keyword, [])

    with tempfile.TemporaryDirectory() as json_dir:
        json_path = Path(json_dir).resolve() / "temp.json"
        json_path.write_bytes(
            json.dumps([{"SourceFile": str(image_path.resolve()), "HierarchicalSubject": keywords_list}]),
        )
        subprocess.run(
            [
                EXIF_TOOL_EXE,  # type: ignore
                "-overwrite_original",
                "-XMP:MetadataDate=now",
                "-n",  # Disable print conversion, use machine readable
                "-writeMode",
                "wcg",  # Create new tags/groups as necessary
                f"-json={json_path}",
                str(image_path.resolve()),
            ],
            check=False,
        )
