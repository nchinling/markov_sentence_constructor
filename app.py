from flask import Flask, request, render_template, jsonify
import random

app = Flask(__name__)

# Initialize sentence list
sentences = []


@app.route('/train', methods=['GET', 'POST'])
def train_model():
    global sentences
    if request.method == 'GET':
        return render_template('train.html')
    elif request.method == 'POST':
        sentence = request.form.get('sentence')
        if sentence:
            sentences.append(sentence)
            message = 'Sentence added successfully!'
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
        generated_sentence.extend(start_sentence)

        # Generate the sentence
        while len(generated_sentence) < 20:  # Limit the generated sentence length to 20 words
            last_word = generated_sentence[-1]
            next_word = choose_next_word(last_word)
            if next_word:
                generated_sentence.append(next_word)
            else:
                break

        generated_sentence = ' '.join(generated_sentence)
        return render_template('generate.html', generated_sentence=generated_sentence, sentences=sentences)
    elif request.method == 'GET':
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
    if candidate_words:
        return random.choice(candidate_words)
    else:
        return None


if __name__ == '__main__':
    app.run(debug=True)
