from flask import Flask, render_template, request, session, redirect, url_for
import random
import os

app = Flask(__name__)
app.secret_key = 'secret123'  # Needed for session management

# Load words from file

def load_words():
    try:
        with open('words.txt', 'r') as file:
            words = file.read().splitlines()
        return [word.strip().lower() for word in words if word.strip()]
    except FileNotFoundError:
        return ['flask', 'python', 'developer', 'hangman', 'template', 'session']  # fallback words

@app.route('/')
def home():
    if 'word' not in session:
        words = load_words()
        word = random.choice(words)
        session['word'] = word
        session['display'] = ['_' for _ in word]
        session['guessed'] = []
        session['attempts'] = 6
    return render_template('index.html',
                           display=session['display'],
                           guessed=session['guessed'],
                           attempts=session['attempts'],
                           game_over=False,
                           message='')

@app.route('/guess', methods=['POST'])
def guess():
    if 'word' not in session:
        return redirect(url_for('home'))

    guess = request.form['letter'].lower()
    word = session['word']
    display = session['display']
    guessed = session['guessed']
    attempts = session['attempts']
    message = ''

    if not guess.isalpha() or len(guess) != 1:
        message = "⚠️ Please enter a valid single alphabet."
    elif guess in guessed:
        message = f"⚠️ You already guessed '{guess}'."
    elif guess in word:
        for i, char in enumerate(word):
            if char == guess:
                display[i] = guess
        message = "✅ Good guess!"
    else:
        attempts -= 1
        message = f"❌ Wrong! '{guess}' is not in the word."

    if guess not in guessed:
        guessed.append(guess)

    session['display'] = display
    session['guessed'] = guessed
    session['attempts'] = attempts

    if '_' not in display:
        message = f"🎉 Congratulations! You guessed it right. The word was '{word}'."
        session.clear()
        return render_template('index.html', display=display, guessed=guessed,
                               attempts=attempts, game_over=True, message=message)

    if attempts <= 0:
        message = f"💀 Game Over! The word was '{word}'."
        session.clear()
        return render_template('index.html', display=display, guessed=guessed,
                               attempts=0, game_over=True, message=message)

    return render_template('index.html', display=display, guessed=guessed,
                           attempts=attempts, game_over=False, message=message)

@app.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
