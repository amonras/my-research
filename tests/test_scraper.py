import pytest
from myresearch.scraper import get_links, get_pdf_content


class TestScraper:
    def test_get_links(self, first_page):
        links = get_links(text=first_page)
        assert len(links) > 0
        for link in links:
            assert "pdf" in link
