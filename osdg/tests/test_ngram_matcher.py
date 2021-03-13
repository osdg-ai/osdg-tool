import pytest

from osdg.core.fos.ngram_matcher import NgramMatcher


def test_init_ngrams_validity_1():
    with pytest.raises(ValueError):
        _ = NgramMatcher(ngrams=1)


def test_init_ngrams_validity_2():
    with pytest.raises(ValueError):
        _ = NgramMatcher(ngrams='abc')


def test_init_ngrams_validity_3():
    with pytest.raises(TypeError):
        _ = NgramMatcher(ngrams=['a', 'b', 1])


def test_init_ngrams_validity_4():
    with pytest.raises(ValueError):
        _ = NgramMatcher(ngrams=['a', 'a', 'b', 'c'])


def test_ngram_index_map():
    ngrams = ['a', 'b', 'c']
    valid_ngram_index_map = {value: idx for idx, value in enumerate(ngrams)}
    nm = NgramMatcher(ngrams=ngrams)
    assert nm.ngram_index_map == valid_ngram_index_map


def test_token_pattern_groups():
    pattern = r'((\d+)(\s\d+)*)'
    with pytest.raises(ValueError):
        _ = NgramMatcher(ngrams=['a', 'b'], token_pattern=pattern)


def test_lowercase():
    lowercase = True
    ngrams = ['A', 'b', 'C']
    nm = NgramMatcher(ngrams=ngrams, lowercase=lowercase)
    assert all(i.islower() for i in ''.join(nm.ngram_index_map.keys()))


def test_not_lowercase():
    lowercase = False
    ngrams = ['A', 'b', 'C']
    nm = NgramMatcher(ngrams=ngrams, lowercase=lowercase)
    assert not all(i.islower() for i in ''.join(nm.ngram_index_map.keys()))


def test_ngram_size_1():
    ngram_size = (1, 2, 3)
    with pytest.raises(ValueError):
        _ = NgramMatcher(ngrams=['a', 'b'], ngram_size=ngram_size)


def test_ngram_size_2():
    ngram_size = (1,)
    with pytest.raises(ValueError):
        _ = _ = NgramMatcher(ngrams=['a', 'b'], ngram_size=ngram_size)


def test_ngram_size_3():
    ngram_size = '1'
    with pytest.raises(ValueError):
        _ = _ = NgramMatcher(ngrams=['a', 'b'], ngram_size=ngram_size)


def test_ngram_size_4():
    ngram_size = 1
    nm = NgramMatcher(ngrams=['a', 'b'], ngram_size=ngram_size)
    assert nm.ngram_size == (1, 1)


def test_ngram_size_5():
    ngram_size = (1, 3)
    nm = NgramMatcher(ngrams=['a', 'b'], ngram_size=ngram_size)
    assert nm.ngram_size == ngram_size


def test_validate_documents_1():
    documents = 'word'
    nm = NgramMatcher(ngrams=['a', 'b'])
    with pytest.raises(TypeError):
        nm._NgramMatcher__validate_documents(documents)


def test_validate_documents_2():
    documents = ['a', 'b', 1]
    nm = NgramMatcher(ngrams=['a', 'b'])
    with pytest.raises(TypeError):
        nm._NgramMatcher__validate_documents(documents)


def test_validate_documents_3():
    documents = ['a', 'b', 'c']
    nm = NgramMatcher(ngrams=['a', 'b'])
    nm._NgramMatcher__validate_documents(documents)


def test_generate_ngrams_1():
    document = "Do I lose when the police officer says papers and I say scissors?"
    true_ngrams = ['do', 'i', 'lose', 'when', 'the', 'police', 'officer',
                   'says', 'papers', 'and', 'i', 'say', 'scissors']
    nm = NgramMatcher(ngrams=['a', 'b'], lowercase=True, ngram_size=1)
    ngrams = nm._generate_ngrams(document)
    assert all(ngram in true_ngrams for ngram in ngrams) and len(ngrams) == len(true_ngrams)


def test_generate_ngrams_2():
    document = "Do I lose when the police officer says papers and I say scissors?"
    true_ngrams = ['Do', 'I', 'lose', 'when', 'the', 'police', 'officer',
                   'says', 'papers', 'and', 'I', 'say', 'scissors']
    nm = NgramMatcher(ngrams=['a', 'b'], lowercase=False, ngram_size=1)
    ngrams = nm._generate_ngrams(document)
    assert all(ngram in true_ngrams for ngram in ngrams) and len(ngrams) == len(true_ngrams)


