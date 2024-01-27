import os
from pathlib import Path
from typing import Optional

data_path = Path(__file__).parent.parent.parent / "data"
resources = Path(__file__).parent / "resources"
static = Path(__file__).parent / "static"


def filename(url: str):
    return url.split("/")[-1]


def pdf_filename(url: str, path: Optional[Path]):

    if path is not None:
        return path / f"{filename(url)}.pdf"
    else:
        os.makedirs(data_path, exist_ok=True)
        return data_path / f"{filename(url)}.pdf"


def text_filename(url: str, path: Optional[Path]):
    if path is not None:
        return path / f"{filename(url)}.txt"
    else:
        os.makedirs(data_path, exist_ok=True)
        return data_path / f"{filename(url)}.txt"
