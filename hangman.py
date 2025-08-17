import random

# ------------------------------------------------
# ANSI Colors
# ------------------------------------------------
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# ------------------------------------------------
# ASCII Art for Hangman stages
# ------------------------------------------------
HANGMAN_PICS = [
    """
     +---+
         |
         |
         |
        ===""",
    """
     +---+
     O   |
         |
         |
        ===""",
    """
     +---+
     O   |
     |   |
         |
        ===""",
    """
     +---+
     O   |
    /|   |
         |
        ===""",
    """
     +---+
     O   |
    /|\\  |
         |
        ===""",
    """
     +---+
     O   |
    /|\\  |
    /    |
        ===""",
    """
     +---+
     O   |
    /|\\  |
    / \\  |
        ==="""
]

# ------------------------------------------------
# Word bank by difficulty
# ------------------------------------------------
WORD_BANK = {
    "easy": ["dog", "cat", "fish", "book", "sun"],
    "medium": ["python", "random", "guitar", "planet", "school"],
    "hard": ["challenge", "algorithm", "mystery", "computer", "developer"]
}

# ------------------------------------------------
# Choose word
# ------------------------------------------------
def choose_word():
    while True:
        level = input("Choose difficulty (easy / medium / hard): ").lower().strip()
        if level in WORD_BANK:
            word = random.choice(WORD_BANK[level])
            return word, level
        print("❌ Invalid choice. Please type: easy, medium, or hard.\n")

# ------------------------------------------------
# Display game state
# ------------------------------------------------
def display_state(secret_word, hidden_word, guessed_letters, lives, max_lives):
    stage_index = max_lives - lives
    stage_index = min(stage_index, len(HANGMAN_PICS)-1)
    print(HANGMAN_PICS[stage_index])

    colored_word = ""
    for i, letter in enumerate(hidden_word):
        if letter == "_":
            colored_word += YELLOW + "_" + RESET + " "
        else:
            colored_word += GREEN + letter + RESET + " "
    print("Word: ", colored_word.strip())

    colored_guesses = " ".join([RED + l + RESET if l not in hidden_word else GREEN + l + RESET for l in guessed_letters])
    print("Guessed letters: ", colored_guesses)
    print(f"Lives left: {lives}\n")

# ------------------------------------------------
# Hint system
# ------------------------------------------------
def give_hint(secret_word, hidden_word):
    for i, letter in enumerate(hidden_word):
        if letter == "_":
            print(f"💡 Hint: The word contains '{secret_word[i]}' at position {i+1}")
            break

# ------------------------------------------------
# Main Game
# ------------------------------------------------
def play_hangman():
    print("🎉 Welcome to Hangman! 🎉")
    print("Guess the secret word letter by letter.\n")

    secret_word, level = choose_word()
    hidden_word = ["_"] * len(secret_word)

    lives_dict = {"easy": 6, "medium": 5, "hard": 4}
    lives = max_lives = lives_dict[level]

    guessed_letters = []
    score = 0

    while lives > 0 and "_" in hidden_word:
        display_state(secret_word, hidden_word, guessed_letters, lives, max_lives)
        guess = input("Enter a letter (or type 'hint' for help): ").lower().strip()

        if guess == "hint" and level == "hard":
            give_hint(secret_word, hidden_word)
            continue

        if len(guess) != 1 or not guess.isalpha():
            print("❌ Please enter a single valid letter.\n")
            continue

        if guess in guessed_letters:
            print("⚠️ You already guessed that letter.\n")
            continue

        guessed_letters.append(guess)

        if guess in secret_word:
            occurrences = secret_word.count(guess)
            score += 10 * occurrences
            print(f"✅ Good guess! (+{10*occurrences} points)\n")
            for i, char in enumerate(secret_word):
                if char == guess:
                    hidden_word[i] = guess
        else:
            lives -= 1
            score -= 5
            print(f"❌ Wrong guess! (-5 points)\n")

    # Game over
    display_state(secret_word, hidden_word, guessed_letters, lives, max_lives)

    if "_" not in hidden_word:
        bonus = lives * 5
        score += bonus
        print(GREEN + f"🎉 Congratulations! You guessed the word: {secret_word}" + RESET)
        print(GREEN + f"🏆 Bonus for remaining lives: +{bonus} points" + RESET)
    else:
        print(RED + f"💀 Game Over! The word was: {secret_word}" + RESET)

    print(CYAN + f"💰 Your final score: {score}" + RESET)

    replay = input("\nDo you want to play again? (yes/no): ").lower().strip()
    if replay.startswith("y"):
        print("\n" + "="*40 + "\n")
        play_hangman()
    else:
        print("👋 Thanks for playing Hangman! Goodbye!")

# ------------------------------------------------
# Run the game
# ------------------------------------------------
if __name__ == "__main__":
    play_hangman()