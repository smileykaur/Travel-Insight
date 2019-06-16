"""
Clean text data
"""

import nltk
import re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
stopWords = set(stopwords.words('english'))
lt = WordNetLemmatizer()

class CleaningText:
    def tokenize(self, text, lower=True):
        if lower:
            return [token.strip().lower() for token in text.split()]
        else:
            return [token.strip() for token in text.split()]

    def remove_stop_words(self, text):
        return [word for word in text if word not in stopWords]

    def lemmatize(self, text):
        return [(lt.lemmatize(x)) for x in text]

    def clean_text(self, text):
        # regex to remove URL from string
        text = re.sub('http://\S+|https://\S+', '', text)
        # regex to remove special characters from string except [: ? ! . , ']
        text = re.sub(r"[^a-zA-Z0-9?!',.]", " ", text)

        tokenized_text = self.tokenize(text, False)
        lemmatized_text = self.lemmatize(tokenized_text)
        cleaned_text = self.remove_stop_words(lemmatized_text)

        return ' '.join(token for token in cleaned_text)
