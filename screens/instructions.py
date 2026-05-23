import pygame

from config import COLORS, SCREEN_HEIGHT, SCREEN_WIDTH
from scene import BaseScene
from ui import Button, draw_panel, draw_text_lines, wrap_text


class InstructionsScene(BaseScene):
    def __init__(self, context):
        super().__init__(context)
        font_button = context.fonts["button"]
        self.back_button = Button(
            (40, SCREEN_HEIGHT - 90, 220, 60),
            "Back",
            font_button,
            self.go_back,
            base_color=COLORS["secondary"],
            hover_color=COLORS["primary"],
        )
        self.instructions = [
            "Look at the picture or word on the screen.",
            "Tap the matching word or picture.",
            "If you miss, the game gives a gentle hint.",
            "Collect stars as you learn new words.",
        ]
        self.panel_rect = pygame.Rect(0, 0, SCREEN_WIDTH - 200, 380)
        self.panel_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
        if context.voice:
            context.voice.speak(
                "How to play. Look at the picture or word, then tap the match. "
                "If you miss, you get a gentle hint. Collect stars as you learn."
            )

    def go_back(self):
        from screens.menu import MenuScene

        self.context.audio.play_click()
        self.manager.go_to(MenuScene(self.context))

    def handle_event(self, event):
        self.back_button.handle_event(event)

    def update(self, dt):
        return None

    def draw(self, surface):
        surface.fill(COLORS["background"])
        title_font = self.context.fonts["title"]
        title = title_font.render("How to Play", True, COLORS["text"])
        surface.blit(title, (60, 80))

        draw_panel(surface, self.panel_rect, radius=24)

        text_font = self.context.fonts["text"]
        wrap_width = self.panel_rect.width - 120
        y = self.panel_rect.top + 60
        for line in self.instructions:
            lines = wrap_text(line, text_font, wrap_width)
            draw_text_lines(surface, lines, text_font, COLORS["text"], (self.panel_rect.left + 60, y))
            y += text_font.get_linesize() * (len(lines) + 1)

        self.back_button.draw(surface)
