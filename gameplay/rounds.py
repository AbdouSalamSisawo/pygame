import random

ACTIVITIES = ("image_to_word", "word_to_image")


def build_round(vocab, tracker, bias):
    target = tracker.choose_target(vocab)
    count = tracker.option_count(target["word"], bias)
    options = tracker.choose_options(vocab, target, count)
    activity = random.choice(ACTIVITIES)
    return {
        "target": target,
        "options": options,
        "activity": activity,
        "eliminated": set(),
        "round_wrong": 0,
    }
