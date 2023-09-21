from tkinter import Tk, END, Canvas, PhotoImage, Label, Entry, Button
from messagebox import showerror, showinfo, showwarning
from random import randint, choice, shuffle
from pyperclip import copy
import json


class SaveData:
    def __init__(self, websiteName: str, emailAddress: str, newPassword: str) -> None:
        self.websiteName = websiteName
        self.emailAddress = emailAddress
        self.newPassword = newPassword

        print([self.websiteName, self.emailAddress, self.newPassword])

    def CompileData(self) -> None:
        if self.IsValid():
            dataDict: dict = {
                self.websiteName: {
                    "Email": self.emailAddress,
                    "Password": self.newPassword
                }
            }
            self.DumpData(dataDict)
        else:
            showwarning(
                "Invalid Input!!", "All details must be filled.")

    def IsValid(self) -> bool:
        return "" not in [self.websiteName, self.emailAddress, self.newPassword]

    def DumpData(self, addData: dict):
        try:
            with open("Assets/Data.json", 'r') as readData:
                mainData: dict = json.load(readData)
                mainData.update(addData)

        except FileNotFoundError:
            mainData = addData

        finally:
            with open("Assets/Data.json", 'w') as writeData:
                json.dump(mainData, writeData, indent=4)
                showinfo("Data Added", "Data Saved Successfully!!")


def GeneratePassword() -> str:
    letters: list = [str(letter) for letter in "abcdefghijklmnopqrstuvwxyz"]
    letters.extend([str(letter) for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"])
    numbers: list = [str(number) for number in range(0, 10)]
    symbols: list = [str(symbol) for symbol in "!@#$%^&*)"]

    newPassword: list = [choice(letters)
                         for _ in range(randint(8, 10))]
    newPassword.extend([choice(numbers)
                       for _ in range(randint(2, 4))])
    newPassword.extend([choice(symbols)
                       for _ in range(randint(2, 4))])

    shuffle(newPassword)

    return "".join(newPassword)


def SearchData(searchWeb: str) -> str:
    try:
        with open("Assets/Data.json", 'r') as readData:
            dataDict: dict = json.load(readData)

    except FileNotFoundError:
        showerror("Error", "Data.json file not found.")

    else:
        try:
            return dataDict[searchWeb]["Password"]
        except KeyError:
            return ""


if __name__ == "__main__":
    showerror(
        "Error", "Try running the Application.py file instead.")
