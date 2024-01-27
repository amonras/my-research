import io
import logging

from myresearch.pdf_reader import stopwords
from wordcloud import WordCloud
import matplotlib

from myresearch.scraper import Scraper

matplotlib.use('Agg')
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def create_wordcloud(text, filename=None, width=800, height=400):
    # Create and generate a word cloud image:
    wordcloud = WordCloud(width=width, height=height, stopwords=stopwords)
    img = wordcloud.generate(" ".join(text))

    # Display the generated image:
    plt.imshow(img, interpolation='bilinear')
    plt.axis("off")

    if filename is not None:
        plt.savefig(filename, bbox_inches="tight")
        print(f"Wordcloud written to {filename}")
        return
    else:
        f = io.BytesIO()
        plt.savefig(f, format="svg", bbox_inches='tight')
        result = f.getvalue().decode('utf-8')  # svg string
        return result


if __name__ == "__main__":
    scraper = Scraper()
    words = scraper.scrape("monras")
    create_wordcloud(" ".join(words))
