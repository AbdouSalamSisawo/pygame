import json

import pygame

from audio import AudioManager, pre_init
from config import FPS, FONT_NAME, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, VOCAB_PATH
from scene import SceneManager
from screens.menu import MenuScene
from storage.progress import load_progress, save_progress
from voice import VoiceManager


class AppContext:
    def __init__(self, screen, clock, fonts, vocab, progress, audio, voice):
        self.screen = screen
        self.clock = clock
        self.fonts = fonts
        self.vocab = vocab
        self.progress = progress
        self.audio = audio
        self.voice = voice


def load_vocab():
    with open(VOCAB_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


def build_fonts():
    return {
        "title": pygame.font.SysFont(FONT_NAME, 56, bold=True),
        "subtitle": pygame.font.SysFont(FONT_NAME, 32, bold=True),
        "button": pygame.font.SysFont(FONT_NAME, 34, bold=True),
        "text": pygame.font.SysFont(FONT_NAME, 26),
        "small": pygame.font.SysFont(FONT_NAME, 20),
    }


def main():
    pre_init()
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    fonts = build_fonts()
    vocab = load_vocab()
    progress = load_progress()
    audio = AudioManager(progress["settings"]["volume"])
    voice = VoiceManager(progress["settings"])

    context = AppContext(screen, clock, fonts, vocab, progress, audio, voice)
    manager = SceneManager(MenuScene(context))

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                manager.handle_event(event)
        manager.update(dt)
        manager.draw(screen)
        pygame.display.flip()

    save_progress(progress)
    pygame.quit()


if __name__ == "__main__":
    main()
