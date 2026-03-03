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
        self.menu_frame = tk.Frame(self.root)
        self.game_frame = tk.Frame(self.root)
        self.add_frame = tk.Frame(self.root)
        self.dictionary_frame = tk.Frame(self.root)

        # Main menu buttons and labels.
        self.mm_tl = tk.Label(self.menu_frame, text='Click on a "New game" to start.')
        self.mm_bl = tk.Label(self.menu_frame, text="Or check out the dictionary and add a new entry.")
        self.nr_b = tk.Button(self.menu_frame, text="New Game", command=self.new_round)
        self.ae_b = tk.Button(self.menu_frame, text="Create Entry", command=self.create_entry)
        self.tree_b = tk.Button(self.menu_frame, text="Dictionary", command=self.words_list)
        self.user_input = tk.Entry(self.menu_frame)

        self.mm_tl.pack()
        self.mm_bl.pack()
        self.nr_b.pack()
        self.ae_b.pack()
        self.tree_b.pack()

        # Game buttons and labels.
        self.ng_tl = tk.Label(self.game_frame, text=f"Translate: ")
        self.ng_bl = tk.Label(self.game_frame, text='To confirm press "Enter", to quit press "ESC"')
        self.nw_b = tk.Button(self.game_frame, text="New Word", command=self.new_round)
        self.ca_b = tk.Button(self.game_frame, text="Check answer", command=self.check_answer)
        self.hint_b = tk.Button(self.game_frame, text="Hint", command=self.hint)
        self.game_input = tk.Entry(self.game_frame)

        self.ng_tl.pack()
        self.ng_bl.pack()
        self.game_input.pack()
        self.nw_b.pack()
        self.hint_b.pack()
        self.ca_b.pack()

        # Add entry buttons and labels.
        self.add_en_b = tk.Button(self.add_frame, text="Add Entry", command=self.next_step)
        self.add_en_tl = tk.Label(self.add_frame, text='Write a German word you would like to save')
        self.add_en_bl = tk.Label(self.add_frame, text='Press "Enter" to continue, "ESC" to return to main menu.')
        self.add_entry_input = tk.Entry(self.add_frame)

        self.add_en_tl.pack()
        self.add_entry_input.pack()
        self.add_en_bl.pack()
        self.add_en_b.pack()

        # Dictionary view
        self.tree = ttk.Treeview(self.dictionary_frame, columns=("German", "Croatian"), show="headings")
        self.tree.heading("German", text="German")
        self.tree.heading("Croatian", text="Croatian")
        
        self.scrollbar = ttk.Scrollbar(self.dictionary_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar)
        self.tree.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.dictionary_input = tk.Entry(self.dictionary_frame)
        self.dictionary_input.pack()

        # App state
        self.state = "IDLE"
        self._handle_frame_switching()
        self._handle_key_presses()

    def words_list(self):
        """A function to display all saved words."""
        self.state = "DICTIONARY_OPEN"
        self.root.geometry("600x600")
        self._handle_frame_switching()
        self._handle_key_presses()
        self.dictionary_input.delete(0, tk.END)
        self.dictionary_input.focus()
        self.tree.delete(*self.tree.get_children())
        all_words = self.backend.read_entries()

        for de, hr in all_words:
            self.tree.insert("", "end", values=(de, hr))

    def word_search(self, event=None):
        """A function to search wanted word inside a dictionary"""
        searched_word = self.dictionary_input.get()

        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            if searched_word in values:
                self.tree.selection_set(item)
                self.tree.see(item)
                break

    def new_round(self):
        """A function to start a new round."""
        if self.state != "PLAYING":
            self.state = "PLAYING"
            self._handle_frame_switching()
            self._handle_key_presses()

        try:
            de_word, accepted = self.backend.new_round()

            self.current_de_word = de_word
            self.current_acepted_answers = accepted
            
            self.ng_tl.config(text=f"Translate: {de_word}")
            self.ng_bl.config(text='Press Enter or "Check Answer" to advance.')

            self.game_input.delete(0, tk.END)
            self.game_input.focus()

        except WordleError as e:
            messagebox.showerror("Backend Error", str(e))
        
    def check_answer(self, event=None):
        """A function to check the validity of the answer"""
        self._handle_key_presses()
        if self.current_de_word is None:
            messagebox.showinfo("Info","Start the round first")

        user_answer = self.game_input.get()

        try:
            if self.backend.check_answer(user_answer, self.current_acepted_answers):
                self.ng_bl.config(text=f'Correct! Here are all of the accepted answers: {", ".join(self.current_acepted_answers)}')

            elif user_answer == "":
                self.ng_bl.config(text=f'The aproved answers are: {", ".join(self.current_acepted_answers)}') 

            else:
                self.ng_bl.config(text=f'Incorrect! The aproved answers are: {", ".join(self.current_acepted_answers)}') 
        
        except WordleError as e:
            messagebox.showerror("Backend Error", str(e))

    def hint(self, event=None):
        """A function to show a hint to the user."""
        self._handle_key_presses()
        current_hint = self.backend.show_hint(self.current_acepted_answers)
        self.ng_bl.config(text=f'Hint: {", ".join(current_hint)}')

    def create_entry(self):
        """A function to create a German dictionary entry."""
        if self.state != "CREATING_DE":
            self.state = "CREATING_DE"
            self._handle_frame_switching()
            self._handle_key_presses()
            self.add_entry_input.focus()
            self.add_en_b.config(command=self.next_step)

        self.add_en_tl.config(text='Write a German word you would like to save')
        self.add_en_bl.config(text='Press "Enter" to continue, "ESC" to return to main menu.')

    def next_step(self, event=None):
        """A function to create a Croatian counterpart entry."""
        self.state = "CREATING_HR"
        self._handle_key_presses()
        self.de_word = self.add_entry_input.get()

        self.add_entry_input.delete(0, tk.END)
        self.add_entry_input.focus()

        self.add_en_tl.config(text='Write a Croatian counterpart') 
        self.add_en_b.config(command=self.final_step)

    def final_step(self, event=None):
        """A function to save both entries"""
        self.state = "SAVING_ENTRY"
        self._handle_key_presses()

        try :
            self.hr_word = self.add_entry_input.get()
            self.backend.create_entry(self.de_word, self.hr_word)
            self.add_en_tl.config(text="Entry saved succesfuly!")
            self.add_en_bl.config(text='Press "Enter" or "ESC" to return to main menu.')
            self.add_en_b.config(text="Return to Main Menu", command=self.reset)

        except WordleError as e:
            self.reset()
            messagebox.showerror("Backend error", str(e))

    def reset(self, event=None):
        """Reset all the values and quit the started process."""
        # Reset the current state.
        self.state = "IDLE"
        self._handle_frame_switching()
        self._handle_key_presses()
        self.add_en_b.config(command=self.create_entry)

        self.current_de_word = None 
        self.current_acepted_answers = None 

        self.root.geometry("600x200")

    def _handle_key_presses(self):
        """A function to handle key bindings depending on the state"""
        self.root.bind("<Escape>", self.reset)
        # Using lambda here because root.destroy() takes onyl one positional agrument.
        self.root.bind("<q>", lambda x:self.root.destroy())

        if self.state == "PLAYING":
            self.game_input.bind("<Return>", self.check_answer)
        
        if self.state == "CREATING_DE":
            self.add_entry_input.bind("<Return>", self.next_step)

        if self.state == "CREATING_HR":
            self.add_entry_input.bind("<Return>", self.final_step)

        if self.state == "SAVING_ENTRY":
            self.add_entry_input.bind("<Return>", self.reset)

        if self.state == "DICTIONARY_OPEN":
            self.dictionary_input.bind("<Return>", self.word_search)

    def _handle_frame_switching(self):
        """A function to switch frames depending on the game state."""
        self.game_frame.pack_forget()
        self.add_frame.pack_forget()
        self.menu_frame.pack_forget()
        self.dictionary_frame.pack_forget()

        if self.state == "IDLE":
            self.menu_frame.pack(fill="both", expand=True)

        elif self.state == "PLAYING":
            self.game_frame.pack(fill="both", expand=True)

        elif self.state in ("CREATING_DE", "CREATING_HR", "SAVING_ENTRY"):
            self.add_frame.pack(fill="both", expand=True)

        elif self.state == "DICTIONARY_OPEN":
            self.dictionary_frame.pack(fill="both", expand=True)

        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = WordleApp(root)
    root.mainloop()

            