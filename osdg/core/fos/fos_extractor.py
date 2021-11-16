from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Union
import numpy as np

from .ngram_matcher import NgramMatcher


class FosExtractor:
    def __init__(self):
        fos_data = np.load(self.__path('data_files/fos_v321.npz'), allow_pickle=True)
        self.fos_ids = fos_data['fos_ids']
        self.fos_names = fos_data['fos_names']
        fos_data.close()

        self._fosmap = dict(zip(self.fos_ids, self.fos_names))

        self.ngram_matcher = NgramMatcher(self.fos_names,
                                          lowercase=True,
                                          token_pattern=r'(?u)\b\w+\b',
                                          ngram_size=(1, 4))


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
            idxs, frequencies = self.ngram_matcher.match([text])[0]
            if submerge:
                fos = {fos_id: frequency
                       for fos_id, _, frequency in self._submerge(self.fos_ids[idxs], self.fos_names[idxs], frequencies)}
            else:
                fos = dict(zip(self.fos_ids[idxs], frequencies))

        elif text_type == 'pdf_document':
            fos = defaultdict(int)
            for paragraph in self._segment(text):
                paragraph_fos = self.extract(paragraph, text_type='paragraph', submerge=False)
                for fos_id in paragraph_fos.keys():
                    fos[fos_id] += 1
            if submerge:
                fos = {
                    fos_id: frequency
                    for fos_id, _, frequency in self._submerge(fos.keys(),
                                                               [self.fos_id2fos_name[fos_id] for fos_id in fos.keys()],
                                                               fos.values())
                }

        else:
            raise NotImplementedError

        return fos

    
    def _segment(self, text):
        raise NotImplementedError


    def _submerge(self, ngram_ids: Iterable[str], ngram_names: Iterable[str], frequencies: Iterable[int]) -> List[List[Union[str, int]]]:
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
        ngrams = self._descore(ngram_ids, ngram_names, frequencies)
        submerged_ngrams, drop_ngram_ids = list(), set()
        for idx, (ngram_id, ngram_name, frequency) in enumerate(ngrams):
            for ngram_id2, ngram_name2, frequency2 in ngrams[idx+1:]:
                if ngram_name2 in ngram_name:
                    frequency += frequency2
                    drop_ngram_ids.add(ngram_id2)
            submerged_ngrams.append([ngram_id, ngram_name, frequency])
        submerged_ngrams = list(filter(lambda ng: ng[0] not in drop_ngram_ids, submerged_ngrams))
        return submerged_ngrams


    def _descore(self, ngram_ids: Iterable[str], ngram_names: Iterable[str], frequencies: Iterable[int]) -> List[List[Union[str, int]]]:
        """
        Reduces ngram frequency if they submerge into higher size ngram by higher size ngram frequency.
        i.e. [('data', 5), ('big data', 3), ('data driven approach', 1)] -> [[('data', 1), ('big data', 3), ('data driven approach', 2)]]
        """
        ngrams = sorted(zip(ngram_ids, ngram_names, frequencies), key=lambda ng: len(ng[1]), reverse=True)
        descored_ngrams = list()
        for idx, (ngram_id, ngram_name, frequency) in enumerate(ngrams):
            for _, fol_ngram_name, fol_frequency in ngrams[:idx]:
                if ngram_name in fol_ngram_name:
                    frequency -= fol_frequency
            if frequency > 0:
                descored_ngrams.append([ngram_id, ngram_name, frequency])
        return descored_ngrams

    
    def fos_id2fos_name(self, fos_id):
        return self._fosmap[fos_id]


    @staticmethod
    def __path(fpath):
        return (Path(__file__).parent/fpath).resolve()
