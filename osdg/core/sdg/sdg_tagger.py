from pathlib import Path
from typing import Dict, List, Union, Iterable
import json


class SdgTagger:
    def __init__(self):
        with open(self.__path('data_files/OSDG-mapping.json'), 'r') as file_:
            self.mapping = [(sdg, set(fos_ids)) for sdg, fos_ids in json.load(file_).items()]

        with open(self.__path('data_files/OSDG-fosmap.json'), 'r') as file_:
            self.fosmap = json.load(file_)

        self.use_frequency = True
        self.n_min_relevant_fos = 2
        self.limit = 5


    def tag(self, fos: Dict[str, Union[int, float]], detailed: bool) -> List[Dict[str, Union[str, float, List[str]]]]:
        """
        Assigns SDG labels to given FOS.

        Parameters
        ----------
        fos : Dict[str, Union[int, float]]
            FOS and their frequencies.

        detailed : bool
            If true, returns relevant FOS ids for each SDG.

        Returns
        -------
        List[Dict[str, Union[str, float, List[str]]]]
            List of SDG labels and their relevance scores.
            If detailed is True, returns relevant FOSes.
        """
        sdgs = []
        fos_ids = fos.keys()
        for sdg, sdg_fos_ids in self.mapping:
            relevant_fos_ids = sdg_fos_ids.intersection(fos_ids)
            if relevant_fos_ids and len(relevant_fos_ids) >= self.n_min_relevant_fos:
                if self.use_frequency:
                    relevance = 0
                    for fos_id in relevant_fos_ids:
                        relevance += fos.get(fos_id)
                else:
                    relevance = len(relevant_fos_ids)
                if detailed:
                    sdgs.append({'sdg': sdg,
                                 'relevance': float(relevance),
                                 'fos_ids': list(relevant_fos_ids),
                                 'fos_names': self._convert_fos_ids_to_names(relevant_fos_ids)})
                else:
                    sdgs.append({'sdg': sdg,
                                 'relevance': float(relevance)})
        sdgs = self._apply_threshold(sdgs)
        return sorted(sdgs, key=lambda x: x['relevance'], reverse=True)[:self.limit]


    def tag_many(self, foses: Iterable[Dict[str, Union[int, float]]], detailed) -> List[List[Dict[str, Union[str, float, List[str]]]]]:
        """
        Assigns SDG labels to multiple sets of FOS.

        Parameters
        ----------
        foses : Iterable[Dict[str, Union[int, float]]]
            List of FOS sets.

        Returns
        -------
        List[List[Dict[str, Union[str, float, List[str]]]]]
            List of SDG labels for each set of FOSes.
            If detailed is True, returns relevant FOSes.
        """
        sdgs = []
        for fos in foses:
            sdgs.append(self.tag(fos, detailed=detailed))
        return sdgs


    def _apply_threshold(self, sdgs):
        return sdgs


    def _convert_fos_ids_to_names(self, fos_ids: Iterable[str]) -> List[str]:
        """
        Converts FOS ids to FOS names.
        """
        return list(map(lambda fos_id: self.fosmap[fos_id], fos_ids))


    @staticmethod
    def __path(fpath):
        return (Path(__file__).parent/fpath).resolve()
