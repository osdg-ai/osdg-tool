#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 13:58:51 2020

@author: lukas

V0.0.2.1
"""
import config
import pickle
import json
import ast
import os

from exceptions import UnsupportedTextLanguageError
from exceptions import QuerySymbolLimitError
from exceptions import NgramTokensNotFound

from scipy.sparse import coo_matrix

from gensim.models.phrases import Phraser

from sklearn.metrics.pairwise import cosine_similarity

from utils import is_english_language

import en_core_web_sm
nlp = en_core_web_sm.load(disbale=["parser", "ner"])

# %%


class SDGFinder:
    """
    SDG Assignation API

    V 0.0.3
    """

    def __init__(self):
        """
        Initialization function to load the dependencies for the Semantic Search
        """
        self.path = f'{os.getcwd()}/data/'

        print("Loading search dependencies, this will take around two minutes.")

        print(" 1/3 Loading resources for text vectorisation")
        # Bigram
        self.bigram = Phraser.load(self.path + "Spacy_bigram_th1.md")

        # Trigram
        self.trigram = Phraser.load(self.path + "spacy_trigram_th1.md")

        # IDF distribution
        with open(self.path + "spacy_idf_th1.json", "r") as file_:
            self.idf = json.loads(file_.read())

        # Mapping between tokens and their position in dictionary
        with open(self.path + "CombinedDictionaryMap.json", "r") as file_:
            self.map_dict = json.loads(file_.read())

        print(" 2/3 Loading Field of Study and Project Matrices")
        # Field of Sudy Matrix
        with open(self.path + "CombinedNGRAMMatrixCSR.pkl", "rb") as file_:
            self.fos_matrix = pickle.load(file_)

        print(" 3/3 Loading Meta-data")
        # MAG FOS ~740k fields
        with open(self.path + "FOSMAP.json", "r") as file_:
            self.fos_meta_data = json.loads(file_.read())

        # Fos Index
        with open(self.path + "FOSIndex.json", "r") as file_:
            self.fos_data_index = json.loads(file_.read())

        # Mapping between FOS and SDG
        with open(self.path+"OSDG-Ontology.json", "r") as file_:
            self.sdgMap = json.loads(file_.read())

        _ = self.sdgMap.pop("SDG_17")

        # Mapping between FOS and SDG
        with open(self.path+"SdgThresholds.json", "r") as file_:
            self.sdgThresholds = json.load(file_)

        print("Loading Completed")
        print("It is OK to proceed to Step 2.")


    def pre_proc(self):

        """
        Function to pre-process text:

        Keeps only the lemmas of the tokens consisting of alphanumeric characters;
        Each token has to be between 2 and 25 symbols long;
        Token must not be: an article , a stop-word , email , url;
        Years (18XX, 19XX, 20XX) are removed;
        Tokens are lowercased

        """

        alphanum = "abcdefghijklmnoprstuvwxyz©®//\\™1234567890-"
        alpha = "abcdefghijklmnoprstuvwxyz"
        articles = set(["the", "a", "an", "have"])
        bad_starts = set(["18", "19", "20"])
        bad_starts2 = set(["-", "_", "//", "\\"])

        tokens = []

        doc = nlp(self.query)
        for tok in doc:
            if all(c in alphanum for c in tok.text.lower()) and any(c in alpha for c in tok.text.lower()):
                if len(tok.text) > 2 and len(tok.text) < 30:
                    if (not tok.is_stop and not tok.like_url and not tok.like_email and tok.lemma_.lower() not in articles):
                        if tok.shape_ != "dddd" or tok.text[0:2] not in bad_starts:
                            plh = tok.lemma_.lower()
                            if plh != "":
                                if plh[0] in bad_starts2:
                                    plh = plh[1:]
                                if plh != "":
                                    if plh[-1] in bad_starts2:
                                        plh = plh[:-1]
                                if plh != "":
                                    tokens.append(plh)

        self.ngram_tokens = self.trigram[self.bigram[tokens]]
        if len(self.ngram_tokens) < config.MIN_NGRAM_TOKENS:
            raise NgramTokensNotFound(f'Length of ngram tokens must be greater than {config.MIN_NGRAM_TOKENS}.')

    def vectorise(self):
        """Converts a list of tokens to a TFIDF matrix (1, len( map_dict ) )"""
        text_tf = {x: self.ngram_tokens.count(x) for x in self.ngram_tokens}
        bads = []
        text_tfidf_d = {}
        for key, value in text_tf.items():
            if key in self.idf.keys():
                text_tfidf_d[key] = value * self.idf[key]
            else:
                bads.append(key)

        if bads != []:
            print(f"The term(s) '{str(bads)}' do not appear in any of the documents. There may be a spelling error - please check and correct the word(s).")

        col, data = [], []

        counter = 0
        for key, value in text_tfidf_d.items():
            if key in self.map_dict:
                col.append(self.map_dict[key])
                data.append(value)
                counter += 1

        row = [0] * counter
        self.query_words = list(set(col))

        self.text_matrix = coo_matrix((data, (row, col)), shape=(1, len(self.map_dict)))

    def search(self):
        """
        Maps query to FOS fields via cosine similarity
        of TF-IDF vectors
        """

        # Vectorise Query
        self.pre_proc()
        self.vectorise()

        # A
        # Calculate Similarities between Query and FOS
        fos_result_mat = cosine_similarity(self.fos_matrix, Y=self.text_matrix, dense_output=True)

        # Convert to dict; filterdepending on strictness level
        fos_result_raw = {x: i[0] for x, i in enumerate(fos_result_mat)}

        # Parse the results - map FOS index to FOS id
        self.fos_result = {self.fos_data_index[x]: i for x, i in fos_result_raw.items()}
        # return self.fos_result

    def getSDG(self, query, detailed=False):
        """
        Maps query FOS to SDGs via a list of ex-ante specified ontologies

        PARAMS:
            query - raw text input ; English , up to 1 M characters ;
            detailed - boolean; determines what is returned by the API ;

        detailed = False :
            Returns a list of tuples.
            Example:
            [(SDG, n)]
            Where "SDG" indicates a Sustainable Development Goal and
            "n" strength of relationship
        detailed = True :
            Retuns a dict :
                {SDG : { "FosIds" : [ FOSId1 , FOSId2 ] ,
                        "FosNames" : ["FOSName1" , "FOSName2"]}}
        """
        self.query = query
        try:
            self.validate_query()
        except (QuerySymbolLimitError, UnsupportedTextLanguageError) as error:
            return error.query_error

        try:
            self.search()
        except NgramTokensNotFound as error:
            return error.query_error

        self.top_fos_no = 100
        short_res = {k: v for k, v in sorted(self.fos_result.items(), key=lambda kv: kv[1], reverse=True)[0: self.top_fos_no]}

        sdg_res_raw_n = {}
        sdg_res_raw_fosIds = {}
        sdg_res_raw_fosNames = {}
        for key, value in self.sdgMap.items():
            plh1 = 0
            plh2 = []
            plh3 = []
            for k in value:
                if k in short_res:
                    plh1 += 1
                    plh2.append(k)
                    plh3.append(self.fos_meta_data[k])
            sdg_res_raw_n[key] = plh1
            sdg_res_raw_fosIds[key] = plh2
            sdg_res_raw_fosNames[key] = plh3

        # Applying .9 quota
        self.sdg_res = sorted(sdg_res_raw_n.items(), key=lambda kv: kv[1] / self.sdgThresholds[kv[0]]['quota_9'], reverse=True)

        self.sdg_res_det = {}
        for key, value in sdg_res_raw_fosIds.items():
            plh = {
                "FOSIds": sdg_res_raw_fosIds[key],
                "FOSNames": sdg_res_raw_fosNames[key]
            }
            self.sdg_res_det[key] = plh

        self.sdg_res_det['strongly_related'] = []
        self.sdg_res_det['moderately_related'] = []

        self.sdg_res_ord = []
        r_count = 0
        for item in self.sdg_res:
            if r_count == 3: 
                break
            value_u = ""
            if item[1] >= self.sdgThresholds[item[0]]['UpperTh']:
                value_u = "Strongly related"
                self.sdg_res_ord.append((item[0], value_u))
                self.sdg_res_det['strongly_related'].append(item[0])
                r_count += 1

            elif self.sdgThresholds[item[0]]['LowerTh'] < item[1] < self.sdgThresholds[item[0]]['UpperTh']:
                value_u = "Moderately related"
                self.sdg_res_ord.append((item[0], value_u))
                self.sdg_res_det['moderately_related'].append(item[0])
                r_count += 1

        return self.sdg_res_det if detailed else self.sdg_res_ord


    def validate_query(self):
        if len(self.query) > config.QUERY_SYMBOL_LIMIT:
            raise QuerySymbolLimitError(f'Query exceeds maximum allowed query length of {config.QUERY_SYMBOL_LIMIT}.')

        if is_english_language(self.query) is False:
            raise UnsupportedTextLanguageError('Language is not supported.')
