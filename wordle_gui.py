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

        self.nr_b = tk.Button(root, text="New round", command=self.new_round)
        self.ae_b = tk.Button(root, text="Add entry", command=self.create_entry)
        self.ca_b = tk.Button(root, text="Check answer", command=self.check_answer)

        self.nr_b.pack()
        self.ae_b.pack()

    def new_round(self):
        """A function to start a new round."""
        self.user_input.bind("<Escape>", self.reset)
        self.user_input.bind("<Return>", self.check_answer)
        self.ca_b.pack()
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
        self.user_input.bind("<Escape>", self.reset)

        if self.current_de_word is None:
            messagebox.showinfo("Info","Start the round first")

        user_answer = self.user_input.get()

        try:
            if self.backend.check_answer(user_answer, self.current_acepted_answers):
                self.result_lbl.config(text=f'Correct! these are all the accepted answers: {", ".join(self.current_acepted_answers)}')
            else:
                self.result_lbl.config(text=f'Incorrect! the aproved answers are: {", ".join(self.current_acepted_answers)}') 
        
        except WordleError as e:
            messagebox.showerror("Backend Error", str(e))

    def create_entry(self):
        """A function to create a German dictionary entry."""
        try:
            self.word_lbl.config(text='Write a German word you would like to save, and press "Enter" to continue, "ESC" to quit. ')
            self.user_input.bind("<Return>", self.next_step)
            self.user_input.bind("<Escape>", self.reset)
        except WordleError as e:
            messagebox.showerror("Backend error", str(e))

    def next_step(self, event):
        """A function to create a Croatian counterpart entry."""
        try:
            self.de_word = self.user_input.get()

            self.user_input.delete(0, tk.END)
            self.user_input.focus

            self.word_lbl.config(text='Write a Croatian counterpart and press "Enter" to save the entry "ESC" to quit. ')

            self.user_input.unbind("<Return>")
            self.user_input.bind("<Return>", self.final_step)
            self.user_input.bind("<Escape>", self.reset)
            
        except WordleError as e:
            messagebox.showerror("Backend error", str(e))    

    def final_step(self, event):
        """A function to save both entries"""
        self.hr_word = self.user_input.get()
        self.backend.create_entry(self.de_word, self.hr_word)

        self.word_lbl.config(text="Entry saved succesfuly!")
        self.user_input.unbind("<Return>")

    def reset(self, event):
        """Reset all the values and quit the started process."""
        # Reset all text and user input.
        self.user_input.delete(0, tk.END)
        self.word_lbl.config(text="")
        self.result_lbl.config(text="")

        # Reset all the keybinds.
        self.user_input.unbind("<Return>")
        self.user_input.unbind("<Escape>")

        # Reset the button configuration.
        self.ca_b.pack_forget()
        self.ae_b.pack()

        # Reset the current state.
        self.current_de_word = False
        self.current_acepted_answers = False
        
if __name__ == "__main__":
    root = tk.Tk()
    app = WordleApp(root)
    root.mainloop()

            