import argparse
import os
from pathlib import Path

import numpy as np

from myresearch.render import create_wordcloud
from myresearch.wordcount import count
from myresearch.scraper import scrape

import logging

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s')


class ExplicitDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    def _get_help_string(self, action):
        if action.default is None or action.default is False:
            return action.help
        return super()._get_help_string(action)


def run(args):
    words = scrape(name=args.name, query=args.query, limit=args.limit, path=args.path)

    if args.wordcloud is not None:
        create_wordcloud(words, args.wordcloud)
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
