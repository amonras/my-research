import pandas as pd

from myresearch.scraper import scrape

repl = {'proof': 'Proof', 'theorem': 'Theorem', 'lemma': 'Lemma', 'Eq ': 'equation ',
            'eq': 'equation ', 'states': 'state', 'Fig': 'Figure',
            'CP': 'completely positive', 'measurements': 'measurement', 'Eqs': 'equations',
            'QFI': 'Quantum Fisher Information', 'MLE': 'maximum likelihood estimator',
            'CR': 'Cramer-Rao', 'GSs': 'Gaussian states', 'models': 'model',
            'quantum': 'Quantum', 'SLD': 'symmetric lograithmic derivative'}


def multipleReplace(text, wordDict):
    for key in wordDict:
        text = text.replace(key, wordDict[key])
    return text


def strip_redundant(text):
    words = []
    for word in text.split(" "):
        if len(word.strip(' ').strip(',')) >= 4:
            words.append(word.lower())
    return " ".join(words)


def count(words):
    wordcount = pd.Series(words).value_counts()
    return wordcount


if __name__ == "__main__":
    words = scrape("monras")
    print(count(words).head(30))
