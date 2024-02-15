import sqlite3
import random
from collections import Counter


def create_table_if_not_exists():
    conn = sqlite3.connect('word_frequencies.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS word_frequencies (
                    current_word TEXT,
                    next_word TEXT,
                    frequency INTEGER
                )''')
    conn.commit()
    conn.close()


def preprocess_and_store(sentences):
    conn = sqlite3.connect('word_frequencies.db')
    c = conn.cursor()
    word_frequency = Counter()
    for sentence in sentences:
        words = sentence.split()
        for i in range(len(words) - 1):
            word_frequency[(words[i], words[i + 1])] += 1

    for word_pair, freq in word_frequency.items():
        c.execute("SELECT * FROM word_frequencies WHERE current_word = ? AND next_word = ?",
                  (word_pair[0], word_pair[1]))
        existing_record = c.fetchone()
        if existing_record:
            updated_freq = existing_record[2] + freq
            c.execute("UPDATE word_frequencies SET frequency = ? WHERE current_word = ? AND next_word = ?",
                      (updated_freq, word_pair[0], word_pair[1]))
        else:
            c.execute("INSERT INTO word_frequencies VALUES (?, ?, ?)",
                      (word_pair[0], word_pair[1], freq))

    conn.commit()
    conn.close()


def get_random_word():
    conn = sqlite3.connect('word_frequencies.db')
    c = conn.cursor()
    c.execute(
        "SELECT DISTINCT current_word FROM word_frequencies ORDER BY RANDOM() LIMIT 1")
    random_word = c.fetchone()[0]

    conn.close()
    return random_word
