"""
Rebuilds web/words.js (the word lists the web page uses in offline mode)
from actions/english.py and actions/answers.txt.
Run:  python make_words_js.py
"""
import json
from actions.wordle_game import ANSWERS, VALID_GUESSES

with open("web/words.js", "w") as f:
    f.write("// Word lists for offline mode, made from english.py and actions/answers.txt\n")
    f.write("// (the same lists the Rasa actions use). Rebuild with: python make_words_js.py\n")
    f.write("const ANSWER_WORDS = " + json.dumps(ANSWERS) + ";\n")
    f.write("const VALID_WORDS = new Set(" + json.dumps(sorted(VALID_GUESSES)) + ");\n")
print("web/words.js updated")
