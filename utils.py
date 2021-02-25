

def is_english_language(string_input):
    """Checks if an IA is in English"""
    english_key_words = set([
        "The", "the", "Is", "is", "Are", "are",
        "This", "this", "That", "that", "Study", "study",
        "And", "and", "We", "we", "New", "new", "Of", "of"
    ])
    return any(w in string_input.split(' ') for w in english_key_words)
