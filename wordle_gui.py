import tkinter as tk
from tkinter import ttk, messagebox
from wordle_backend import WordleBackend, WordleError

class WordleApp():
    """A class that represents the wordle app."""
    def __init__(self, root):
        self.root = root
        self.root.title("Worlde Dictionary")

        # Backend integration
        self.backend = WordleBackend("wordle_translations.json")

        # Round state
        self.current_de_word = None
        self.current_acepted_answers = None

        # UI Widgets
        self.word_lbl = tk.Label(root, name='click on a "New game" to start') 
        self.word_lbl.pack()

        self.user_answer = tk.Entry(root)
        self.user_answer.pack()

        self.result_lbl = tk.Label(root, text="")
        self.result_lbl.pack()

        tk.Button(root, text="New round", command=self.new_round).pack()
        tk.Button(root, text="Check answer", command=self.check_answer).pack()

    def new_round(self):
        """A function to start a new round."""
        try:
            de_word, accepted = self.backend.new_round()

            self.current_de_word = de_word
            self.current_acepted_answers = accepted

            self.word_lbl.config(text=f"Translate: {de_word}")
            self.result_lbl.config(text="")

            self.user_answer.delete(0, tk.END)
            self.user_answer.focus()

        except WordleError as e:
            messagebox.showerror("Backend Error", str(e))
    
    def check_answer(self):
        """A function to check the validity of the answer"""
        if self.current_de_word is None:
            messagebox.showinfo("Info", "Start the round first")

        user_answer = self.user_answer.get()

        try:
            if self.backend.check_answer(user_answer, self.current_acepted_answers):
                self.result_lbl.config(text=f"Correct! these are all the accepted answers: {self.current_acepted_answers}") 
            else:
                self.result_lbl.config(text=f"Incorrect! the aproved answers are: {self.current_acepted_answers}")
        
        except WordleError as e:
            messagebox.showerror("Backend Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = WordleApp(root)
    root.mainloop()

            