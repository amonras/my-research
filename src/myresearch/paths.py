import os
from pathlib import Path
from typing import Optional

directory = Path(__file__).parent.parent.parent / "data"
resources = Path(__file__).parent / "resources"
static = Path(__file__).parent / "static"


def filename(url: str):
    return url.split("/")[-1]


def pdf_filename(url: str, path: Optional[Path]):

    if path is not None:
        return path / f"{filename(url)}.pdf"
    else:
        os.makedirs(directory, exist_ok=True)
        return directory / f"{filename(url)}.pdf"


def text_filename(url: str, path: Optional[Path]):
    if path is not None:
        return path / f"{filename(url)}.txt"
    else:
        os.makedirs(directory, exist_ok=True)
        return directory / f"{filename(url)}.txt"