def test_generate_ngrams_3():
    document = "Do I lose when the police officer says papers and I say scissors?"
    true_ngrams = ['do', 'i', 'lose', 'when', 'the', 'police', 'officer',
                   'says', 'papers', 'and', 'i', 'say', 'scissors', 'do i',
                   'i lose', 'lose when', 'when the', 'the police', 'police officer',
                   'officer says', 'says papers', 'papers and', 'and i', 'i say', 'say scissors']

    nm = NgramMatcher(ngrams=['a', 'b'], lowercase=True, ngram_size=(1, 2))
    ngrams = nm._generate_ngrams(document)
    assert all(ngram in true_ngrams for ngram in ngrams) and len(ngrams) == len(true_ngrams)


def test_match_ngrams_1():
    ngrams = ['wages', 'household', 'parsley farmer']
    documents = ['If a parsley farmer gets sued, can they garnish his wages?']
    answer = ([0, 2], [1, 1])
    nm = NgramMatcher(ngrams=ngrams, lowercase=True, ngram_size=(1, 2))
    idxs, frequencies = nm._match_ngrams(documents)[0]
    assert all(answer[0][i] == idx and answer[1][i] == frequencies[i]
               for i, idx in enumerate(idxs))


def test_match_ngrams_2():
    ngrams = ['wages', 'household', 'parsley farmer']
    documents = ['If a parsley farmer gets sued, can they garnish his wages? Poor parsley farmer.']
    answer = ([0, 2], [1, 2])
    nm = NgramMatcher(ngrams=ngrams, lowercase=True, ngram_size=(1, 2))
    idxs, frequencies = nm._match_ngrams(documents)[0]
    assert all(answer[0][i] == idx and answer[1][i] == frequencies[i]
               for i, idx in enumerate(idxs))


def test_match_ngrams_3():
    ngrams = ['wages', 'household', 'parsley farmer']
    documents = ['If a parsley farmer gets sued, can they garnish his wages? Poor parsley farmer.',
                 'If a parsley farmer gets sued, can they garnish his wages?']
    answer_1 = ([0, 2], [1, 2])
    answer_2 = ([0, 2], [1, 1])
    nm = NgramMatcher(ngrams=ngrams, lowercase=True, ngram_size=(1, 2))
    results = nm._match_ngrams(documents)
    assert all(answer_1[0][i] == idx and answer_1[1][i] == results[0][1][i]
               for i, idx in enumerate(results[0][0]))
    assert all(answer_2[0][i] == idx and answer_2[1][i] == results[1][1][i]
               for i, idx in enumerate(results[1][0]))


def test_match_1():
    ngrams = ['wages', 'household', 'parsley farmer']
    documents = ['If a parsley farmer gets sued, can they garnish his wages?']
    answer = ([0, 2], [1, 1])
    nm = NgramMatcher(ngrams=ngrams, lowercase=True, ngram_size=(1, 2))
    idxs, frequencies = nm.match(documents)[0]
    assert all(answer[0][i] == idx and answer[1][i] == frequencies[i]
               for i, idx in enumerate(idxs))


def test_match_2():
    ngrams = ['wages', 'household', 'parsley farmer']
    documents = ['If a parsley farmer gets sued, can they garnish his wages? Poor parsley farmer.']
    answer = ([0, 2], [1, 2])
    nm = NgramMatcher(ngrams=ngrams, lowercase=True, ngram_size=(1, 2))
    idxs, frequencies = nm.match(documents)[0]
    assert all(answer[0][i] == idx and answer[1][i] == frequencies[i]
               for i, idx in enumerate(idxs))


def test_match_3():
    ngrams = ['wages', 'household', 'parsley farmer']
    documents = ['If a parsley farmer gets sued, can they garnish his wages? Poor parsley farmer.',
                 'If a parsley farmer gets sued, can they garnish his wages?']
    answer_1 = ([0, 2], [1, 2])
    answer_2 = ([0, 2], [1, 1])
    nm = NgramMatcher(ngrams=ngrams, lowercase=True, ngram_size=(1, 2))
    results = nm.match(documents)
    assert all(answer_1[0][i] == idx and answer_1[1][i] == results[0][1][i]
               for i, idx in enumerate(results[0][0]))
    assert all(answer_2[0][i] == idx and answer_2[1][i] == results[1][1][i]
               for i, idx in enumerate(results[1][0]))


