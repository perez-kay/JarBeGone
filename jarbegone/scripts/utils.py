"""
This script contains utility functions necessary for the Flask app.
"""

import os
import numpy as np
from jarbegone import app

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """
    Checks to make sure if the file given is of one of the allowed file types.

    Parameters
    ----------
    filename : str
        The name of the file, with the extension included

    Returns
    -------
    boolean
        True if file is of an allowed type, false otherwise
    """

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_uploads():
    """Removes all files in the uploads directory."""

    for file in os.listdir(app.config['UPLOAD_PATH']):
        os.remove(os.path.join(app.config['UPLOAD_PATH'], file))


def get_word_embeddings():
    """
    Generates the word embeddings from the embeddings text file.

    Returns
    -------
    dict
        The dictionary containing the embeddings for each word
    """

    word_embeddings = {}
    f = open('glove.6B.100d.txt', encoding='utf-8')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs
    f.close()
    return word_embeddings


def get_matching_txt(filename):
    return filename.rsplit('.', 1)[0].lower() + ".txt"
