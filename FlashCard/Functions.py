from tkinter import Canvas, Tk, PhotoImage, Button
import pandas
import random

# -- Read CSV Data --

FROM: str = "French"
TO: str = "English"

data = pandas.read_csv("Learning/Data/french_words.csv").to_dict()
newDict = {data[FROM][key]: data[TO][key] for key in data[FROM]}

unknown: list[str] = [word for word in newDict]

# -- Function --


def IsKnown(word: str):
    unknown.remove(word)


def RandomCard() -> str:
    keyValue: str = random.choice(unknown)
    return keyValue, newDict[keyValue]