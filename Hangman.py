import random

# Step 1: List of words
word_list = ['python', 'hangman', 'programming', 'code', 'developer']

# Step 2: Randomly choose a word
chosen_word = random.choice(word_list)
word_length = len(chosen_word)

# Step 3: Game variables
guessed_letters = []
attempts = 6
display = ['_' for _ in range(word_length)]

print("🎮 Welcome to Hangman!")
print("Guess the word letter by letter.")
print("You have", attempts, "lives.\n")

# Step 4: Game loop
while attempts > 0 and '_' in display:
    print("Word: ", ' '.join(display))
    print("Guessed Letters: ", ', '.join(guessed_letters))
    guess = input("Enter a letter: ").lower()

    if not guess.isalpha() or len(guess) != 1:
        print("❌ Please enter a single alphabet.\n")
        continue

    if guess in guessed_letters:
        print("⚠️ You already guessed that letter.\n")
        continue

    guessed_letters.append(guess)

    if guess in chosen_word:
        print("✅ Good guess!\n")
        for i in range(word_length):
            if chosen_word[i] == guess:
                display[i] = guess
    else:
        attempts -= 1
        print(f"❌ Wrong guess! You have {attempts} {'life' if attempts == 1 else 'lives'} left.\n")

# Step 5: End game
if '_' not in display:
    print("🎉 Congratulations! You guessed the word:", chosen_word)
else:
    print("💀 Game Over! The correct word was:", chosen_word)
