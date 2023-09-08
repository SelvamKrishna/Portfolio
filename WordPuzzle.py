from random import choice

words = ['acoustic', 'albatross', 'alligator', 'apple', 'banana', 'bat', 'bison',
         'butterfly', 'catapult', 'cheetah', 'chocolate', 'crocodile', 'dingo',
         'dolphin', 'dragon', 'eagle', 'elephant', 'elephant', 'elephant', 'flamingo',
         'flamingo', 'fox', 'gazelle', 'giraffe', 'giraffe', 'guitar', 'happiness',
         'hawk', 'hedgehog', 'helicopter', 'iguana', 'iguana', 'iguana', 'island',
         'jaguar', 'jazz', 'jellyfish', 'jellyfish', 'kangaroo', 'kangaroo', 'kangaroo',
         'koala', 'lemon', 'lemur', 'lemur', 'llama', 'macaw', 'mango', 'meerkat',
         'mongoose', 'narwhal', 'narwhal', 'newt', 'notebook', 'ocean', 'octopus',
         'octopus', 'otter', 'panda', 'parrot', 'penguin', 'platypus', 'quartz',
         'quokka', 'quokka', 'quokka', 'rabbit', 'raccoon', 'raccoon', 'rhinoceros',
         'sloth', 'sloth', 'squirrel', 'strawberry', 'tapir', 'tiger', 'tiger', 'toucan',
         'uakari', 'umbrella', 'unicorn', 'unicorn', 'vampire', 'violin', 'vulture',
         'vulture', 'watermelon', 'weasel', 'weasel', 'whale', 'x-ray', 'x-ray', 'xenopus',
         'xylophone', 'yak', 'yak', 'yak', 'zebra', 'zebra', 'zeppelin', 'zeppelin']


guesses = 10
answer = choice(words).lower()
display = []

for character in answer:
    if choice( (True, False, False) ) is True:
        display.append(character)
    else: display.append("_")

while guesses != 0:
    print("-----------------------------")
    print(f"guesses = {guesses}")

    display_string = ""

    for i in display:
        display_string += i
        display_string += " "

    print(f"word    = {display_string}")

    guess = input("Guess the Letter : ").lower()
    
    if guess in answer:
        if guess not in display:
          for idx in range(len(answer)):
              if answer[idx] == guess:
                  display[idx] = guess
        else: guesses -= 1
    else: guesses -= 1

    if "_" not in display:
        print("YOU WON")
        break

if guesses == 0:
    print("YOU LOSE")
print("-----------------------------")
print(f"answer = {answer}")