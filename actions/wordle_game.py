"""
Core Wordle game logic (requirements G1-G7).
No Rasa code here. The Rasa actions call these functions.
"""

import random
from pathlib import Path

from .english import ENGLISH_WORDS

WORD_LENGTH = 5

# G2: six guesses, the same as NYT Wordle, so it feels familiar.
MAX_GUESSES = 6

# G3: every real five-letter word in english.py is an allowed guess.
VALID_GUESSES = {w for w in ENGLISH_WORDS if len(w) == WORD_LENGTH and w.isalpha()}

# G7: the hidden answer only comes from the curated list of common words.
ANSWER_FILE = Path(__file__).parent / "answers.txt"
ANSWERS = ANSWER_FILE.read_text().split()

# The three letter states.
CORRECT = "correct"   # right letter, right spot
PRESENT = "present"   # in the word, wrong spot
ABSENT = "absent"     # not in the word


def pick_answer():
    """G1: choose a hidden five-letter answer for a new game."""
    return random.choice(ANSWERS)


def check_guess(guess):
    """
    G4: check a guess before it is scored.
    Returns None if the guess is fine, or a kind message if it is not.
    An invalid guess does NOT use up a turn.
    """
    guess = guess.strip().lower()

    if not guess.isalpha():
        return "Please use letters only, with no numbers, spaces, or symbols. This did not use a guess."
    if len(guess) != WORD_LENGTH:
        return f"'{guess.upper()}' has {len(guess)} letters. Please try a {WORD_LENGTH}-letter word. This did not use a guess."
    if guess not in VALID_GUESSES:
        return f"I don't know the word '{guess.upper()}'. Please try another word. This did not use a guess."
    return None


def score_guess(guess, answer):
    """
    G5: score each letter, handling repeated letters correctly.
    Step 1: letters in the right spot are CORRECT.
    Step 2: other letters are PRESENT only if that letter is still
            "left over" in the answer. Otherwise ABSENT.
    """
    guess = guess.lower()
    answer = answer.lower()
    result = [ABSENT] * WORD_LENGTH

    leftover = {}
    for i in range(WORD_LENGTH):
        if guess[i] == answer[i]:
            result[i] = CORRECT
        else:
            letter = answer[i]
            leftover[letter] = leftover.get(letter, 0) + 1

    for i in range(WORD_LENGTH):
        if result[i] == CORRECT:
            continue
        letter = guess[i]
        if leftover.get(letter, 0) > 0:
            result[i] = PRESENT
            leftover[letter] -= 1

    return result


def describe_result(guess, result):
    """Plain-language result that a screen reader or voice can say."""
    phrases = []
    for letter, state in zip(guess.upper(), result):
        if state == CORRECT:
            phrases.append(f"{letter} is correct")
        elif state == PRESENT:
            phrases.append(f"{letter} is in the word, wrong spot")
        else:
            phrases.append(f"{letter} is not in the word")
    return ". ".join(phrases) + "."


def symbols(result):
    """Text symbols so the states never depend on color alone."""
    marks = {CORRECT: "✓", PRESENT: "~", ABSENT: "✗"}
    return " ".join(marks[state] for state in result)

#pick_answer picks a random word from answers.txt.
#check_guess rejects bad guesses with a kind message, and the guess doesn’t count.
#score_guess marks each letter correct, present, or absent. It handles double letters by “using up” each answer letter only once.
#describe_result and symbols turn the result into a sentence and ✓ ~ ✗ symbols, so color isn’t the only cue