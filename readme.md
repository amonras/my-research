# MyResearch web scaper
This tool allows you to download from [arXiv.org](https://arxiv.org/) the body of your research and extract insights about it.

At the moment only word count and wordcloud is available.

```
$ myresearch --help
usage: myresearch [-h] --name NAME [--wordcount WORDCOUNT] [--wordcloud WORDCLOUD]

A tool to scrape and summarize a given research body

options:
  -h, --help            show this help message and exit
  --limit LIMIT         Maximum number of papers to use (default: inf)
  --path PATH           Path to use for storage (default: /Users/amonras/PycharmProjects/my-research/data)
  --wordcount WORDCOUNT
                        destination file for wordcount CSV file
  --wordcloud WORDCLOUD
                        destination file for word cloud. Format is inferred from the extension (png is recommended)

One of these arguments are required, but not both:
  --name NAME           Search name
  --query QUERY         Full query string
```

so for example
```bash
$ myresearch --name monras --wordcloud wc.png
Wordcloud written to wc.png
```

this generates the file `wc.png` ub the local directory:
![Word Cloud](wc.png)

### Notes:
At the moment only the first arxiv page will be scrapped.

## Installation
Just download the repo and 
```
pip install my-research
```
