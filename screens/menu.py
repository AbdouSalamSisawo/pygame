import pygame

from config import COLORS, SCREEN_HEIGHT, SCREEN_WIDTH
from scene import BaseScene
from ui import Button, draw_panel


class MenuScene(BaseScene):
    def __init__(self, context):
        super().__init__(context)
        font_button = context.fonts["button"]
        button_w, button_h = 320, 68
        gap = 16
        total_height = 4 * button_h + 3 * gap
        self.panel_rect = pygame.Rect(0, 0, 720, total_height + 100)
        self.panel_rect.centerx = SCREEN_WIDTH // 2
        self.panel_rect.top = 220
        start_y = self.panel_rect.top + 40
        if context.voice:
            context.voice.speak(
                "Welcome to Word Explorer. Choose Start Game, Instructions, Settings, or Exit."
            )

        def start_game():
            from screens.game import GameScene

            context.audio.play_click()
            self.manager.go_to(GameScene(context))

        def open_instructions():
            from screens.instructions import InstructionsScene

            context.audio.play_click()
            self.manager.go_to(InstructionsScene(context))

        def open_settings():
            from screens.settings import SettingsScene

            context.audio.play_click()
            self.manager.go_to(SettingsScene(context))

        def exit_game():
            context.audio.play_click()
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        self.buttons = [
            Button(
                (
                    (SCREEN_WIDTH - button_w) // 2,
                    start_y,
                    button_w,
                    button_h,
                ),
                "Start Game",
                font_button,
                start_game,
            ),
            Button(
                (
                    (SCREEN_WIDTH - button_w) // 2,
                    start_y + (button_h + gap),
                    button_w,
                    button_h,
                ),
                "Instructions",
                font_button,
                open_instructions,
            ),
            Button(
                (
                    (SCREEN_WIDTH - button_w) // 2,
                    start_y + 2 * (button_h + gap),
                    button_w,
                    button_h,
                ),
                "Settings",
                font_button,
                open_settings,
            ),
            Button(
                (
                    (SCREEN_WIDTH - button_w) // 2,
                    start_y + 3 * (button_h + gap),
                    button_w,
                    button_h,
                ),
                "Exit",
                font_button,
                exit_game,
                base_color=COLORS["danger"],
                hover_color=COLORS["danger"],
            ),
        ]

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def update(self, dt):
        return None

    def draw(self, surface):
        surface.fill(COLORS["background"])
        title_font = self.context.fonts["title"]
        subtitle_font = self.context.fonts["text"]
        title = title_font.render("Word Explorer", True, COLORS["text"])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        surface.blit(title, title_rect)

        subtitle = subtitle_font.render("Clean, friendly word practice for kids", True, COLORS["muted"])
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 150))
        surface.blit(subtitle, subtitle_rect)

        divider_y = self.panel_rect.top - 18
        pygame.draw.line(
            surface,
            COLORS["outline"],
            (SCREEN_WIDTH // 2 - 260, divider_y),
            (SCREEN_WIDTH // 2 + 260, divider_y),
            width=2,
        )
        draw_panel(surface, self.panel_rect, radius=24)

        for button in self.buttons:
            button.draw(surface)
