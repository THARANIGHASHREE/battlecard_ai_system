import spacy

# Load English NLP model once
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text, top_n=10):
    """
    Extracts top keywords (nouns & proper nouns) from text.
    """
    doc = nlp(text)
    # Keep nouns & proper nouns, ignore stopwords & punctuation
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and token.is_alpha]

    # Count frequency
    freq = {}
    for word in keywords:
        freq[word] = freq.get(word, 0) + 1

    # Sort by frequency
    sorted_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    # Return top N as a list of words
    return [word for word, count in sorted_keywords[:top_n]]
