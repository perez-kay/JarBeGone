from .tokenizing import get_tokenized_sentences, get_raw_sentences
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

class TextRank:
    """
    This class represents an implementation for the Text Rank algorithm.

    ...

    Attributes
    ----------
    raw_sentences : list of str
        The text ripped straight from the PDF. This text has not been cleaned,
        so it still contains all in-text citations, numbers, URLs, etc. It has
        been split into sentences.
    sentence_tokens : list of list of str
        The cleaned PDF text with its stop words removed. Stop words are words
        like: is, the, are, etc. Each sentence is now a list of its important
        words.
    lengths : dict
        Represents the different lengths a summary can be.
    sentence_vectors : list
        The vectors that represent each sentence, made by taking the average
        of all of the word embeddings using the words in the sentence.
    sim_matrix : 2D NumPy array
        The similarity matrix for the PDF, which compares the similarity of
        all sentences against each other.

    Methods
    -------
    get_summary(length)
        Generates the summary for the passed in text.

    """


    def __init__(self, path_to_text, word_embeddings):
        """
        Parameters
        ----------
        path_to_text : str
            The relative path location to the pre-processed PDF.
            Must point to a plain text file.

        word_embeddings : dict
            The word embeddings generated from "glove.6B.100d.txt"
        """

        self.word_embeddings = word_embeddings
        self.raw_sentences = get_raw_sentences(path_to_text)
        self.sentence_tokens = get_tokenized_sentences(self.raw_sentences)
        self.lengths = {
            'short': round(len(self.raw_sentences) * 0.1),
            'medium': round(len(self.raw_sentences) * 0.2),
            'long': round(len(self.raw_sentences) * 0.3)
        }
        self.sentence_vectors = self._get_sentence_vectors()
        self.sim_matrix = self._get_sim_matrix()



    def _get_sentence_vectors(self):
        """
        Generates the sentence vectors for each sentence.

        Returns
        -------
        list
            The sentence vectors for each sentence
        """

        sentence_vectors = []
        for sentence in self.sentence_tokens:
            if len(sentence) != 0:
                v = sum([self.word_embeddings.get(word, np.zeros((100,))) for word in sentence])/(len(sentence)+0.001)
            else:
                v = np.zeros((100,))
            sentence_vectors.append(v)
        return sentence_vectors

    def _get_sim_matrix(self):
        """
        Generates the similarity matrix for the sentences.

        Each sentence is compared against all of the other sentences in the
        document. Their similarity is determined based on the Cosine Similarity
        of their sentence vectors. Sentences are not compared against themselves
        and thus receive a 0 score.

        Returns
        -------
        2D NumPy array
            The array representing the similarity matrix
        """

        sim_matrix = np.zeros([len(self.raw_sentences), len(self.raw_sentences)])
        for i in range(len(self.raw_sentences)):
            for j in range(len(self.raw_sentences)):
                if i != j:
                    sim_matrix[i][j] = cosine_similarity(
                                self.sentence_vectors[i].reshape(1,100),
                                self.sentence_vectors[j].reshape(1,100))[0,0]
        return sim_matrix

    def get_summary(self, length):
        """
        Generates the summary for the text, based off of the given length

        Parameters
        ----------
        length : str
            Length can either be 'Short', 'Medium', or 'Long'
            This determines how many sentences are included in the summary.
            Length is based off of the original size of the text.

        Returns
        -------
        list
            A list containing the top <length> sentences to be included in
            the summary.
        """

        nx_graph = nx.from_numpy_array(self.sim_matrix)
        scores = nx.pagerank(nx_graph)
        scored_sentences = sorted(((scores[i],s) for i,s in
                                enumerate(self.raw_sentences)), reverse=True)

        ranked_sentences = [sentence for score, sentence in scored_sentences]
        if length not in self.lengths.keys():
            size = self.lengths['Short']
        else:
            size = self.lengths[length]

        summary = []
        for i in range(len(self.raw_sentences)):
            if self.raw_sentences[i] in ranked_sentences[:size]:
                summary.append(self.raw_sentences[i])
        return summary

