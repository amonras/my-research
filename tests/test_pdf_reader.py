from pytest import fixture

from myresearch.scraper import Scraper, get_pdf_content


@fixture
def scraper():
    scraper = Scraper()
    yield scraper


class TestPdfReader:
    def test_reader(self, scraper, random_pdf):
        text = get_pdf_content(random_pdf)

        assert "quantum" in text
        assert "machine" in text
        assert "learning" in text

    def test_pdf_text_extraction_no_ligatures(self, random_pdf):
        text = get_pdf_content(random_pdf)

        # List of common ligatures to check for
        ligatures = [#'fi', 'fl', 'ff', 'ffi', 'ffl',
                     'ﬁ']

        for ligature in ligatures:
            assert ligature not in text, f"Ligature '{ligature}' found in extracted text"

    def test_no_newlines_escapes(self, random_pdf):
        text = get_pdf_content(random_pdf)

        for word in text.split(" "):
            assert "\n" not in word
