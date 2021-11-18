from collections import defaultdict
from typing import Any, DefaultDict, Iterable, List, Tuple, Union, NoReturn

import numpy as np
import re


class NgramMatcher:
    def __init__(self,
                 ngrams: Iterable[str],
                 lowercase: bool = True,
                 token_pattern: str = r'(?u)\b\w+\b',
                 ngram_size: Union[int, Tuple[int, int]] = (1, 1)):
        r"""
        Ngram matcher and counter.

        Parameters
        ----------
        ngrams : Iterable[str]
            List of ngrams to match.
        lowercase : bool, by default True
            Lowercases all characters.
        token_pattern : str, by default r'(?u)\b\w+\b'
            Regex expression that designates a token.
        ngram_size : Union[int, Tuple[int, int]], by default (1, 1)
            Minimum and maximum boundaries for token amount per ngram.
            If integer is provided, it represents both minimum and maximum boundaries.
        """
        self.__validate_ngrams(ngrams)
        self.ngrams = np.array(ngrams)

        self.lowercase = lowercase
        if lowercase:
            self.ngram_index_map = {ngram.strip().lower(): idx for idx, ngram in enumerate(ngrams)}
        else:
            self.ngram_index_map = {ngram.strip(): idx for idx, ngram in enumerate(ngrams)}

        self.token_pattern = token_pattern
        self.__token_pattern = re.compile(token_pattern)
        if self.__token_pattern.groups > 1:
            raise ValueError(f'Too many groups in ngram pattern : {self.__token_pattern.groups}')

        if isinstance(ngram_size, int):
            self.ngram_size = (ngram_size, ngram_size)
        elif isinstance(ngram_size, tuple) and len(ngram_size) == 2:
            self.ngram_size = ngram_size
        else:
            raise ValueError(f'Expected int or tuple of length 2 for argument ngram_size. Got {type(ngram_size)}.')


    @staticmethod
    def __validate_ngrams(ngrams) -> NoReturn:
        if isinstance(ngrams, str) or not hasattr(ngrams, '__iter__'):
            raise ValueError('Terms must be iterable.')
        if len(ngrams) == 0:
            raise ValueError('Empty terms passed.')
        if len(ngrams) != len(set(ngrams)):
            raise ValueError('Terms contain duplicate entries.')
        try:
            _ = ''.join(ngrams)
        except TypeError:
            raise TypeError('Terms contain non str type values.')


    @staticmethod
    def __validate_documents(documents: Any) -> NoReturn:
        if isinstance(documents, str) or not hasattr(documents, '__iter__'):
            raise TypeError('Iterable of strings is expected.')
        if any(not isinstance(doc, str) for doc in documents):
            raise TypeError('Documents contain non str values.')


    def _generate_ngrams(self, document: str) -> List[str]:
        """
        Extracts ngrams from text.

        Parameters
        ----------
        document : str
            Text

        Returns
        -------
        List[str]
            List of generated ngrams.
        """
        if self.lowercase:
            document = document.lower()
        tokens = self.__token_pattern.findall(document)

        min_n, max_n = self.ngram_size
        if max_n == 1:
            return tokens

        if min_n == 1:
            ngrams = list(tokens)
            min_n += 1
        else:
            ngrams = list()

        n_tokens = len(tokens)

        for k in range(min_n, min(max_n + 1, n_tokens + 1)):
            for j in range(n_tokens - k + 1):
                ngrams.append(
                    ' '.join(tokens[j:j+k])
                )

        return ngrams


    def _match_ngrams(self, documents: Iterable[str]) -> List[Tuple[List[int], List[int]]]:
        """
        Matches ngrams to texts.
        For each document:
          1. Converts document into tokens
          2. Generates ngrams of size defined in ngram_size
          3. Crossreferences ngrams with matching ngrams
          > Counts each ngram frequency

        Parameters
        ----------
        documents : Iterable[str]
            List of texts.

        Returns
        -------
        List[Tuple[List[int], List[int]]]
            Each element is a tuple.
              - index 0 contains ngram indices List[int]
              - index 1 contains ngram frequencies List[int]
        """
        ngrams = []

        ngram_index_map = self.ngram_index_map

        self.__validate_documents(documents)
        for document in documents:
            ngram_counts = defaultdict(int)
            for ngram in self._generate_ngrams(document):
                try:
                    idx = ngram_index_map[ngram]
                except KeyError:
                    continue
                ngram_counts[idx] += 1

            ngrams.append((list(ngram_counts.keys()),
                           list(ngram_counts.values())))

        return ngrams


    def match(self, documents: Iterable[str]) -> List[Tuple[List[int], List[int]]]:
        """
        Matches ngrams to texts.

        Parameters
        ----------
        documents : Iterable[str]
            List of texts.

        Returns
        -------
        List[Tuple[List[int], List[int]]]
            Each element is a tuple.
              - index 0 contains ngram indices List[int]
              - index 1 contains ngram frequencies List[int]
        """
        ngrams = self._match_ngrams(documents)
        return ngrams
