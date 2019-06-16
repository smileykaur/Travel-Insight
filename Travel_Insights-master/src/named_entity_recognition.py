"""
Processing text through spacy NLP pipeline and extracting features such as part of speech tags,
dependency parsing and named entity recognition.

"""

import spacy
import pandas as pd
from collections import Counter
nlp = spacy.load('en')


class NER:
    def __init__(self, df_agg_by_submissions):
        self.df_agg_by_sub = df_agg_by_submissions
        self.nlp_dict = {'submission_id': list(), 'top_destination': list(),
                         'top_organization': list(), 'top_product': list()}
        self.result_path = "../results/"

    def NER(self):
        # TODO: cleaning the text for better results
        self.df_agg_by_sub.apply(lambda x: self.nlp_processing(x.submission_id, x.comment), axis=1)

        # write results to output

        self.ner_df = pd.DataFrame(self.nlp_dict)
        self.ner_df.to_csv(self.result_path+"ner_by_submission.csv")

        return

    def nlp_processing(self, submission_id, text):
        # This will perform all NLP processing on text. Inclued following stages:
        # 1. creates chunk of text before processing through spacy as max character limit
        # for spacy NLP processing is 100000
        # 2. generate top-K  gpe(destinations), orgs(organizations), products (PRODUCT),

        tokens_list = text.split()
        chunk_counter = 0
        gpe, org, product = list(), list(), list()
        chunk_size = 80000

        while chunk_counter < len(tokens_list) // chunk_size:
            chunk = tokens_list[chunk_counter * chunk_size: chunk_counter * chunk_size + chunk_size]
            # transforming into Spacy Doc format
            text_nlp = nlp(' '.join(chunk))
            _gpe, _org, _product = self.ner_processing(text_nlp)
            gpe.extend(_gpe)
            org.extend(_org)
            product.extend(_product)
            chunk_counter += 1

        # handle if any remaining chunks
        if chunk_size * chunk_counter < len(tokens_list):
            chunk = tokens_list[chunk_size * chunk_counter:]
            text_nlp = nlp(' '.join(chunk))
            _gpe, _org, _product = self.ner_processing(text_nlp)
            gpe.extend(_gpe)
            org.extend(_org)
            product.extend(_product)

        # adding to global nlp_dict
        self.nlp_dict['submission_id'].append(submission_id)
        self.nlp_dict['top_destination'].append(Counter(gpe).most_common(5))
        self.nlp_dict['top_organization'].append(Counter(org).most_common(5))
        self.nlp_dict['top_product'].append(Counter(product).most_common(5))

    def ner_processing(self, text_nlp):
        # this function identifies labels from NER on Spacy doc
        GPE = []
        ORG_FAC = []
        PRODUCT = []
        for ent in text_nlp.ents:
            if ent.label_ == "GPE" or ent.label_ == "LOC":
                GPE.append(str.lower(str(ent)))
            elif ent.label_ == "FAC" or ent.label_ == "ORG":
                ORG_FAC.append(str.lower(str(ent)))
            elif ent.label_ == "PRODUCT":
                PRODUCT.append(str.lower(str(ent)))

        return GPE, ORG_FAC, PRODUCT
