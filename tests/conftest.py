from pathlib import Path
from pytest import fixture

resources = Path(__file__).parent / "resources"


@fixture
def first_page():
    with open(resources / "first_page.html", "r") as f:
        text = f.read()

    yield text


@fixture
def random_pdf():
    yield resources / '1903.01391.pdf'

