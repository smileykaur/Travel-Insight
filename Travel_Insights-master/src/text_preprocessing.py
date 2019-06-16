"""
This module will take the data read from reddit and perform basic pre-processing on data such as -
    - converting text to lower case,
    - type-conversion of data,
    - removing the unwanted character, punctuations
"""

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
import re
# from bs4 import BeautifulSoup
import unicodedata
import spacy

tokenizer = ToktokTokenizer()
nlp = spacy.load('en')
stopword_list = nltk.corpus.stopwords.words('english')


class TextCleaning:
    """
    This class implements text pre-processing
    """
    def __init__(self):
        self.text = None

    def remove_accented_chars(self):
        """
        :return:
        """
        self.text = unicodedata.normalize('NFKD', self.text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def remove_special_characters(self, remove_digits=True):
        """
        remove characters and digits. User can chose if the
        :param remove_digits:
        :return:
        """
        pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
        self.text = re.sub(pattern, '', self.text)

    def simple_stemmer(self):
        """
        generate word stems i.e root words
        :return:
        """
        ps = nltk.porter.PorterStemmer()
        self.text = ' '.join([ps.stem(word) for word in self.text.split()])

    def lemmatize_text(self):
        """
        Lemattize text
        :return:
        """
        _text = nlp(self.text)
        self.text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in _text])

    def remove_stopwords(self, is_lower_case=False):
        """
        Remove stopwords
        :param is_lower_case:
        :return:
        """
        tokens = tokenizer.tokenize(self.text)
        tokens = [token.strip() for token in tokens]

        if is_lower_case:
            filtered_tokens = [token for token in tokens if token not in stopword_list]
        else:
            filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]

        filtered_text = ' '.join(filtered_tokens)
        return filtered_text

    def normalize_corpus(self, doc, accented_char_removal=True, text_lower_case=True,
                         special_char_removal=True, stopword_removal=True, remove_digits=True,
                         text_lemmatization=False, text_stemming=False,):
        """
        Take text and apply pre-processing steps
        :param doc: input text
        :param html_stripping: boolean (True or False)
        :param accented_char_removal: boolean (True or False)
        :param text_lower_case: boolean (True or False)
        :param special_char_removal: boolean (True or False)
        :param stopword_removal: boolean (True or False)
        :param remove_digits: boolean (True or False)
        :param text_lemmatization: boolean (True or False)
        :param text_stemming: boolean (True or False)
        :return:
        """
        self.text = doc

        if accented_char_removal:
            self.remove_accented_chars()

        if text_lower_case:
            self.text = self.text.lower()

        # remove extra newlines
        self.text = re.sub(r'[\r|\n|\r\n]+', ' ', self.text)

        if special_char_removal:
            # insert spaces between special characters to isolate them
            special_char_pattern = re.compile(r'([{.(-)!}])')
            self.text = special_char_pattern.sub(" \\1 ", self.text)
            self.remove_special_characters(remove_digits=remove_digits)

        # remove extra whitespace
        self.text = re.sub(' +', ' ', self.text)

        # remove stopwords:
        if stopword_removal:
            self.text = self.remove_stopwords(is_lower_case=text_lower_case)

        # lemmatize text:
        if text_lemmatization:
            self.lemmatize_text()

        # stemming text
        if text_stemming:
            self.simple_stemmer()

        return self.text
