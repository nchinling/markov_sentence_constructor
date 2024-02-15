import random
from collections import Counter
import sqlite3


def choose_next_word(last_word):
    conn = sqlite3.connect('word_frequencies.db')
    c = conn.cursor()
    c.execute(
        "SELECT next_word, frequency FROM word_frequencies WHERE current_word = ?", (last_word,))
    frequencies = c.fetchall()

    if frequencies:
        chosen_word = random.choices([freq[0] for freq in frequencies], weights=[
                                     freq[1] for freq in frequencies])[0]
        return chosen_word
    else:
        return None
