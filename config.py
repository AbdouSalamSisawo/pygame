import os

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
VOCAB_PATH = os.path.join(DATA_DIR, "vocab.json")
SAVE_PATH = os.path.join(DATA_DIR, "progress.json")

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Word Explorer"

FONT_NAME = "Segoe UI"

COLORS = {
    "background": (245, 247, 250),
    "panel": (255, 255, 255),
    "primary": (47, 111, 237),
    "primary_dark": (34, 88, 187),
    "secondary": (246, 183, 60),
    "accent": (51, 196, 159),
    "danger": (241, 107, 107),
    "text": (30, 35, 50),
    "muted": (107, 114, 128),
    "shadow": (210, 217, 226),
    "outline": (224, 229, 236),
    "highlight": (236, 245, 255),
}
