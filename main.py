import csv
from tkinter import *
import pandas as pd
from random import choice
import os
import sys

# use this directory when generating exe file
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

# card_back_img_dir = application_path + "/images/card_back.png"
# card_front_img_dir = application_path + "/images/card_front.png"
# right_button_img_dir = application_path + "/images/right.png"
# wrong_button_img_dir = application_path + "/images/wrong.png"
# words_dir = application_path + "/data/english_indonesia_words.csv"
# word_to_learn_dir = application_path + "/data/word_to_learn.csv"

card_back_img_dir = "images/card_back.png"
card_front_img_dir = "images/card_front.png"
right_button_img_dir = "images/right.png"
wrong_button_img_dir = "images/wrong.png"
words_dir = "data/english_indonesia_words.csv"
word_to_learn_dir = "data/word_to_learn.csv"

BACKGROUND_COLOR = "#B1DDC6"


def word_known():
    global current_card
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv(word_to_learn_dir, index=False)
    next_card()


def next_card():
    global current_card
    global timer
    current_card = choice(to_learn)
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")
    window.after_cancel(timer)
    timer = window.after(3000, flip_card)


def flip_card():
    global current_card
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(card_title, text="Indonesia", fill="white")
    canvas.itemconfig(card_word, text=current_card["Indonesia"], fill="white")


try:
    data = pd.read_csv(word_to_learn_dir)
except FileNotFoundError:
    data = pd.read_csv(words_dir)
finally:
    to_learn = data.to_dict(orient="records")

window = Tk()
window.title("English-Indonesia Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card_front_img = PhotoImage(file=card_front_img_dir)
card_back_img = PhotoImage(file=card_back_img_dir)
canvas = Canvas(width=800, height=526)
canvas_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

wrong_button_img = PhotoImage(file=wrong_button_img_dir)
wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

right_button_img = PhotoImage(file=right_button_img_dir)
right_button = Button(image=right_button_img, highlightthickness=0, command=word_known)
right_button.grid(row=1, column=1)

current_card = choice(to_learn)
timer = window.after(0, flip_card)
next_card()


window.mainloop()
