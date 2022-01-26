from pathlib import Path
from typing import Dict, List, Union, Iterable
import json


class SdgTagger:
    def __init__(self):
        with open(self.__path('data_files/OSDG-kw-mapping.json'), 'r') as file_:
            self.mapping = [(sdg, set(keywords)) for sdg, keywords in json.load(file_).items()]

        self.use_frequency = True
        self.n_min_relevant_fos = 1
        self.limit = 3


    def tag(self, keywords: Dict[str, Union[int, float]], detailed: bool) -> List[Dict[str, Union[str, float, List[str]]]]:
        """
        Assigns SDG labels to given FOS.

        Parameters
        ----------
        keywords : Dict[str, Union[int, float]]
            Keywords and their frequencies.

        detailed : bool
            If true, returns relevant FOS ids for each SDG.

        Returns
        -------
        List[Dict[str, Union[str, float, List[str]]]]
            List of SDG labels and their relevance scores.
            If detailed is True, returns relevant FOSes.
        """
        sdgs = []
        keywords_ = set(keywords.keys())
        for sdg, sdg_keywords in self.mapping:
            rel_keywords = sdg_keywords.intersection(keywords_)
            if rel_keywords and len(rel_keywords) >= self.n_min_relevant_fos:
                if self.use_frequency:
                    relevance = 0
                    for kw in rel_keywords:
                        relevance += keywords.get(kw)
                else:
                    relevance = len(rel_keywords)
                if detailed:
                    sdgs.append({'sdg': sdg,
                                 'relevance': float(relevance),
                                 'keywords': list(rel_keywords)})
                else:
                    sdgs.append({'sdg': sdg,
                                 'relevance': float(relevance)})
        sdgs = self._apply_threshold(sdgs)
        return sorted(sdgs, key=lambda x: x['relevance'], reverse=True)[:self.limit]


    def tag_many(self, keywords: Iterable[Dict[str, Union[int, float]]], detailed) -> List[List[Dict[str, Union[str, float, List[str]]]]]:
        """
        Assigns SDG labels to multiple sets of FOS.

        Parameters
        ----------
        keywords : Iterable[Dict[str, Union[int, float]]]
            List of keyword sets

        Returns
        -------
        List[List[Dict[str, Union[str, float, List[str]]]]]
            List of SDG labels for each set of FOSes.
            If detailed is True, returns relevant FOSes.
        """
        sdgs = []
        for kws in keywords:
            sdgs.append(self.tag(kws, detailed=detailed))
        return sdgs


    def _apply_threshold(self, sdgs):
        return sdgs

    @staticmethod
    def __path(fpath):
        return (Path(__file__).parent/fpath).resolve()
