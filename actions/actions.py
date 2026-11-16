"""
Custom actions for Wordle for Everyone.
Rasa runs these. Each one reads slots, uses the game rules
in wordle_game.py, sends a message, and updates slots.
"""

from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from .wordle_game import (
    MAX_GUESSES, CORRECT, pick_answer, check_guess,
    score_guess, describe_result, symbols,
)


def give_hint(dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
    """Enhancement (Category A): gentle hints first, then more direct ones.
    Hints never cost a guess."""
    answer = tracker.get_slot("answer_word")
    if not answer:
        dispatcher.utter_message(text="Let's start a game first, then I can give you a hint.")
        return []

    hints_used = int(tracker.get_slot("hints_used") or 0)
    vowels = sum(1 for letter in answer if letter in "aeiou")
    vowel_word = "vowel" if vowels == 1 else "vowels"

    hints = [
        f"Gentle hint: the word has {vowels} {vowel_word}.",
        f"Bigger hint: the word starts with the letter {answer[0].upper()}.",
        f"Biggest hint: the word ends with the letter {answer[-1].upper()}.",
    ]

    if hints_used >= len(hints):
        dispatcher.utter_message(
            text=("You've used all 3 hints. You can keep guessing, "
                  "or say 'I give up' and I'll show you the word."),
            json_message={"type": "hint", "hints_left": 0},
        )
        return []

    dispatcher.utter_message(
        text=hints[hints_used] + " Hints don't use up a guess.",
        json_message={"type": "hint", "hints_left": len(hints) - hints_used - 1},
    )
    return [SlotSet("hints_used", float(hints_used + 1))]


class ActionStartGame(Action):
    """G1: pick a hidden word and reset everything for a new game."""

    def name(self) -> Text:
        return "action_start_game"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        answer = pick_answer()

        dispatcher.utter_message(text=(
            f"Let's play! I'm thinking of a 5-letter word. "
            f"You have {MAX_GUESSES} guesses, and there is no timer, so take your time. "
            "After each guess, I'll mark every letter: "
            "✓ means right letter, right spot. "
            "~ means the letter is in the word, but in a different spot. "
            "✗ means the letter is not in the word. "
            "You can ask for a hint at any time."
        ), json_message={"type": "new_game", "max_guesses": MAX_GUESSES, "word_length": 5})

        return [
            SlotSet("answer_word", answer),
            SlotSet("guesses_left", float(MAX_GUESSES)),
            SlotSet("board", ""),
            SlotSet("hints_used", 0.0),
            SlotSet("game_over", False),
            SlotSet("guess", None),
        ]


class ActionMakeGuess(Action):
    """G3-G6: check the guess, score it, and decide win, loss, or keep going."""

    def name(self) -> Text:
        return "action_make_guess"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Spelled-out guesses like "c r a n e" become "crane".
        guess = (tracker.get_slot("guess") or "").lower()
        guess = guess.replace(" ", "").replace("-", "").replace(".", "")

        answer = tracker.get_slot("answer_word")
        guesses_left = int(tracker.get_slot("guesses_left") or 0)
        board = tracker.get_slot("board") or ""

        # The web page's Hint button sends "hint" as the guess. It never uses a turn.
        if guess == "hint":
            return give_hint(dispatcher, tracker) + [SlotSet("game_over", False)]

        # Enhancement (Category C): "I give up" kindly shows the word and ends the game.
        if guess in ("giveup", "igiveup"):
            dispatcher.utter_message(
                text=(f"That's okay! The word was {answer.upper()}. "
                      "Giving up is part of the game. Want to try another one?"),
                json_message={"type": "gave_up", "answer": answer},
            )
            return [SlotSet("game_over", True)]

        # G4: a bad guess gets a kind message and does NOT use a turn.
        problem = check_guess(guess)
        if problem:
            dispatcher.utter_message(text=problem, json_message={"type": "invalid_guess"})
            return [SlotSet("game_over", False)]

        # G5: score the guess.
        result = score_guess(guess, answer)
        guesses_left -= 1

        # Keep every earlier guess on the board, so players don't have to remember.
        board = board + f"{guess.upper()}   {symbols(result)}\n"

        won = all(state == CORRECT for state in result)
        game_over = won or guesses_left == 0

        # The web page uses this data to draw the tiles.
        dispatcher.utter_message(
            text=f"Your guesses so far:\n{board}{describe_result(guess, result)}",
            json_message={
                "type": "guess_result",
                "guess": guess,
                "result": result,
                "description": describe_result(guess, result),
                "guesses_left": guesses_left,
                "game_over": game_over,
                "won": won,
                "answer": answer if game_over else None,
            },
        )

        # G6: clear win or loss message, and always offer a new game.
        if won:
            dispatcher.utter_message(text=(
                f"You got it! The word was {answer.upper()}. Well done!"
            ))
        elif guesses_left == 0:
            dispatcher.utter_message(text=(
                f"That was a good try. The word was {answer.upper()}. "
                "Every game helps you get better."
            ))
        else:
            word = "guess" if guesses_left == 1 else "guesses"
            dispatcher.utter_message(text=f"You have {guesses_left} {word} left.")

        return [
            SlotSet("guesses_left", float(guesses_left)),
            SlotSet("board", board),
            SlotSet("game_over", game_over),
        ]


class ActionHint(Action):
    """Hint flow for typed or spoken requests like "give me a hint"."""

    def name(self) -> Text:
        return "action_hint"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return give_hint(dispatcher, tracker)