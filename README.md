# wordle-for-everyone-1-
Wordle for Everyone
A friendly five-letter word game made for older adults. No timer. No pressure. Take your time.
Built for AI 380: Human-AI Interaction (Fall 2026). By Juniper Ammirati and Kendall Brown.

Play it

Live link: https://kjbrown24.github.io/wordle-for-everyone-1-/ (works any time)

Open the link in any modern browser (Safari, Chrome, Edge, or Firefox) on a laptop, desktop, or tablet. There is nothing to install and no account or sign-in. You can type, tap, or talk to it.

How to play

The game thinks of a hidden 5-letter word. You have 6 guesses.
Type your guess in the Your guess box (or tap the on-screen keys).
Press Submit guess (or the Enter key).
Each letter gets a result. You can tell them apart without color:


Mark
Border
Meaning
✓
Solid
Right letter, right spot
~
Dashed
In the word, wrong spot
✗
Dotted
Not in the word


The game also writes the result in plain words, for example: "E is correct. A is in the word, wrong spot." It also tells you how many guesses are left.
Win by guessing the word. If you run out of guesses, the game shows the word and offers a new game.

Good to know
If your guess is too short, too long, has a non-letter, or is not a real word, the game says so kindly and does not use up a guess.
Your earlier guesses stay on the board, and the on-screen keyboard keeps the marks, so you don't have to remember them.
There is never a timer.




Buttons

Button
What it does
New game
Starts a fresh word.
Get a hint
Gives a gentle hint, such as how many vowels the word has. Hints do not use up a guess. (shows how many are left, 3 per game)
I give up
Kindly shows you the word. Giving up is part of the game.
How to play
Shows these instructions again. Always available. (top right)


Settings

Open the Settings box at the top of the page:
Feedback style: Color and symbols, High contrast (black and white), or Symbols only (no color).
Text size: make everything larger.
Read results aloud: the game speaks each result.
Reduce motion (turns off tile animations) and Click sounds

Talk to the game (voice)
You don't have to type. You can speak your guess and the game will reply out loud.
Allow the microphone when your browser asks.
Say your five-letter word, for example "water".
The game says the result in plain words and tells you how many guesses are left.
- Say a word, then say the word or spell it (“C, R, A, N, E”). The word appears on the board first so you can check it. Then press Submit or say “submit”. You can also say “hint”, “I give up”, “clear”, or “new game”. Voice works in Chrome, Edge, and Safari (not Firefox). The game reads results aloud only if Read results aloud is on in Settings
Tips
Speak slowly and clearly, one word at a time.
If the game doesn't catch what you said, nothing is lost. It will ask you to try again and will not use up a guess.
Typing and voice work together. You can switch between them at any time.
Voice replies use the same wording as the written results, which stay on screen.
Keyboard-only play
Tab / Shift+Tab moves between controls. The control you are on has a visible outline.
Type letters directly into the guess box. Backspace fixes a mistake.
Enter and submit the guess.

Accessibility features
Three letter states shown by symbol, border style, and a written sentence, not color alone
Always-visible legend
Results written as plain text so screen readers can announce them
No timers, and invalid guesses are free
Keyboard-friendly with visible focus
Voice play: speak your guess and hear the reply
Adjustable text size and feedback style
Gentle, encouraging wording, with no streaks

Game design choices
Six guesses (G2): the same as NYT Wordle, so players who already know the game feel at home.
Word list (G3, G4): every guess is checked against the provided english.py. Answers and guesses come from that list.
Curated answers (G7): answers come from a hand-picked pool of 734 common, everyday words, so players are not asked to guess obscure ones. A word is kept only if it is exactly 5 letters and appears in english.py. Upsetting words (for example, about illness or death) were removed. make_answer_list.py repeats this process.

Privacy
The game does not ask for or store your name, age, health information, or recordings. Voice is used only to understand your guess. Settings are saved only in your own browser, so they stay the same next time.” This one matters: the assignment requires settings that persist, and ours do.



Project files

File
What it does
web/index.html
The game page players see: tiles, keyboard, Settings, and Help.
actions/wordle_game.py
The game rules (G1 to G7): picks the hidden word, validates guesses, rejects bad guesses without using a turn, scores repeated letters correctly, and ends with a clear win or loss and a new-game offer.
actions/actions.py
Rasa custom actions for starting a game, making a guess, hints, and giving up.
actions/english.py
The provided word list. All 5-letter words in it are allowed guesses.
actions/answers.txt
The 734 curated answer words.
make_answer_list.py, actions/candidate_answers.txt
How the answer list was built, so answers are never obscure words.
domain.yml
Rasa slots, responses, and actions for the game.
data/flows.yml
Rasa CALM flows: the game loop and the hint flow.
config.yml, endpoints.yml, credentials.yml
Rasa settings for text and voice.
test_game.py
Tests that the game rules work.
start.sh, .devcontainer/
Start the game in GitHub Codespaces.
web/offline.js
(offline mode)
web/words.js
word lists for offline mode
web/config.js
Rasa address
make_words_js.py

.github/workflows/pages.yml
publishes the game page



Always available
When the Rasa server is running, the game uses Rasa. When it isn’t, the page plays the same game in the browser (offline mode). A badge under the buttons shows which one is on






AI tools used
We used Claude to create our interface. We first built a working Wordle with Rasa in the terminal, then developed it further with Claude to use CALM and to create a remote interface. 
