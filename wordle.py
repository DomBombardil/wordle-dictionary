import json
import re
from pathlib import Path
import random


class Wordle:
    def __init__(self):        
        self.path = Path("wordle_translations.json")
    
    def __repr__(self):
        return f'Wordle(path="{self.path}")'
    
    def main_menu(self):
        while True:
            print("\n--- Wordle Menu ---")
            print("1. Create a new entry")
            print("2. Read all entries")
            print("3. Search for an entry")
            print("4. Play the Wordle game")
            print("5. Exit")

            choice = input("Choose an option (1-5): ").strip()

            if choice == '1':
                self.create_entry()
            elif choice == '2':
                self.read_entries()
            elif choice == '3':
                self.search_entry()
            elif choice == '4':
                self.play_system()
            elif choice == '5':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")

    def create_entry(self):
        de = input("Enter the German word: ").strip()
        hr = input("Enter the Croatian translation: ").strip().lower()

        try:
            data = self._read_file()
        
        except FileNotFoundError:
            data = {}

        if de in data or hr in data.values():
            print("This entry already exists.")
            return
        
        data[de] = hr

        self._write_text(data)

    def read_entries(self):
        try:
            data = self._read_file()
        
        except FileNotFoundError:
            print("No entries found.")
            return
        
        if not data:
            print("No entries found.")
            return
        
        for de, hr in data.items():
            print(f"German: {de} - Croatian: {hr}")

    def search_entry(self):
        term = input(
            "Enter the German or Croatian word to search: ").strip().lower()

        data = self._read_file()
        
        found = False
        for de, hr in data.items():
            if term == de.lower() or term == hr.lower():
                print(f"Found: German: {de} - Croatian: {hr}")
                found = True
            
                if not found:
                    print("Entry not found.")
                    add_entry = input(
                        "Would you like to add it? (y/n): ").strip().lower()
                    if add_entry == 'y':
                        self.create_entry()
                        break
                    if add_entry == 'n':
                        print("No entry added.")
                        break

    def _read_file(self):
        try: 
            data = json.loads(self.path.read_text(encoding='utf-8'))
            return data
        
        except FileNotFoundError:
            print("File missing")

    def _write_text(self, data):
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=4)
                             , encoding="utf-8")
        print("Entry added successfully.")

    def play_system(self):
        """A function that shows the user a word in german and 
        asks for the croatian translation."""
        data = self._read_file()
        
        de_word, hr_word = random.choice(list(data.items()))

         # Split accepted answers by common delimiters and strip whitespace.
        accepted_answers = self._split_accepted_answers(data)[de_word]
        
        print(f"What is the Croatian translation for '{de_word}'?")
        user_answer = input("If you need a hint, type 'hint'. ").strip().lower()
        
        while True:
            if user_answer == 'hint':
                # Provide a hint by showing the first letter and masking the rest.
                hints = [
                    word[0] + ' '.join(['_ ' for _ in word[1:]])
                    for word in accepted_answers
                ]
                
                print(f"Here is your hint: {hints}")
                user_answer = input(f"Now, please enter your answer: ").strip().lower()                

            if user_answer in accepted_answers:
                print(f"Correct! {user_answer} is the correct translation of the word {de_word}.")
                print(f"Congratulations! Other answers include: {', '.join(accepted_answers)}")
                return

            elif user_answer == "":
                print(f"You did not provide an answer. The correct translation is '{hr_word}'.")
                return
                
            else:
                print(f"Incorrect. The correct translation is '{hr_word}'.")
                add_to_accepted = input(
                    f"Should I add this translation to the accepted answers? (y/n): ").strip().lower()
                if add_to_accepted == 'y':
                    self._write_text({**data, de_word: hr_word + ', ' + user_answer})
                    print("Entry updated successfully.")
                else:
                    print("Entry not added.")
                return

    def _split_accepted_answers(self, data):
        """A helper function to split accepted answers by common delimiters."""
        split_data = {}

        for de, hr in data.items():
            split_answers = [
                part.strip().lower() for part in re.split(r'[,/;]', hr)
            ]
            split_data[de] = split_answers
        return split_data
    


        


    
