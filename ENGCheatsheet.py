import random
import json
import time
from tkinter import Tk, Label, Button, Entry, Text, Scrollbar, Frame, CENTER
class EnglishNote:

    def __init__(self, master):
        self.word_dict = {}
        self.load_data()
        self.root = master
        self.root.title("English CheatSheet")
        self.root.geometry("500x500")

        # GUI elements
        self.label = Label(self.root, text="Choose an option:")
        self.label.pack()

        self.button_add = Button(self.root, text="Add a Word", command=self.add_word)
        self.button_add.pack(side="top", anchor=CENTER)

        self.button_delete = Button(self.root, text="Delete a Word", command=self.del_word)
        self.button_delete.pack(side="top", anchor=CENTER)

        self.button_see = Button(self.root, text="See the Words", command=self.see_word)
        self.button_see.pack(side="top", anchor=CENTER)

        self.button_quiz = Button(self.root, text="Play Quiz", command=self.quiz)
        self.button_quiz.pack(side="top", anchor=CENTER)

        self.button_exit = Button(self.root, text="Exit", command=self.exit_program)
        self.button_exit.pack(side="top", anchor=CENTER)


    def add_word(self):
        add_window = Tk()
        add_window.title("Add a Word")
        add_window.geometry("500x300")

        label_eng = Label(add_window, text="English word:")
        label_eng.pack()

        entry_eng = Entry(add_window)
        entry_eng.pack()

        label_kor = Label(add_window, text="Meaning:")
        label_kor.pack()

        entry_kor = Entry(add_window)
        entry_kor.pack()

        def save_word():
            eng = entry_eng.get()
            kor = entry_kor.get()
            self.word_dict[eng] = kor
            self.save_data()
            print("Added successfully.")
            add_window.destroy()

        button_save = Button(add_window, text="Save", command=save_word)
        button_save.pack()

    def del_word(self):
        del_window = Tk()
        del_window.title("Delete a Word")
        del_window.geometry("500x300")

        label_eng = Label(del_window, text="English word to delete:")
        label_eng.pack()

        entry_eng = Entry(del_window)
        entry_eng.pack()

        def delete_word():
            eng = entry_eng.get()
            if eng in self.word_dict:
                del self.word_dict[eng]
                self.save_data()
                print("Deleted successfully.")
                del_window.destroy()
            else:
                print("The word is not in the list.")

        button_delete = Button(del_window, text="Delete", command=delete_word)
        button_delete.pack()

    def see_word(self):
        see_window = Tk()
        see_window.title("English Words")
        see_window.geometry("800x800")

        frame = Frame(see_window)
        frame.pack(expand=True, fill="both")

        scrollbar = Scrollbar(frame, orient="vertical")
        textbox = Text(frame, wrap="none", yscrollcommand=scrollbar.set, width=50, height=15)

        for eng, kor in self.word_dict.items():
            textbox.insert("end", f"{eng}: {kor}\n")

        scrollbar.config(command=textbox.yview)
        scrollbar.pack(side="right", fill="y")
        textbox.pack(side="left", fill="both", expand=True)

        def close_window():
            see_window.destroy()

        button_close = Button(see_window, text="Close", command=close_window)
        button_close.pack()

    def quiz(self):
        quiz_window = Tk()
        quiz_window.title("Quiz")
        quiz_window.geometry("500x300")

        random_pair = random.choice(list(self.word_dict.items()))
        random_word = random_pair[0]

        label_quiz = Label(quiz_window, text=f"Meaning: {random_pair[1]}")
        label_quiz.pack()

        entry_guess = Entry(quiz_window)
        entry_guess.pack()

        trial_label = Label(quiz_window, text="Tries remaining: 3")
        trial_label.pack()

        def check_guess():
            guess = entry_guess.get()
            nonlocal random_word
            nonlocal random_pair

            if random_word == guess:
                result_label.config(text="Correct!")
                quiz_window.after(2000, lambda: quiz_window.destroy())
            else:
                trial_label.config(text=f"Tries remaining: {int(trial_label.cget('text')[-1]) - 1}")
                if int(trial_label.cget('text')[-1]) == 0:
                    result_label.config(text="You should study harder.")
                    quiz_window.after(2000, lambda: quiz_window.destroy())
                else:
                    random_pair = random.choice(list(self.word_dict.items()))
                    random_word = random_pair[0]
                    label_quiz.config(text=f"Meaning: {random_pair[1]}")
                    entry_guess.delete(0, "end")

        button_check = Button(quiz_window, text="Check", command=check_guess)
        button_check.pack()

        result_label = Label(quiz_window, text="")
        result_label.pack()

    def exit_program(self):
        self.root.destroy()

    def load_data(self):
        try:
            with open('word_data.json', 'r') as file:
                self.word_dict = json.load(file)
        except FileNotFoundError:
            # Initialize an empty dictionary if the file doesn't exist
            self.word_dict = {}

    def save_data(self):
        with open('word_data.json', 'w') as file:
            json.dump(self.word_dict, file)


root = Tk()
english_note = EnglishNote(root)
root.mainloop()
