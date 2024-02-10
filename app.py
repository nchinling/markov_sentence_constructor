from flask import Flask, request, render_template, jsonify
import random
import sqlite3

app = Flask(__name__)

# Function to create a connection to the SQLite database


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('sentences.db')
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to create the sentences table if not exists


def create_table(conn):
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS sentences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sentence TEXT NOT NULL
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_create_table)
    except sqlite3.Error as e:
        print(e)


# Initialize the database connection and create the table
conn = create_connection()
if conn is not None:
    create_table(conn)
    conn.close()

# Initialize sentence list
sentences = []


# @app.route('/train', methods=['GET', 'POST'])
# def train_model():
#     global sentences
#     if request.method == 'GET':
#         return render_template('train.html')
#     elif request.method == 'POST':
#         sentence = request.form.get('sentence')
#         if sentence:
#             sentences.append(sentence)
#             message = 'Sentence added successfully!'
#         else:
#             message = 'Invalid request. Sentence not provided.'
#         return render_template('train.html', message=message)

@app.route('/train', methods=['GET', 'POST'])
def train_model():
    if request.method == 'GET':
        return render_template('train.html')
    elif request.method == 'POST':
        paragraph = request.form.get('paragraph')
        if paragraph:
            sentences = paragraph.split('.')
            # Remove full stops from each sentence
            sentences = [sentence.replace('.', '') for sentence in sentences]
            # Remove leading/trailing whitespace and convert to lowercase
            sentences = [sentence.strip().lower()
                         for sentence in sentences if sentence.strip()]
            conn = create_connection()
            if conn is not None:
                cursor = conn.cursor()
                for sentence in sentences:
                    cursor.execute(
                        "INSERT INTO sentences (sentence) VALUES (?)", (sentence,))
                conn.commit()
                conn.close()
                message = 'Sentences added successfully!'
            else:
                message = 'Database connection error.'
        else:
            message = 'Invalid request. Sentence not provided.'
        return render_template('train.html', message=message)


@app.route('/generate', methods=['GET', 'POST'])
def generate_sentence():
    global sentences
    generated_sentence = None

    if request.method == 'POST':
        if not sentences:
            return render_template('generate.html', error_message="There are no sentences yet")

        generated_sentence = []

        # Choose a random sentence to start
        start_sentence = random.choice(sentences).split()
        # generated_sentence.extend(start_sentence)

        # Generate the sentence
        while len(generated_sentence) < 20:  # Limit the generated sentence length to 10 words
            last_word = start_sentence[-1]
            print(last_word)
            generated_sentence.append(last_word)
            next_word = choose_next_word(last_word)
            print(next_word)
            # next_word = "cool"
            if next_word:
                generated_sentence.append(next_word)
                # generated_sentence.append("fun")
            else:
                break

        generated_sentence = ' '.join(generated_sentence)
        return render_template('generate.html', generated_sentence=generated_sentence, sentences=sentences)
    elif request.method == 'GET':
        sentences = get_sentences_from_database()  # Fetch sentences from the database
        return render_template('generate.html', generated_sentence=generated_sentence, sentences=sentences)


def choose_next_word(last_word):
    """
    Choose the next word based on the last word in the generated sentence.
    """
    global sentences
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

# Function to fetch sentences from the database


def get_sentences_from_database():
    conn = sqlite3.connect('sentences.db')
    cursor = conn.cursor()
    cursor.execute("SELECT sentence FROM sentences")
    sentences = [row[0] for row in cursor.fetchall()]
    conn.close()
    return sentences


if __name__ == '__main__':
    app.run(debug=True)
