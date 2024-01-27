import argparse
import io
import os
import time
from pathlib import Path

import numpy as np

from myresearch.paths import data_path

from matplotlib import pyplot as plt

from myresearch.render import create_wordcloud
from myresearch.wordcount import count
from myresearch.scraper import Scraper
from tqdm.auto import tqdm
from logging import Logger

import logging

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s')

logger = logging.getLogger(__name__)


class ExplicitDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    def _get_help_string(self, action):
        if action.default is None or action.default is False:
            return action.help
        return super()._get_help_string(action)


def custom_function(custom_logger: Logger = None):
    logger = custom_logger or logging.getLogger(__name__)

    for i in tqdm(range(10), desc='Progress'):
        # Your processing logic here
        time.sleep(0.5)
        # Send progress to the client using WebSocket
        logger.info(f'Processing step {i}')
    logger.info("Custom function completed")

    f = io.BytesIO()
    a = np.random.rand(10)
    plt.bar(range(len(a)), a)
    plt.savefig(f, format="svg")

    result = f.getvalue().decode('utf-8')  # svg string
    return result


def web_runner(kwargs, custom_logger: Logger = None):
    """
    Wrapper to run the tool in a web server. Using custom_logger will redirect logs to a temporary output window
    :param custom_logger:
    :return:
    """
    logger = custom_logger or logging.getLogger(__name__)

    if kwargs["query"] == "":
        kwargs["query"] = None
    if kwargs["name"] == "":
        kwargs["name"] = None
    if kwargs["limit"] is not None:
        kwargs["limit"] = int(kwargs["limit"])
    # if kwargs["width"] is not None:
    #     kwargs["width"] = int(kwargs["width"])
    # if kwargs["height"] is not None:
    #     kwargs["height"] = int(kwargs["height"])

    kwargs["path"] = data_path

    scraper = Scraper(logger=logger)
    words = scraper.scrape(**kwargs)

    wc = create_wordcloud(text=words, filename=None, width=800, height=400)
    return wc


def run(args):
    scraper = Scraper()
    words = scraper.scrape(name=args.name, query=args.query, limit=args.limit, path=args.path)

    if args.wordcloud is not None:
        create_wordcloud(text=words, filename=args.wordcloud)
    if args.wordcount is not None:
        count(words).to_csv(args.wordcount)


def main():
    parser = argparse.ArgumentParser(description="A tool to scrape and summarize a your research papers",
                                     formatter_class=ExplicitDefaultsHelpFormatter)

    exgroup = parser.add_argument_group(title='One of these arguments are required, but not both')
    group = exgroup.add_mutually_exclusive_group(required=True)
    group.add_argument('--name', help='Search name', action='store')
    group.add_argument('--query', help='Full query string', action='store')

    parser.add_argument('--limit', type=int, help="Maximum number of papers to use", action='store', default=np.inf)
    parser.add_argument('--path', type=str, help="Path to use for storage", action='store',
                        default=Path(os.getcwd()) / "data/")
    parser.add_argument('--wordcount', help='destination file for wordcount', action='store', default=None)
    parser.add_argument('--wordcloud',
                        type=Path,
                        help='destination file for word cloud. Format is inferred from the extension '
                             '(png is recommended)',
                        action='store',
                        default=None)

    # Parse the arguments and execute the corresponding command
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
