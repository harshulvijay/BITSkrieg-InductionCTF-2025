#!/usr/bin/env python3
"""
Dog-Napped! — Guess the City (Affine Cipher + ASCII Dogs + Flag)
"""

import random
import re
import sys
from textwrap import dedent

# -------------------
# ASCII DOGS
# -------------------

DOG_HAPPY = r"""
          __
 \ ______/ (^_^)
  }        /~~
 /_)^ --,r'
|b      |b
"""

DOG_SAD = r"""
          __
 \ ______/ (T_T)
  }        /
 /_)_---,r'
|b      |b
"""

# -------------------
# Game Data
# -------------------

BANNER = r"""
*******************************************
***      The Case of the DOG-NAP        ***
*******************************************
"""

def load_flag(filename="flag.txt") -> str:
    try:
        with open(filename, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "FLAG{missing_flag_file}"
FLAG = load_flag()

# Affine cipher params
A = 5
B = 8
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
A2I = {c: i for i, c in enumerate(ALPHA)}
I2A = {i: c for i, c in enumerate(ALPHA)}

# -------------------
# Helper Functions
# -------------------

def _clean(s: str) -> str:
    return re.sub(r"[^A-Za-z]", "", s).upper()

def affine_encrypt(plaintext: str, a: int = A, b: int = B) -> str:
    p = _clean(plaintext)
    if not p:
        return ""
    out = []
    for ch in p:
        x = A2I[ch]
        enc = (a * x + b) % 26
        out.append(I2A[enc])
    return "".join(out)

def spaced_like_city(template: str, letters: str) -> str:
    letters_iter = iter(letters)
    out = []
    for ch in template:
        if ch.isalpha():
            out.append(next(letters_iter, "_"))
        else:
            out.append(ch)
    return "".join(out)

def make_clue(city: str) -> str:
    enc = affine_encrypt(city, A, B)
    return dedent(
        f"""
        Encrypted city:  {enc}
        """
    ).strip()

def normalize_city(s: str) -> str:
    return _clean(s)

def load_cities(filename="cities.txt"):
    try:
        with open(filename, "r") as f:
            return [line.strip().upper() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: cities.txt not found.")
        sys.exit(1)

# -------------------
# Main Game
# -------------------

def main(seed: int | None = None) -> None:
    rng = random.Random(seed)
    cities = load_cities()

    if not cities:
        print("No cities available in cities.txt")
        sys.exit(1)

    target_city = rng.choice(cities)

    print(BANNER)
    print(f"DI knew Dr. Straylight was no good! His name literally means 'light from a stray source.' He's a wild card! But a wild card with my Satta, which I will not stand for!\n")
    print(make_clue(target_city))
    
    turns = 3

    while turns > 0:
        try:
            print("\nThe clock is ticking! Will you **(g)**uess the city and risk it all, or **(e)**ncrypt a word to test your wits?")
            choice = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nSatta tilts his head. Goodbye!")
            break

        if choice in {"g", "guess"}:
            guess = input("Your city guess: ").strip().upper()
            turns -= 1
            if normalize_city(guess) == normalize_city(target_city):
                print(DOG_HAPPY)
                print("\n🎉 BARK BARK! That's pawsome! You've rescued Satta!")
                print(f"The hidden city was {target_city}.")
                print(f"🎯 FLAG: {FLAG}")
                break
            else:
                print(DOG_SAD)
                print("\nWrong! You’ve failed to rescue Satta...")
                print("Connection closing...")
                sys.exit(0)

        elif choice in {"e", "encrypt"}:
            text = input("What city would you like to encrypt? ").strip().upper()
            if text not in cities:
                print("Connection lost...")
                sys.exit(0)
            else:
                enc = affine_encrypt(text, A, B)
                print(f"Here's your encrypted city:  {enc}")
                print("Trying to test my cipher? Heh. You're playing right into my hands.")
                turns -= 1
                if turns > 0:
                    print(f"You have {turns} more chance{'s' if turns > 1 else ''} left!")

        else:
            print("Commands: (g)uess my city or (e)ncrypt a city")

        if turns == 0:
            print(DOG_SAD)
            print("\nOut of turns! Satta remains dog-napped...")
            print("Connection closing...")
            break

# -------------------
# Entry Point
# -------------------

if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else None
    main(seed)
