#  Markov Sentence Generator app

## About the app
A Markov sentence generator is a type of algorithm used to generate sentences based on statistical patterns observed in a given corpus of text. The algorithm relies on Markov chains, which are mathematical models that describe a sequence of possible events in which the probability of each event depends on the state attained in the preceding event. A Markov chain can be used to model the likelihood of transitioning from one word to another based on the words that precede it in a given text.

The generator constructs a Markov chain by recording the frequency of word transitions. For example, if the word "cat" frequently follows the word "the" in the input text, the generator assigns a higher probability to that transition in the Markov chain.

To generate a sentence, the generator starts with a randomly selected word and uses the Markov chain to probabilistically select the next word based on the preceding word. This process continues until a predetermined stopping condition is met, such as reaching a provided sentence length. 

## Features

### 1. Train Model
- Users can provide paragraphs of text to train the text generation model.
- The paragraphs are preprocessed to remove unwanted characters, leading/trailing whitespace, and are converted to lowercase.
- The trained data is stored in a SQLite database.

### 2. Generate Text
- Users can generate text based on the trained model.
- The text generation process starts with a random word from the trained data and iteratively predicts the next word using a Markov Chain model until the desired length of the text is achieved.
- The generated text is capitalised and ends with a full-stop.


## Components

### 1. Flask Application
- The core of the application built using Flask, a Python web framework.
- Consists of routes for training the model, generating text, and serving HTML templates.

### 2. SQLite Database
- Stores the trained data in a relational database.
- The database schema includes tables for storing word frequencies.

### 3. Text Generation Logic
- Implemented using Markov Chain modeling.
- Chooses the next word based on the frequency of occurrence in the trained data.

## Usage

1. **Training the Model**
   - Navigate to the '/train' route.
   - Provide a paragraph of text in the input field and submit.
   - Trained data will be stored in the database.

2. **Generating Text**
   - Visit the '/generate' route.
   - Optionally specify the desired length of the generated text.
   - Click on the "Generate" button.
   - The app will generate text based on the trained model and display it on the page.

## Dependencies

- Flask: Web framework for building the application.
- SQLite3: Database management system for storing trained data.
- Random: Python module for selecting random words.
- Collections: Provides specialised datatypes.
