from Imports import *


def SaveFunction() -> None:
    save = SaveData(websiteEntry.get(), emailEntry.get(), passwordEntry.get())
    save.CompileData()
    websiteEntry.delete(0, END)
    passwordEntry.delete(0, END)


def GenerateFunction() -> None:
    passwordText: str = GeneratePassword()
    passwordEntry.delete(0, END)
    passwordEntry.insert(END, passwordText)
    copy(passwordText)


def SearchFunction() -> None:
    foundPassword: str = SearchData(websiteEntry.get())
    if foundPassword == "":
        showerror(
            "Error", "The given website is not available.Try checking for any spelling mistakes")
    else:
        passwordEntry.delete(0, END)
        passwordEntry.insert(END, foundPassword)
        copy(foundPassword)


screen = Tk()
screen.title("Password Manager")
screen.config(padx=40, pady=25)

logoCanvas = Canvas(master=screen, width=200, height=200)
logoImage = PhotoImage(file="Assets/logo.png")
logoCanvas.create_image(100, 100, image=logoImage)
logoCanvas.grid(row=0, column=0, columnspan=3)

Label(text="Website :", font=("Arial", 10, "bold")).grid(row=1, column=0)
Label(text="Email :", font=("Arial", 10, "bold")).grid(row=2, column=0)
Label(text="Password :", font=("Arial", 10, "bold")).grid(row=3, column=0)

websiteEntry = Entry(width=21)
websiteEntry.focus()
emailEntry = Entry(width=40)
passwordEntry = Entry(width=21)
websiteEntry.grid(row=1, column=1)
emailEntry.grid(row=2, column=1, columnspan=2)
emailEntry.insert(0, "selvam.krishna0510@gmail.com")
passwordEntry.grid(row=3, column=1)

Button(text="Search Password",
       command=SearchFunction,
       width=15).grid(row=1, column=2)
Button(text="Generate Password",
       command=GenerateFunction,
       width=15).grid(row=3, column=2)
Button(text="Add",
       command=SaveFunction,
       width=34).grid(row=4, column=1, columnspan=2, pady=25)

screen.mainloop()
