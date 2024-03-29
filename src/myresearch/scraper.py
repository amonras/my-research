import logging
import os
import re
from pathlib import Path
from typing import Optional

import bs4
import numpy as np
import requests
from fitz import fitz, TEXT_DEHYPHENATE

from myresearch.paths import text_filename, pdf_filename
from myresearch.pdf_reader import filter_words, ignore

basic_logger = logging.getLogger(__name__)
basic_logger.setLevel(logging.DEBUG)


def get_links(text):
    """
    Given an html body, return the list of links to PDF papers
    :param text:
    :return:
    """
    soup = bs4.BeautifulSoup(text, "lxml")
    links = [
        span.find('a', string='pdf')['href']
        for span in soup.select('p.list-title.is-inline-block span')
        if span.find('a', string='pdf')
    ]

    return links


def get_pdf_content(filename):
    """
    Given a PDF object, extract the text contents
    :param filename:
    :return:
    """
    with open(filename, 'rb') as pdf_file:
        doc = fitz.open(filename)  # open a document
        full_text = []
        for page in doc:  # iterate the document pages
            text = page.get_text("words", flags=TEXT_DEHYPHENATE)
            full_text.extend([w[4] for w in text])  # write text of page

    return " ".join(full_text)


def get_search_url(name: str):
    return f"https://arxiv.org/search/?query={name}&searchtype=all&source=header"


class Scraper:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def download_and_read_pdf(self, pdf_url, path):
        self.logger.debug(f"Getting {pdf_url}")
        filename = pdf_filename(pdf_url, path)
        try:
            # Download the PDF file
            self.logger.info(f"Querying {pdf_url}")
            response = requests.get(pdf_url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Save the PDF content to the temporary file
                with open(filename, "wb") as pdf_file:
                    pdf_file.write(response.content)
            else:
                self.logger.error(f"Failed to download PDF. Status Code: {response.status_code}")
                return None
        finally:
            # Load the PDF into a PdfReader instance
            text = get_pdf_content(filename)
            return text

    def get_links_from_page(self, url, limit: Optional[int] = None):
        """
        Retrieve list of papers in url
        :param url:
        :param limit:
        :return:
        """
        self.logger.debug(f"Retrieving list of links from {url}")
        limit = limit or np.Inf

        response = requests.get(url)
        if response.status_code == 200:
            links = get_links(response.text)
            if len(links) > limit:
                links = links[:limit]
            return links
        else:
            self.logger.error(f"Response {response.status_code}")
            return None

    def scrape(
            self,
            name: Optional[str] = None,
            query: Optional[str] = None,
            path: Optional[Path] = None,
            limit: Optional[int] = None,
            **kwargs
    ):
        """
        Scrape arXiv page and retrieve its papers
        """
        if query is None:
            # Get the main url query from the name
            query = get_search_url(name)
        links = self.get_links_from_page(query, limit=limit)

        texts = []

        for link in links:
            filename = text_filename(link, path)
            if os.path.exists(filename):
                self.logger.debug(f"File {filename} already exists. Skipping download.")
                continue
            with open(filename, "w") as f:
                f.write(self.download_and_read_pdf(link, path))

        for link in links:
            filename = text_filename(link, path)
            with open(filename, "r") as f:
                text = re.split(r"[, \-!?:]+", f.read())
                texts.extend(text)

        words = [word.lower() for word in filter_words(texts, callable_ignore=ignore)]

        return words


if __name__ == "__main__":
    scraper = Scraper()
    scraper.scrape(name="monras")
