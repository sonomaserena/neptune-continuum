"""Check Singee words against the sound rules in *The Singee Language, Sound and Spelling*.

Rules checked: no O; only Singee letters (Nation spelling); words end on a vowel or N;
two vowels never touch (the catch goes between them); only N or the rasp X may close a
syllable before another consonant; no consonant cluster at the start of a word.
Hyphens are ignored, so example glosses like yen-ru-ka-ni can be checked as written.
Usage: python3 -I singee_check.py word [word ...]
"""
import re, sys

VOWELS = set("aeiu")
LETTERS = set("aeiuptkmnslxhvrly'g-")
TOKEN = re.compile(r"ng|lh|t'|k'|'|[aeiu]|[ptkmnslxhvrly]")

def check(word):
    w = word.lower().replace("-", "").replace("’", "'")
    if "o" in w:
        return "has an O"
    if not set(w) <= LETTERS:
        return "letters that aren't Singee: " + "".join(sorted(set(w) - LETTERS))
    toks = TOKEN.findall(w)
    if "".join(toks) != w:
        return "can't be split into Singee sounds (a stray g?)"
    if not (toks[-1] in VOWELS or toks[-1] == "n"):
        return "ends on something other than a vowel or N"
    for a, b in zip(toks, toks[1:]):
        if a in VOWELS and b in VOWELS:
            return "two vowels touch; a catch belongs between them"
    cons = lambda t: t not in VOWELS
    if len(toks) > 1 and cons(toks[0]) and cons(toks[1]):
        return "starts with two consonants"
    for i in range(1, len(toks) - 1):
        if cons(toks[i]) and cons(toks[i + 1]) and toks[i] not in ("n", "x"):
            return f"a syllable closes on {toks[i]}, but only N or X can"
    return "ok"

if __name__ == "__main__":
    bad = 0
    for word in sys.argv[1:]:
        result = check(word)
        bad += result != "ok"
        print(f"{word}: {result}")
    sys.exit(1 if bad else 0)
