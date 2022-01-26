from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Union
import json
import numpy as np
import pandas as pd

from .ngram_matcher import NgramMatcher


class KeywordExtractor:
    def __init__(self):
        self.keywords = np.array(pd.read_parquet(self.__path('data_files/keywords.parquet')).keyword)
        
        with open(self.__path('data_files/stop_words.json'), 'r') as file_:
            stop_words = json.load(file_)

        self.ngram_matcher = NgramMatcher(self.keywords,
                                          lowercase=True,
                                          singularize=True,
                                          token_pattern=r'(?u)\b\w+\b',
                                          ngram_size=(1, 4),
                                          stop_words=stop_words)


    def extract(self, text: str, text_type: str = 'paragraph', submerge: bool = False) -> Dict[str, int]:
        """
        Matches fos to one text.

        Parameters
        ----------
        text : str
            Input text.

        Returns
        -------
        Dict[str, int]
            Matched FOS to text.
              - keys : FOS ids
              - values : frequencies
        """
        if text_type == 'paragraph':
            idxs, freqs = self.ngram_matcher.match([text])[0]
            keywords = self.keywords[idxs]
            if submerge:
                return {
                    keyword: freq
                    for keyword, freq in self._submerge(keywords, freqs)}
            else:
                return dict(zip(keywords, freqs))

        elif text_type == 'pdf_document':
            keywords = defaultdict(int)
            for paragraph in self._segment(text):
                paragraph_kws = self.extract(paragraph, text_type='paragraph', submerge=False)
                for keyword in paragraph_kws.keys():
                    keywords[keyword] += 1
            if submerge:
                return {
                    keyword: freq
                    for keyword, freq in self._submerge(keywords.keys(), keywords.values())
                }

        else:
            raise NotImplementedError


    def _segment(self, text):
        raise NotImplementedError


    def _submerge(self, ngram_names: Iterable[str], frequencies: Iterable[int]) -> List[List[Union[str, int]]]:
        """
        Ngrams which are substrings of some other ngram are removed.
        Ngrams to which some other ngram subemrges into are awarded that ngram frequency.
        i.e. [('data', 5), ('big data', 3), ('data driven approach', 1)] -> [[('big data', 8), ('data driven approach', 6)]]

        NOTES
        -----
        - Maybe it is better to distribute frequency score instead of adding it on top.
          1. If [`data`, 5] submerges into n other ngrams, each ngram is awarded 5 / n .
          2. Distribute proportionally based on ngram frequencies.
        """
        ngrams = self._descore(ngram_names, frequencies)
        submerged_ngrams, drop_ngrams = list(), set()
        for idx, (ngram_name, frequency) in enumerate(ngrams):
            for ngram_name2, frequency2 in ngrams[idx+1:]:
                if ngram_name2 in ngram_name:
                    frequency += frequency2
                    drop_ngrams.add(ngram_name2)
            submerged_ngrams.append([ngram_name, frequency])
        submerged_ngrams = list(filter(lambda ng: ng[0] not in drop_ngrams, submerged_ngrams))
        return submerged_ngrams


    def _descore(self, ngram_names: Iterable[str], frequencies: Iterable[int]) -> List[List[Union[str, int]]]:
        """
        Reduces ngram frequency if they submerge into higher size ngram by higher size ngram frequency.
        i.e. [('data', 5), ('big data', 3), ('data driven approach', 1)] -> [[('data', 1), ('big data', 3), ('data driven approach', 2)]]
        """
        ngrams = sorted(zip(ngram_names, frequencies), key=lambda ng: len(ng[0]), reverse=True)
        descored_ngrams = list()
        for idx, (ngram_name, frequency) in enumerate(ngrams):
            for fol_ngram_name, fol_frequency in ngrams[:idx]:
                if ngram_name in fol_ngram_name:
                    frequency -= fol_frequency
            if frequency > 0:
                descored_ngrams.append([ngram_name, frequency])
        return descored_ngrams

    @staticmethod
    def __path(fpath):
        return (Path(__file__).parent/fpath).resolve()
