import random

# Class to manage reusable elements
class GuessTheWordGame:
    def __init__(self):
        self.dictionary = "dictionary.txt"
        self.score = 0
        self.round = 1
        self.max_attempts = 3
    
    def load_dictionary(self):
    # Load dictionary and filter words with 6 letters or less.
        try:
            with open(self.dictionary, 'r') as f:
                words = [
                    line.strip() for line in f
                    if line.strip() and len(line.strip()) <= 6
                ]
                print(words)
            if not words:
                raise ValueError("No valid words in dictionary!")
            return words
        except FileNotFoundError:
            print("Dictionary file not found!")
            return []
        except ValueError as e:
            print(e)
            return []
    
    def shuffle_word(self, word):
        """Shuffle the letters of a word."""
        shuffled = list(word)
        random.shuffle(shuffled)
        return ''.join(shuffled)
    
    def validate_guess(self, guess, actual_word):
        """Check if the guess is valid."""
        if len(guess) != len(actual_word):
            return False, "Your word must use all letters!"
        elif guess not in self.dictionary:
            return False, "Invalid word! Make sure it's a real word."
        return True, ""
    
    def play_round(self):
        """Play a single round."""
        # Choose a random word
        actual_word = random.choice(self.dictionary)
        shuffled_word = self.shuffle_word(actual_word)
        
        print(f"\nRound {self.round}")
        print(f"Guess the word: {shuffled_word}")
        print(f"(Hint: {actual_word})")  # This can be removed for challenge
        
        attempts = self.max_attempts
        
        while attempts > 0:
            guess = input(f"Attempt {self.max_attempts - attempts + 1}/{self.max_attempts}: ").strip()
            is_valid, message = self.validate_guess(guess, actual_word)
            
            if not is_valid:
                print(f"Error: {message}")
                continue  # Retry same attempt without decrementing
            
            if guess == actual_word:
                print(f"Correct! You earned {len(actual_word)} points.")
                self.score += len(actual_word)
                return
            
            print("Incorrect guess! Try again.")
            attempts -= 1
        
        print(f"Out of attempts! The word was: {actual_word}")
    
    def start_game(self):
        """Start the game."""
        if not self.dictionary:
            print("Game cannot start. No words available!")
            return
        
        total_rounds = 2
        while self.round <= total_rounds:
            self.play_round()
            self.round += 1
        
        print(f"\nGame Over! Your total score: {self.score}")

# Main execution
if __name__ == "__main__":
    game = GuessTheWordGame()
    game.start_game()

