import tkinter as tk
from tkinter import ttk, messagebox
from wordle_backend import WordleBackend, WordleError

class WordleApp():
    """A class that represents the wordle app."""
    def __init__(self, root):
        self.root = root
        self.root.title("Worlde Dictionary")
        self.root.geometry("600x200")

        # Backend integration
        self.backend = WordleBackend("wordle_translations.json")

        # Round state
        self.current_de_word = None
        self.current_acepted_answers = None

        # UI Widgets
        self.word_lbl = tk.Label(root, text='Click on a "New game" to start') 
        self.word_lbl.pack()

        self.user_input = tk.Entry(root)
        self.user_input.pack()

        self.result_lbl = tk.Label(root, text='Or click on an Add entry to add a new word to the dictionary')
        self.result_lbl.pack()

        self.nr_b = tk.Button(root, text="New Game", command=self.new_round)
        self.ae_b = tk.Button(root, text="Add entry", command=self.create_entry)
        self.ca_b = tk.Button(root, text="Check answer", command=self.check_answer)
        self.hint_b = tk.Button(root, text="Hint", command=self.hint)

        self.nr_b.pack()
        self.ae_b.pack()


        self.user_input.bind("<Escape>", self.reset)

        # App state
        self.state = "IDLE"

    def new_round(self):
        """A function to start a new round."""
        self.state = "PLAYING"

        self.user_input.bind("<Return>", self.check_answer)
        self.nr_b.config(text="New word")
        self.ca_b.pack()
        self.hint_b.pack()
        self.ae_b.pack_forget()

        try:
            de_word, accepted = self.backend.new_round()

            self.current_de_word = de_word
            self.current_acepted_answers = accepted

            self.word_lbl.config(text=f"Translate: {de_word}")
            self.result_lbl.config(text='To confirm press "Enter", to quit press "ESC"')

            self.user_input.delete(0, tk.END)
            self.user_input.focus()

        except WordleError as e:
            messagebox.showerror("Backend Error", str(e))
        
    def check_answer(self, event=False):
        """A function to check the validity of the answer"""
        self.state = "PLAYING"

        self.user_input.bind("<Escape>", self.reset)

        if self.current_de_word is None:
            messagebox.showinfo("Info","Start the round first")

        user_answer = self.user_input.get()

        try:
            if self.backend.check_answer(user_answer, self.current_acepted_answers):
                self.result_lbl.config(text=f'Correct! Here are all of the accepted answers: {", ".join(self.current_acepted_answers)}')

            elif user_answer == "":
                self.result_lbl.config(text=f'The aproved answers are: {", ".join(self.current_acepted_answers)}') 

            else:
                self.result_lbl.config(text=f'Incorrect! The aproved answers are: {", ".join(self.current_acepted_answers)}') 
        
        except WordleError as e:
            messagebox.showerror("Backend Error", str(e))

    def hint(self, event=False):
        """A function to show a hint to the user."""
        self.state = "PLAYING"

        current_hint = self.backend.show_hint(self.current_acepted_answers)
        self.result_lbl.config(text=f'Hint: {", ".join(current_hint)}')

    def create_entry(self):
        """A function to create a German dictionary entry."""
        self.state = "CREATING"

        self.word_lbl.config(text='Write a German word you would like to save')
        self.result_lbl.config(text='Press "Enter" to continue, "ESC" to return to main menu.')

        self.user_input.bind("<Return>", self.next_step)

        self.nr_b.pack_forget()
        self.ae_b.config(command=self.next_step)

    def next_step(self, event=False):
        """A function to create a Croatian counterpart entry."""
        self.state = "CREATING_DE"

        self.de_word = self.user_input.get()

        self.user_input.delete(0, tk.END)
        self.user_input.focus

        self.word_lbl.config(text='Write a Croatian counterpart') 

        self.user_input.unbind("<Return>")
        self.user_input.bind("<Return>", self.final_step)
            
        self.ae_b.config(command=self.final_step)
        
    def final_step(self, event=False):
        """A function to save both entries"""
        self.state = "CREATING_HR"

        try :
            self.hr_word = self.user_input.get()
            self.backend.create_entry(self.de_word, self.hr_word)

            self.word_lbl.config(text="Entry saved succesfuly!")
            self.user_input.unbind("<Return>")

        except WordleError as e:
            self.reset()
            messagebox.showerror("Backend error", str(e))

    def reset(self, event):
        """Reset all the values and quit the started process."""
        # Reset the current state.
        self.state = "IDLE"
        self.current_de_word = None 
        self.current_acepted_answers = None 

        # Reset all text and user input.
        self.user_input.delete(0, tk.END)
        self.word_lbl.config(text='Click on a "New game" to start')
        self.result_lbl.config(text='Or click on an Add entry to add a new word to the dictionary')

        # Reset all the keybinds.
        self.user_input.unbind("<Return>")

        # Reset the button configuration.
        self.ca_b.pack_forget()
        self.hint_b.pack_forget()
        self.ae_b.pack_forget()
        self.nr_b.config(text="New Game")
        self.nr_b.pack()
        self.ae_b.config(command=self.create_entry)
        self.ae_b.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = WordleApp(root)
    root.mainloop()

            