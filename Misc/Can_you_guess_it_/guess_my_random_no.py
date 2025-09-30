import random

def main():
    try:
        with open("flag.txt", "r") as f:
            FLAG = f.read().strip()
    except FileNotFoundError:
        FLAG = "dummy_flag"

    print("Welcome to the guessing game!")
    print("Can you guess my random number??")

    random.seed(8008135)

    while True:
        
        secret = random.randrange(1000)

        guess = input("Enter your guess (0-999): ").strip()
        try:
            g = int(guess)
        except ValueError:
            print("That's not a number. Try again.")
            continue

        if g == secret:
            print(f"Correct! Here's your flag: {FLAG}")
            break
        else:
            print("Nope! Try again.")

if __name__ == "__main__":
    main()