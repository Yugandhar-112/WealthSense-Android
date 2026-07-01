"""
Builds the bag-of-words vocabulary from dataset.py.

This is deterministic and must be run before training so the vocabulary
(and therefore the model's input layout) is fixed and known. The same
vocabulary is hardcoded into CategoryClassifier.kt on the Android side -
if you change dataset.py, re-run this and copy the new vocab into Kotlin,
or the app and model will disagree on what each input position means.
"""
import re
import json
from collections import Counter
from dataset import DATA

TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str):
    return TOKEN_RE.findall(text.lower())


def build_vocab(min_freq: int = 2, max_size: int = 60):
    counts = Counter()
    for text, _ in DATA:
        counts.update(set(tokenize(text)))  # count once per example, not per occurrence

    # Drop near-useless numeric tokens and very rare tokens
    filtered = [(w, c) for w, c in counts.items() if c >= min_freq and not w.isdigit()]
    filtered.sort(key=lambda x: (-x[1], x[0]))  # most frequent first, alphabetical tiebreak
    vocab_words = [w for w, _ in filtered[:max_size]]

    return {word: idx for idx, word in enumerate(vocab_words)}


if __name__ == "__main__":
    vocab = build_vocab()
    print(f"Vocabulary size: {len(vocab)}")
    print(json.dumps(vocab, indent=2))

    with open("vocab.json", "w") as f:
        json.dump(vocab, f, indent=2)

    # Emit ready-to-paste Kotlin map literal too
    kotlin_entries = ",\n        ".join(f'"{w}" to {i}' for w, i in vocab.items())
    print("\n\n--- Kotlin map (for reference / regeneration) ---\n")
    print(f"    private val vocab = mapOf(\n        {kotlin_entries}\n    )")
