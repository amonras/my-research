import re

from myresearch.paths import resources


def get_stopwords():
    """
    Read contents of resource file, return list of stopwords
    :return:
    """
    text = ""
    with open(resources / "stopwords.txt", "r") as f:
        line = f.readline()
        text += line
        while line:
            line = f.readline()
            text += line
    # not efficient but it's ok. little overhead
    text = " ".join(text.split("\n"))
    words = text.split(" ")
    return words


def filter_words(words, callable_ignore):
    for word in words:
        if not callable_ignore(word):
            yield word


# Define the regular expression pattern for letters only
letters_only_pattern = re.compile(r'^[a-zA-Z]+$')


def is_letters_only(input_string):

    # Use the pattern to match the input string
    match = letters_only_pattern.match(input_string)

    # Return True if the input consists exclusively of letters, False otherwise
    return bool(match)


stopwords = get_stopwords()


def ignore(word):
    if len(word) < 4:
        return True
    if not is_letters_only(word):
        return True
    if word in stopwords:
        return True
    return False
