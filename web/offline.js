// =========================================================
// OFFLINE MODE
// When the Rasa server is not running, the page plays the game
// by itself. These rules and messages copy actions/wordle_game.py
// and actions/actions.py, so the game feels the same either way.
// It answers in the same format as Rasa's REST channel:
//   [{ text: "..." }, { custom: {...} }, ...]
// =========================================================

const OfflineGame = (() => {
  const LENGTH = 5;
  const MAX_GUESSES = 6;   // G2: same as NYT Wordle
  let answer = null, guessesLeft = 0, hintsUsed = 0, over = true;

  // G4: check a guess; returns a kind message, or null if it's fine
  function checkGuess(guess) {
    if (!/^[a-z]+$/.test(guess)) return "Please use letters only, with no numbers, spaces, or symbols. This did not use a guess.";
    if (guess.length !== LENGTH) return `'${guess.toUpperCase()}' has ${guess.length} letters. Please try a ${LENGTH}-letter word. This did not use a guess.`;
    if (!VALID_WORDS.has(guess)) return `I don't know the word '${guess.toUpperCase()}'. Please try another word. This did not use a guess.`;
    return null;
  }

  // G5: score letters; repeated letters are only counted as often as they appear
  function score(guess, ans) {
    const result = Array(LENGTH).fill("absent");
    const leftover = {};
    for (let i = 0; i < LENGTH; i++) {
      if (guess[i] === ans[i]) result[i] = "correct";
      else leftover[ans[i]] = (leftover[ans[i]] || 0) + 1;
    }
    for (let i = 0; i < LENGTH; i++) {
      if (result[i] === "correct") continue;
      if (leftover[guess[i]] > 0) { result[i] = "present"; leftover[guess[i]]--; }
    }
    return result;
  }

  function describe(guess, result) {
    return result.map((s, i) => {
      const L = guess[i].toUpperCase();
      return s === "correct" ? `${L} is correct` : s === "present" ? `${L} is in the word, wrong spot` : `${L} is not in the word`;
    }).join(". ") + ".";
  }

  function start() {
    answer = ANSWER_WORDS[Math.floor(Math.random() * ANSWER_WORDS.length)];   // G1
    guessesLeft = MAX_GUESSES; hintsUsed = 0; over = false;
    return [
      { text: `Let's play! I'm thinking of a 5-letter word. You have ${MAX_GUESSES} guesses, and there is no timer, so take your time. ` +
              "After each guess, I'll mark every letter: ✓ means right letter, right spot. ~ means the letter is in the word, but in a different spot. " +
              "✗ means the letter is not in the word. You can ask for a hint at any time." },
      { custom: { type: "new_game", max_guesses: MAX_GUESSES, word_length: LENGTH } }
    ];
  }

  function hint() {
    if (!answer || over) return [{ text: "Let's start a game first, then I can give you a hint." }];
    const vowels = [...answer].filter(c => "aeiou".includes(c)).length;
    const hints = [
      `Gentle hint: the word has ${vowels} ${vowels === 1 ? "vowel" : "vowels"}.`,
      `Bigger hint: the word starts with the letter ${answer[0].toUpperCase()}.`,
      `Biggest hint: the word ends with the letter ${answer[LENGTH - 1].toUpperCase()}.`
    ];
    if (hintsUsed >= hints.length) {
      return [{ text: "You've used all 3 hints. You can keep guessing, or say 'I give up' and I'll show you the word." },
              { custom: { type: "hint", hints_left: 0 } }];
    }
    const msg = hints[hintsUsed] + " Hints don't use up a guess.";
    hintsUsed++;
    return [{ text: msg }, { custom: { type: "hint", hints_left: hints.length - hintsUsed } }];
  }

  function giveUp() {
    over = true;
    return [{ text: `That's okay! The word was ${answer.toUpperCase()}. Giving up is part of the game. Want to try another one?` },
            { custom: { type: "gave_up", answer } }];
  }

  function makeGuess(raw) {
    const guess = (raw || "").toLowerCase().replace(/[\s.-]/g, "");
    if (!answer || over) return [{ text: "Press New game to start a game." }];
    if (guess === "hint") return hint();
    if (guess === "giveup" || guess === "igiveup") return giveUp();

    const problem = checkGuess(guess);
    if (problem) return [{ text: problem }, { custom: { type: "invalid_guess" } }];

    const result = score(guess, answer);
    guessesLeft--;
    const won = result.every(s => s === "correct");
    over = won || guessesLeft === 0;
    const replies = [{ custom: {
      type: "guess_result", guess, result, description: describe(guess, result),
      guesses_left: guessesLeft, game_over: over, won, answer: over ? answer : null
    } }];
    if (won) replies.push({ text: `You got it! The word was ${answer.toUpperCase()}. Well done!` });             // G6
    else if (guessesLeft === 0) replies.push({ text: `That was a good try. The word was ${answer.toUpperCase()}. Every game helps you get better.` });
    else replies.push({ text: `You have ${guessesLeft} ${guessesLeft === 1 ? "guess" : "guesses"} left.` });
    return replies;
  }

  // Understands the same messages the page sends to Rasa.
  function handle(message) {
    if (message === "/start_game") return start();
    if (message === "/get_hint") return hint();
    const m = message.match(/^\/SetSlots\(guess=(.*)\)$/);
    if (m) return makeGuess(m[1]);
    return [{ text: "In offline mode, please use the buttons or type a 5-letter word." }];
  }

  return { handle, score, checkGuess };
})();
