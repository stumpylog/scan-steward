import subprocess
from pathlib import Path

import orjson as json

from scansteward.imageops.constants import EXIF_TOOL_EXE
from scansteward.imageops.types import HierarchicalSubject


def read_keywords(image_path: Path) -> list[HierarchicalSubject]:
    proc = subprocess.run(
        [  # noqa: S603
            EXIF_TOOL_EXE,  # type: ignore
            "-struct",
            "-json",
            "-xmp:all",
            "-n",  # Disable print conversion, use machine readable
            "-Orientation",
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

    root = HierarchicalSubject("root")
    for line in data["HierarchicalSubject"]:
        values_list = line.split("|")
        process(root, values_list[1:])

    # Remove the sneaky root
    for actual_root in root.children:
        actual_root.parent = None

    return root.children
