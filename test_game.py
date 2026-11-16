"""
Quick checks for the game rules. Run:  python test_game.py
No Rasa needed.
"""

from actions.wordle_game import (
    ANSWERS, VALID_GUESSES, MAX_GUESSES, pick_answer, check_guess,
    score_guess, describe_result, symbols, CORRECT as C, PRESENT as P, ABSENT as A,
)

# G1 + G7: answer comes from the curated list, and every answer is a valid guess
answer = pick_answer()
assert answer in ANSWERS and len(answer) == 5
assert all(a in VALID_GUESSES for a in ANSWERS)
print(f"G1/G7 ok: {len(ANSWERS)} curated answers, {len(VALID_GUESSES)} allowed guesses")

# G2
assert MAX_GUESSES == 6
print("G2 ok: 6 guesses")

# G3 + G4: invalid guesses get a message (and do not count)
assert check_guess("apple") is None
assert check_guess("app") is not None        # too short
assert check_guess("apples") is not None     # too long
assert check_guess("ap1le") is not None      # non-letter
assert check_guess("xqzzt") is not None      # not a real word
print("G3/G4 ok:", check_guess("xqzzt"))

# G5: repeated letters
assert score_guess("apple", "apple") == [C, C, C, C, C]
assert score_guess("eerie", "apple") == [A, A, A, A, C]   # APPLE has one E: only the E in place counts
assert score_guess("speed", "abide") == [A, A, P, A, P]   # one E present, extra E absent
assert score_guess("lolly", "hello") == [A, P, C, C, A]   # HELLO's two L's are both used up in place
print("G5 ok: repeated letters scored correctly")

print()
print("Example: guess CRANE, answer CREAM")
r = score_guess("crane", "cream")
print(" ", symbols(r))
print(" ", describe_result("crane", r))
print("\nAll checks passed.")
