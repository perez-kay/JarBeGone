"""
This script contains functions for cleaning up pre-processed PDF text and
tokenizing its sentences.

Terminology Definitions:

raw_sentences:   The text ripped straight from the PDF. This text has not been
                 cleaned, so it still contains all in-text citations,
                 numbers, URLs, etc. It has been split up into a list where
                 each entry is a single sentence.

clean_sentences: Every sentence has had the noise removed (in-text citations,
                 numbers, URLs, etc,), all punctuation has been removed
                 and the text is in all lower case.

sentence_tokens: These are the clean sentences that have had all of their stop
                 words removed. Stop words are words like: is, the, are, etc.
                 Each sentences is now a list of its important words.     
"""

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import re

def get_raw_sentences(pdf_path):
    """
    Extracts the raw text from the PDF and separates it out into sentences.

    Parameters
    ----------
    pdf_path : str
        The local file path of the PDF

    Returns
    -------
    list
        Each entry is one sentence from the PDF.
    """
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'al', 'etc', 'e.g', 'i.e', 'fig'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)
    with open(pdf_path, "r") as file:
            # returns one string with all of the text
        raw_text = file.read()
    file.close()

    raw_sentences = sentence_splitter.tokenize(re.sub(" +", " ", raw_text))
    return raw_sentences

def get_single_clean_sentence(sentence):
    """
    Removes any and all instances of noise from a single sentence.
    Examples of noise include: in-text citations, URLs, numbers, emails, etc.

    Parameters
    ----------
    sentence : str
        The sentence to be cleaned

    Returns
    -------
    str
        The sentence with the noise removed
    """

    # removes any instance of an in-text citation following any of these formats:
    # (Smith & Johnson, 2019), (Smith, 2019), (Smith et al., 2019), (Smith & Johnson, 2019; James, 2019)
    clean_sentence = re.sub(r"\s\((?:(?:[\w \.&]+\, )+[0-9]{4}[;|:]*\s*)+\)", "", sentence)

    # removes any additional text/numbers next to "Table"
    clean_sentence = re.sub("(Table \w+)", "Table", clean_sentence)

    # Removes numbers (including decimals)
    clean_sentence = re.sub(r"\d+(\.[0-9]+)*", "", clean_sentence)

    # Removes the list of emails that tends to appear at the beginning
    # of a paper
    clean_sentence = re.sub(r"{.+}@\S+", "", clean_sentence)

    # removes any URLs
    clean_sentence = re.sub(r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#“”"-]*[\w@?^=%&\/~+“”"#-])', " ", clean_sentence)
    clean_sentence = re.sub(r"www\.\S+", "", clean_sentence)

    # removes any additional white space (e.g: "I like      cats   .") 
    clean_sentence = re.sub(" +", " ", clean_sentence)
    return clean_sentence

def get_clean_sentences(raw_sentences):
    """
    Cleans pre-processed PDF text to remove any noise.

    Parameters
    ----------
    raw_sentences : list
        Contains all sentences from the original PDF

    Returns
    -------
    list
        Each entry is a sentences with the noise removed
    """

    clean_sentences = []
    for sentence in raw_sentences:
        clean_sentences.append(get_single_clean_sentence(sentence))
    return clean_sentences

def get_tokenized_sentences(raw_sentences):
    # remove punctuation and make all letters lowercase
    clean_sentences = [re.sub(r'[^\w\s]','',sentence.lower()) for sentence in get_clean_sentences(raw_sentences)]

    stop_words = stopwords.words('english')

    # Removes stop words (using the list of stop words from NLTK) and returns
    # A list of lists, with each list containing the words in each sentence
    sentence_tokens = [[words for words in word_tokenize(sentence) if words not in 
                        stop_words] for sentence in clean_sentences]
    return sentence_tokens




