import re

def extract_terms(text):
    """
    Extract technical terms using simple heuristics
    """

    # Find capitalized words and technical patterns
    terms = set()

    words = text.split()

    for word in words:
        # remove punctuation
        clean_word = re.sub(r'[^a-zA-Z0-9]', '', word)

        # filter conditions
        if len(clean_word) > 6 and clean_word.isalpha():
            terms.add(clean_word)

    return list(terms)[:20]  # limit to top 20