"""
Builds the curated answer list (requirement G7).

How the list is made:
1. Start from candidate_answers.txt: everyday words we picked by hand
   (things, actions, and feelings people use in normal conversation).
2. Keep only words that are exactly 5 letters and only letters.
3. Keep only words that are also in english.py (the required word source).
4. Remove words that might feel upsetting or awkward for older players
   (illness, death, and similar topics).
5. Remove duplicates and sort.

Run:  python make_answer_list.py
Output: actions/answers.txt
"""

from actions.english import isEnglishWord

AVOID = {"tumor", "widow", "naked", "toxic", "cough", "fever", "grave",
         "knife", "rifle", "sword", "thief", "greed", "panic", "skull"}

with open("actions/candidate_answers.txt") as f:
    candidates = f.read().split()

answers = set()
skipped_not_in_list = []
for word in candidates:
    word = word.strip().lower()
    if len(word) != 5 or not word.isalpha():
        continue
    if word in AVOID:
        continue
    if not isEnglishWord(word):
        skipped_not_in_list.append(word)
        continue
    answers.add(word)

answers = sorted(answers)
with open("actions/answers.txt", "w") as f:
    f.write("\n".join(answers) + "\n")

print(f"Candidates: {len(candidates)}")
print(f"Answers saved: {len(answers)}")
print(f"Not in english.py (skipped): {skipped_not_in_list}")
