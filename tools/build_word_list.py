"""Build the word tables in *The Singee Language, Word List* from tools/singee_words.tsv.

For every word it checks the sound rules (tools/singee_check.py), derives the Authority's
clerk spelling with the five clerk habits, and writes a say-it guide with the stress on
the root. It reports any two different words the clerks would have spelled the same.
Add a word by adding a row to the TSV (stress column: which syllable of the first word
carries the root, blank for the first), then run:
    python3 -I tools/build_word_list.py
"""
import csv, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from singee_check import check, TOKEN, VOWELS

ROOT = pathlib.Path(__file__).resolve().parent.parent
TSV = ROOT / "tools" / "singee_words.tsv"
DOC = ROOT / "canon" / "The Singee Language - Word List.md"
START, END = "<!-- word tables start -->", "<!-- word tables end -->"
SAY = {"a": "ah", "e": "eh", "i": "ee", "u": "oo", "x": "kh"}

def syllables(word):
    """Split a word that already passes the sound rules into syllables: an optional
    consonant, a vowel, and an N or X that closes the syllable before another consonant
    or at the end of the word."""
    toks = TOKEN.findall(word.lower())
    sylls, i = [], 0
    while i < len(toks):
        s = []
        if toks[i] not in VOWELS:
            s.append(toks[i]); i += 1
        s.append(toks[i]); i += 1
        if i < len(toks) and toks[i] in ("n", "x") and (i + 1 == len(toks) or toks[i + 1] not in VOWELS):
            s.append(toks[i]); i += 1
        sylls.append(s)
    return sylls

def say(word, stress):
    out = []
    for n, s in enumerate(syllables(word), start=1):
        txt = "".join(SAY.get(t, t) for t in s)
        out.append(txt.upper() if n == stress else txt)
    return "-".join(out)

def clerk(word):
    w = word.replace("lh", "l").replace("Lh", "L").replace("x", "r").replace("X", "R").replace("'", "")
    if w.endswith("i"):
        w = w[:-1] + "ee"
    return w

def main():
    rows = list(csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t"))
    bad, sections, clerks = [], {}, {}
    for r in rows:
        words = r["nation"].split()
        for w in words:
            if check(w) != "ok":
                bad.append(f"{w}: {check(w)}")
        stress = int(r["stress"]) if r["stress"].strip() else 1
        guide = " ".join(say(w, stress if i == 0 else 1) for i, w in enumerate(words))
        cl = " ".join(clerk(w) for w in words)
        clerks.setdefault(cl.lower(), set()).add(r["nation"].lower())
        sections.setdefault(r["section"], []).append((r["nation"], cl, guide, r["meaning"]))
    if bad:
        print("Words that break the sound rules:\n  " + "\n  ".join(bad)); sys.exit(1)
    same = {c: n for c, n in clerks.items() if len(n) > 1}
    out = []
    for sec, items in sections.items():
        out.append(f"### {sec}\n")
        out.append("| **The Nation's spelling** | **Clerk spelling** | **Say it** | **Meaning** |")
        out.append("| --- | --- | --- | --- |")
        for nation, cl, guide, meaning in items:
            out.append(f"| {nation} | {cl} | {guide} | {meaning} |")
        out.append("")
    doc = DOC.read_text(encoding="utf-8")
    a, b = doc.index(START) + len(START), doc.index(END)
    DOC.write_text(doc[:a] + "\n\n" + "\n".join(out) + "\n" + doc[b:], encoding="utf-8")
    print(f"{len(rows)} entries written in {len(sections)} sections.")
    if same:
        print("Clerk spelling collapses these different words into one:")
        for c, n in same.items():
            print(f"  {c}: {', '.join(sorted(n))}")

if __name__ == "__main__":
    main()
