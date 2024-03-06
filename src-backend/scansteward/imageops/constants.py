from __future__ import annotations

import shutil
from typing import TYPE_CHECKING

EXIF_TOOL_EXE = shutil.which("exiftool")
if TYPE_CHECKING:
    assert EXIF_TOOL_EXE is not None
