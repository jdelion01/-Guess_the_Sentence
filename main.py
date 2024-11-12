import random
import tkinter as tk
from tkinter import simpledialog, messagebox


# Reads sentences from a file, gracefully handles errors
def read_sentences():
    try:
        with open("sentences.txt", "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        messagebox.showerror("Error", "sentences.txt file not found.")
        return []
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading sentences.txt: {e}")
        return []


# Class for Guess the Sentence Game
class GuessSentence:
    def __init__(self):
        self.sentences = read_sentences()
        self.scores = self.load_scores()

        # Setting up the main game window
        self.root = tk.Tk()
        self.root.title("Welcome to Guess the Sentence Game")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        # Buttons for starting the game, viewing top scores, quitting, and adding a sentence
        self.play_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.play_button.pack(pady=15)

        self.top_button = tk.Button(self.root, text="Top Scores", command=self.top_scores)
        self.top_button.pack(pady=15)

        self.add_sentence_button = tk.Button(self.root, text="Add a Sentence", command=self.add_sentence)
        self.add_sentence_button.pack(pady=15)

        self.quit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.quit_button.pack(pady=15)

        # Create a label to display the hint (initially hidden)
        self.hint_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.hint_label.pack(pady=10)

        # Entry for user guess
        self.guess_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.guess_entry.pack(pady=10)

        # Button to submit guess
        self.submit_button = tk.Button(self.root, text="Submit Guess", command=self.submit_guess)
        self.submit_button.pack(pady=10)

        # Current sentence and player's name will be saved here
        self.current_sentence = None
        self.current_player = None

    # Load scores from the file or return an empty dictionary if file not found
    def load_scores(self):
        try:
            with open("score1.txt", "r") as file:
                return eval(file.read())  # Read scores as dictionary
        except FileNotFoundError:
            return {}
        except Exception as e:
            messagebox.showerror("Error", f"Error loading scores: {e}")
            return {}

    # Save scores to a file
    def save_scores(self):
        try:
            with open("score1.txt", "w") as file:
                file.write(str(self.scores))
        except Exception as e:
            messagebox.showerror("Error", f"Error saving scores: {e}")

    # Generate a hint by showing the first letter of each word in the sentence
    def generate_hint(self, secret_sentence):
        words = secret_sentence.split()
        hint = ' '.join([word[0] + '.' * (len(word) - 1) for word in words])
        return hint

    # Show the hint in the label
    def display_hint(self, secret_sentence):
        hint = self.generate_hint(secret_sentence)
        self.hint_label.config(text=f"Hint: {hint}")

    # Check the player's guess
    def check_guess(self, secret_sentence):
        guess = self.guess_entry.get().strip()
        return guess == secret_sentence

    # Start a new game
    def start_game(self):
        if not self.sentences:
            messagebox.showerror("No Sentences", "No sentences available to play. Please add sentences.")
            return

        player_name = simpledialog.askstring("Name of Player", "Please enter your name:")
        if not player_name:
            messagebox.showerror("Invalid Input", "Name cannot be empty!")
            return

        self.current_player = player_name
        secret_sentence = random.choice(self.sentences)
        self.current_sentence = secret_sentence

        # Clear any previous hint and guesses
        self.hint_label.config(text="")
        self.guess_entry.delete(0, tk.END)

        # Show the hint immediately when the game starts
        self.display_hint(secret_sentence)

        # Disable the submit button until player enters a guess
        self.submit_button.config(state=tk.NORMAL)

    # Submit the player's guess
    def submit_guess(self):
        if self.check_guess(self.current_sentence):
            messagebox.showinfo("Congratulations",
                                f"Congratulations, {self.current_player}! You guessed the sentence correctly.")
            self.scores[self.current_player] = self.scores.get(self.current_player, 0) + 10
            self.save_scores()
        else:
            messagebox.showinfo("Incorrect", "Oops! That's not the correct sentence. Please try again.")

        # After submitting a guess, reset the game for a new round
        self.submit_button.config(state=tk.DISABLED)  # Disable submit button after guess
        self.hint_label.config(text="")  # Clear the hint
        self.guess_entry.delete(0, tk.END)  # Clear the input field

    # Show top scores
    def top_scores(self):
        if not self.scores:
            messagebox.showinfo("No Scores", "No scores available yet.")
            return

        # Sort the scores in descending order
        sorted_scores = sorted(self.scores.items(), key=lambda item: item[1], reverse=True)

        # Format the sorted scores into a string
        scores_str = "\n".join(f"{player}: {score}" for player, score in sorted_scores)

        # Display the top scores in a message box
        messagebox.showinfo("Top Scores", scores_str)

    # Allow the player or admin to add a new sentence
    def add_sentence(self):
        new_sentence = simpledialog.askstring("Add Sentence", "Please enter a new sentence:")
        if new_sentence:
            with open("sentences.txt", "a") as file:
                file.write("\n" + new_sentence.strip())
            self.sentences.append(new_sentence.strip())
            messagebox.showinfo("Success", "Sentence added successfully!")
        else:
            messagebox.showwarning("Invalid Input", "Sentence cannot be empty.")

    # Run the Tkinter main loop
    def run(self):
        self.root.mainloop()


# Main entry point for the game
if __name__ == "__main__":
    game = GuessSentence()
    game.run()
