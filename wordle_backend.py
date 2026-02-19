import json
import re
from pathlib import Path
import random

class WordleError(Exception):
    """Base class for exceptions in this module."""
    pass

class DuplicateEntryError(WordleError):
    """Raised when an entry already exists in the dictionary."""
    pass

class InvalidEntryError(WordleError):
    """Raised when an entry is invalid (e.g., empty or whitespace)."""
    pass

class EntryNotFoundError(WordleError):
    """Raised when an entry is not found in the dictionary."""
    pass

class Wordle:
    def __init__(self):        
        self.path = (
        Path.home() 
        / "Documents" 
        / "Python_programming" 
        / "python_work" 
        / "RealPython_learning" 
        / "REPL_interactive_sessions"
        / "Wordle" 
        / "wordle_translations.json"
        )
    
    def __repr__(self):
        return f'Wordle(path="{self.path}")'
    
    def create_entry(self, de_word, hr_word):
        de = de_word.strip()
        hr = hr_word.strip().lower()

        if not de or not hr:
            raise InvalidEntryError("Both German and Croatian words must be non-empty and not just whitespace.")

        try:
            data = self._read_file()
        
        except FileNotFoundError:
            data = {}

        if de in data:
            raise DuplicateEntryError(f"The German word '{de}' already exists in the dictionary.")

        if hr in data.values():
            raise DuplicateEntryError(f"The Croatian word '{hr}' already exists in the dictionary.")
        
        data[de] = hr

        self._write_text(data)

    def read_entries(self):
        data = self._read_file()
        return list(data.items())

    def search_entry(self, term):
        term = term.strip().lower()

        data = self._read_file()

        for de, hr in data.items():
            de_norm = de.strip().lower()
            hr_parts = [part.strip().lower() for part in re.split(r'[,/;]', hr) if part.strip()]

            if term == de_norm or term in hr_parts:
                return de, hr

        raise EntryNotFoundError(f"The term '{term}' was not found in the dictionary.")

    def _read_file(self):
        # Read the JSON file and return the data as a dictionary.
        try: 
            data = json.loads(self.path.read_text(encoding='utf-8'))
            return data

        # If the file does not exist, return an empty dictionary.
        except FileNotFoundError:
            return {}
            
        # Except a corupted file or invalid JSON
        except json.JSONDecodeError as e:
            raise WordleError(f"Dictionary file is corrupted.") from e

    def _write_text(self, data):
        text = json.dumps(data, ensure_ascii=False, indent=4)
        self.path.write_text(text, encoding="utf-8")
        
    def new_round(self):
        """Start a new round by selecting a random German word, and let the player guess the Croatian translation."""
        data = self._read_file()
        if not data:
            raise WordleError("The dictionary is empty. Please add some entries before starting a new round.")

        de_play_word = random.choice(list(data.keys()))
        accepted_answers = self._split_accepted_answers(data[de_play_word]) 
        return de_play_word, accepted_answers

    def show_hint(self, accepted_answers):
        hint = [
            word[0] + ' '.join(['_' for _ in word[1:]])
            for word in accepted_answers
        ]
        return hint 

    def check_answer(self, user_answer, accepted_answers):
        """A function to determine if the user answer is correct"""
        return user_answer.strip().lower() in accepted_answers

    def _split_accepted_answers(self, data):
        """A helper function to split accepted answers by common delimiters."""
        split_data = {}

        for de, hr in data.items():
            split_answers = [
                part.strip().lower() for part in re.split(r'[,/;]', hr) if part.strip()
            ]
            split_data[de] = split_answers
        return split_data
    

        


    
