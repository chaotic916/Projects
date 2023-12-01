from random import randint
import time

def randpick():

    # Create a list with four randomly generated numbers(integers)
    rand4 = [randint(0,9) for _ in range(4)]
    # Create a single string with the generated four numbers
    answer = ''.join(map(str, rand4))
    return answer

# To inspect the guessed number with the correct answer
# 'inputguess' is supposed to be a 4-digit number, so is 'answer'
def inspect(guess_str, answer_str):
    bulls = 0
    cows = 0
    # i is the index number, digit is the [i]
    for i, digit in enumerate(guess_str):
        if digit == answer_str[i]:
            bulls += 1
        elif digit in answer_str:
            cows += 1
        else:
            digit = -1
            # or another value to indicate it's not a correct digit
    return bulls, cows

def gameplay():
    answer_generated = randpick()
    life = 10
    print(f"You have total 10 lives. Be careful not to waste them!")

    while life > 0:
        guess = input("Guess a 4-digit number: ")

        if guess.isdigit() and len(guess) == 4:
            while True:
                bulls, cows = inspect(guess, answer_generated)
                life -= 1

                if life>0 and bulls < 4:
                    time.sleep(1)
                    print(f"Result: {bulls} Bulls, {cows} Cows. You have {life} lives remaining.")
                    break
                elif life == 0:
                    time.sleep(3)
                    print(f"You failed it! The correct answer was {answer_generated}.")
                    main_menu()
                elif bulls == 4:
                    time.sleep(3)
                    print("Congratulations! You got the correct answer.")
                    main_menu()
        else:
            print("Please enter a valid 4-digit number.")
            continue

def main_menu():
    print("""
Welcome to our silly guessing game! Hope you know the drill.
Here is what you should do: Guess a four-digit number and see if it's right.

If your guess has the right number at the right place, you will get 'Bull',
and you got the right number at a wrong place, you will get 'Cow'.

You have 10 trials to reach the full answer.\n""")
    menu_choice = input("""1. Play the Game
2. Exit the Game
Your choice?\n""")

    if menu_choice == '1':
        gameplay()
    elif menu_choice == '2':
        exit()
    else:
        main_menu()
        print("Invalid choice. Please enter '1' to play or '2' to exit.")

main_menu()

