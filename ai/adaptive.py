import random
import time


class AdaptiveTracker:
    def __init__(self, progress):
        self.progress = progress
        self.stats = progress.setdefault("stats", {})

    def _ensure_word(self, word):
        if word not in self.stats:
            self.stats[word] = {
                "correct": 0,
                "wrong": 0,
                "streak": 0,
                "last_seen": 0,
            }
        return self.stats[word]

    def get_word_stats(self, word):
        return self._ensure_word(word)

    def record(self, word, correct):
        stats = self._ensure_word(word)
        if correct:
            stats["correct"] += 1
            stats["streak"] += 1
        else:
            stats["wrong"] += 1
            stats["streak"] = 0
        stats["last_seen"] = time.time()

    def _weight(self, word):
        stats = self._ensure_word(word)
        weight = 1.0 + stats["wrong"] * 0.7 - stats["correct"] * 0.2
        return max(0.4, weight)

    def choose_target(self, vocab):
        weights = [self._weight(item["word"]) for item in vocab]
        return random.choices(vocab, weights=weights, k=1)[0]

    def option_count(self, word, bias):
        stats = self._ensure_word(word)
        wrong = stats["wrong"]
        if bias == "easy":
            return 2 if wrong >= 1 else 3
        if bias == "hard":
            return 4 if wrong <= 1 else 3
        return 2 if wrong >= 3 else 3

    def choose_options(self, vocab, target, count):
        others = [item for item in vocab if item["word"] != target["word"]]
        random.shuffle(others)
        options = [target] + others[: max(1, count - 1)]
        random.shuffle(options)
        return options
