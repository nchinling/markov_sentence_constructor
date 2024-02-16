from flask import Flask, request, render_template
import random
import sqlite3
from db_utlilty import preprocess_and_store, create_table_if_not_exists, get_random_word
from generator import choose_next_word

app = Flask(__name__)

sentences = []


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/train', methods=['GET', 'POST'])
def train_model():
    if request.method == 'GET':
        return render_template('train.html')
    elif request.method == 'POST':
        paragraph = request.form.get('paragraph')
        if paragraph:
            sentences = paragraph.split('.')
            # Remove unwanted characters
            sentences = [sentence.replace('.', '').replace(
                '"', '').replace(',', '') for sentence in sentences]
            # Remove leading/trailing whitespace and convert to lowercase
            sentences = [sentence.strip().lower()
                         for sentence in sentences if sentence.strip()]
            create_table_if_not_exists()
            preprocess_and_store(sentences)
            message = 'Sentences added successfully!'
        else:
            message = 'Invalid request. Sentence not provided.'
        return render_template('train.html', message=message)


@app.route('/generate', methods=['GET', 'POST'])
def generate_sentence():
    global sentences
    generated_sentence = None

    if request.method == 'POST':
        generated_sentence = []

        counter = 0
        while len(generated_sentence) < 15:
            if (counter == 0):
                last_word = get_random_word()
                counter = 1
            else:
                last_word = generated_sentence[-1]
            next_word = choose_next_word(last_word)

            if next_word:
                generated_sentence.append(next_word)
            else:
                break

        generated_sentence = ' '.join(generated_sentence)
        generated_sentence = generated_sentence.capitalize()
        generated_sentence += '.'
        return render_template('generate.html', generated_sentence=generated_sentence, sentences=sentences)
    elif request.method == 'GET':
        return render_template('generate.html', generated_sentence=generated_sentence, sentences=sentences)


if __name__ == '__main__':
    app.run(debug=True)
