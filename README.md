# README

scan-steward is a tool to help you sort, categorize, and generally assist with making sense of a bunch of old images.s

## Inspiration

This project was born out of another project I embarked on in late 2023, the scanning of thousands of slides from my
parents' and grandparents' trips and life. As I accumulated more and more images, with pictures of my family, as well
as pictures of other things, I found it hard to keep track of what images a particular person showed up in. Then I
wanted to know where the picture was taken, roughly what it was about, an idea of the year and finally to know any
important memories attached to the image.

Existing photo album type software didn't have the features I wanted. Captions were too basic, searching didn't allow
combinations of people and location or required highly specific location and time information. And so, this project was
born with the goal to assist one or more family members in sorting out all that information.

It allows one or more users (probably other family members) to view, sort, categorize, tag and add memories scans of old photographs,
slides, etc and then share with more users to view, remember and enjoy a little bit of history no one might have ever seen before.

## Features

- Create and manage people and descriptions of them using Markdown formatted for rich text descriptions
- Add images to rough locations, letting you go from general ("Georgia") to specific ("Atlanta") to really specific ("Coke Headquarters")
- Add a rough date to images, so even if you only know the year, you can still filter to those images
- Add images into multiple albums, each with distinct sort ordering, so you can sort trip images differently than the images of Grandma

## Roadmap

- View, add, edit and delete boxes for faces and pets in images
- Sync the database into the image file, using [Metadata Working Group](https://en.wikipedia.org/wiki/Metadata_Working_Group) standard tags
  - Including region boxes, tags, rough location and rough dates
- Text based searching over description and captions
- Filter on images containing any people or all people

## Installation

Installation is via Docker.

## Usage

## Contributing

## Built On

## Links

- <https://exiftool.org/struct.html>
- <https://exiftool.org/TagNames/MWG.html>

## Code

### Batched Updates with exiftool

```python
import shutil
import subprocess
import orjson as json
from pathlib import Path
import tempfile

if __name__ == "__main__":
    test_file1 = Path("test.jpg").resolve()
    test_file2 = Path("another_test.jpg").resolve()
    data = [
        {
            "SourceFile": str(test_file1),
            "RegionInfo": {
                "AppliedToDimensions": {"W": 4288, "H": 2847, "Unit": "pixel"},
                "RegionList": [
                    {
                        "Area": {"H": 1, "W": 2, "X": 4, "Y": 4, "Unit": "normalized"},
                        "Name": "This is Me",
                        "Type": "Face",
                    }
                ],
            },
        },
        {
            "SourceFile": str(test_file2),
            "RegionInfo": {
                "AppliedToDimensions": {"W": 4288, "H": 2847, "Unit": "pixel"},
                "RegionList": [
                    {
                        "Area": {"H": 1, "W": 2, "X": 4, "Y": 4, "Unit": "normalized"},
                        "Name": "This is Another Me Batched",
                        "Type": "Face",
                    }
                ],
            },
        },
    ]

    tool = shutil.which("exiftool")
    assert tool is not None

    with tempfile.TemporaryDirectory() as json_dir:
        json_path = Path(json_dir)  / "temp.json"
        json_path.write_bytes(json.dumps(data))
        subprocess.run(
            [tool, "-overwrite_original", "-XMP:MetadataDate=now", "-wm", "cg", f"-json={json_path}", test_file1, test_file2]
        )


```
