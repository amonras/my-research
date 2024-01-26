import logging

from myresearch.pdf_reader import stopwords
from myresearch.scraper import scrape
from wordcloud import WordCloud
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def create_wordcloud(text, filename=None):
    # Create and generate a word cloud image:
    wordcloud = WordCloud(width=800, height=400, stopwords=stopwords)
    img = wordcloud.generate(" ".join(text))

    # Display the generated image:
    plt.imshow(img, interpolation='bilinear')
    plt.axis("off")

    if filename is not None:
        plt.savefig(filename, bbox_inches="tight")
        print(f"Wordcloud written to {filename}")
    else:
        plt.show()


if __name__ == "__main__":
    words = scrape("monras")
    create_wordcloud(" ".join(words))
