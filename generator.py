import random
from db_utlilty import get_sentences_from_database


def choose_next_word(last_word):
    """
    Choose the next word based on the last word in the generated sentence.
    """
    global sentences
    sentences = get_sentences_from_database()
    candidate_words = []
    for sentence in sentences:
        words = sentence.split()
        for i in range(len(words) - 1):
            if words[i] == last_word:
                candidate_words.append(words[i + 1])
                print(candidate_words)
    if candidate_words:
        return random.choice(candidate_words)
    else:
        return None
