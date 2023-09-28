from Functions import *


def SwapCard():
    global cardQues
    global cardAnsw
    cardQues, cardAnsw = RandomCard()

    DisplayCard(True)


def DisplayCard(currentState: bool = True):
    if currentState is True:
        newColor = "black"
        newTitle = FROM
        newText = cardQues
        newImage = cardFrontImg
    else:
        newColor = "white"
        newTitle = TO
        newText = cardAnsw
        newImage = cardBackImg

    mainCanv.itemconfig(currentImg, image=newImage)
    mainCanv.itemconfig(titleText, text=newTitle, fill=newColor)
    mainCanv.itemconfig(wordText, text=newText, fill=newColor)


def KnownFactor(isUnknown: bool):
    if isUnknown:
        pass
    else:
        IsKnown(cardQues)

    DisplayCard(False)
    window.after(3000, SwapCard)


color = "#B1DDC6"

window = Tk()
window.title("Flash Card")
window.config(bg=color, padx=50, pady=50)

mainCanv = Canvas(master=window, width=800, height=526,
                  bg=color, highlightthickness=0)

cardFrontImg = PhotoImage(
    file="Learning/Images/card_front - Copy.png", )
cardBackImg = PhotoImage(
    file="Learning/Images/card_back - Copy.png", )

currentImg = mainCanv.create_image(400, 263, image=cardFrontImg)

titleText = mainCanv.create_text(
    400, 150, font=("Arial", 40, "italic"), text="Title")
wordText = mainCanv.create_text(
    400, 250, font=("Arial", 60, "bold"), text="word")
mainCanv.grid(row=0, column=0, columnspan=2)

unknownImg = PhotoImage(file="Learning/Images/wrong - Copy.png")
Button(master=window, image=unknownImg,
       command=lambda: KnownFactor(True), highlightthickness=0).grid(row=1, column=0)

knownImg = PhotoImage(file="Learning/Images/right - Copy.png")
Button(master=window, image=knownImg,
       command=lambda: KnownFactor(True), highlightthickness=0).grid(row=1, column=1)

SwapCard()
window.mainloop()
