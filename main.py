import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"

# data = None

# ------------------   Reading Data ----------------------


# -----------------------  Next ---------------------------

def right_click():
    global data
    new_data = data.drop(data.index[data.French == french_word])
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def show_answer(_french_word, _data):
    english_word = _data[_data.French == _french_word].English.item()
    canvas.itemconfig(canvas_image, image=back_card_img)
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word_displayed, text=english_word, fill="white")


def next_card():
    # To avoid the card flip when we press many times on nex card
    global flipper, data, french_word
    window.after_cancel(flipper)

    try:
        data = pandas.read_csv("data/words_to_learn.csv")
    except FileNotFoundError:
        data = pandas.read_csv("data/french_words.csv")

    french_word = random.choice(data.French)
    canvas.itemconfig(canvas_image, image=front_card_img)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(word_displayed, text=french_word, fill="black")
    flipper = window.after(3000, show_answer, french_word, data)


# ----------------------- UI ------------------------------
window = Tk()
window.title("My flash cards")
window.config(padx=50, pady=10, bg=BACKGROUND_COLOR)
flipper = window.after(3000, show_answer)

canvas = Canvas(width=800, height=530, bg=BACKGROUND_COLOR, highlightthickness=0)
back_card_img = PhotoImage(file="images/card_back.png")
front_card_img = PhotoImage(file="images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=front_card_img)
language = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
word_displayed = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_btn = Button(image=wrong_img, bd=0, highlightthickness=0, command=next_card)
wrong_btn.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
right_btn = Button(image=right_img, bd=0, highlightthickness=0, command=right_click)
right_btn.grid(row=1, column=1)

next_card()

window.mainloop()
