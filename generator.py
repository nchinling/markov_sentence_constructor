import random
from db_utlilty import get_sentences_from_database
from collections import Counter


def choose_next_word(last_word):
    """
    Choose the next word based on the last word in the generated sentence.
    """
    global sentences
    sentences = get_sentences_from_database()
    candidate_words = []
    word_frequency = Counter()

    for sentence in sentences:
        words = sentence.split()
        for i in range(len(words) - 1):
            if words[i] == last_word:
                candidate_words.append(words[i + 1])
                word_frequency[words[i + 1]] += 1
                print(candidate_words)
    if candidate_words:
        # return random.choice(candidate_words)
        # Weighted selection based on frequency
        total_frequency = sum(word_frequency.values())
        # create dictionary (dictionary comprehension)
        probabilities = {word: freq / total_frequency for word,
                         freq in word_frequency.items()}
        chosen_word = random.choices(
            list(probabilities.keys()), weights=list(probabilities.values()))[0]
        return chosen_word
    else:
        return None
