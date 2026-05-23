import pygame

from config import COLORS, SCREEN_HEIGHT, SCREEN_WIDTH
from scene import BaseScene
from storage.progress import default_progress, save_progress
from ui import Button, draw_panel


class SettingsScene(BaseScene):
    def __init__(self, context):
        super().__init__(context)
        self.progress = context.progress
        self.voice = context.voice
        self.difficulty_options = ["easy", "normal", "hard"]
        self.button_font = context.fonts["button"]
        self.text_font = context.fonts["text"]

        self.panel_rect = pygame.Rect(0, 0, SCREEN_WIDTH - 220, 660)
        self.panel_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)
        left = self.panel_rect.left + 60
        control_left = self.panel_rect.left + 220
        control_right = self.panel_rect.left + 440

        self.back_button = Button(
            (40, SCREEN_HEIGHT - 90, 220, 60),
            "Back",
            self.button_font,
            self.go_back,
            base_color=COLORS["secondary"],
        )
        self.volume_down = Button(
            (control_left, self.panel_rect.top + 110, 70, 60),
            "-",
            self.button_font,
            self.volume_lower,
            base_color=COLORS["primary"],
        )
        self.volume_up = Button(
            (control_right, self.panel_rect.top + 110, 70, 60),
            "+",
            self.button_font,
            self.volume_raise,
            base_color=COLORS["primary"],
        )
        self.voice_input_button = Button(
            (control_left, self.panel_rect.top + 230, 310, 60),
            "",
            self.button_font,
            self.toggle_voice_input,
            base_color=COLORS["primary"],
        )
        self.voice_output_button = Button(
            (control_left, self.panel_rect.top + 340, 310, 60),
            "",
            self.button_font,
            self.toggle_voice_output,
            base_color=COLORS["primary"],
        )
        self.voice_volume_down = Button(
            (control_left, self.panel_rect.top + 450, 70, 60),
            "-",
            self.button_font,
            self.voice_volume_lower,
            base_color=COLORS["primary"],
        )
        self.voice_volume_up = Button(
            (control_right, self.panel_rect.top + 450, 70, 60),
            "+",
            self.button_font,
            self.voice_volume_raise,
            base_color=COLORS["primary"],
        )
        self.difficulty_button = Button(
            (control_left, self.panel_rect.top + 520, 310, 60),
            "",
            self.button_font,
            self.cycle_difficulty,
            base_color=COLORS["accent"],
        )
        self.reset_button = Button(
            (control_left, self.panel_rect.top + 590, 310, 60),
            "Reset Progress",
            self.button_font,
            self.reset_progress,
            base_color=COLORS["danger"],
        )
        self.label_positions = {
            "volume": (left, self.panel_rect.top + 80),
            "voice_input": (left, self.panel_rect.top + 200),
            "voice_output": (left, self.panel_rect.top + 310),
            "voice_volume": (left, self.panel_rect.top + 420),
        }

    def _difficulty_label(self):
        current = self.progress["settings"].get("difficulty_bias", "normal")
        return f"Difficulty: {current.title()}"

    def volume_lower(self):
        volume = max(0.0, self.progress["settings"]["volume"] - 0.1)
        self.progress["settings"]["volume"] = round(volume, 2)
        self.context.audio.set_volume(volume)
        save_progress(self.progress)

    def volume_raise(self):
        volume = min(1.0, self.progress["settings"]["volume"] + 0.1)
        self.progress["settings"]["volume"] = round(volume, 2)
        self.context.audio.set_volume(volume)
        save_progress(self.progress)

    def _voice_input_label(self):
        enabled = self.progress["settings"].get("voice_input", True)
        return f"Voice Input: {'On' if enabled else 'Off'}"

    def _voice_output_label(self):
        enabled = self.progress["settings"].get("voice_output", True)
        return f"Voice Output: {'On' if enabled else 'Off'}"

    def toggle_voice_input(self):
        value = not self.progress["settings"].get("voice_input", True)
        self.progress["settings"]["voice_input"] = value
        self.voice.set_input_enabled(value)
        save_progress(self.progress)

    def toggle_voice_output(self):
        value = not self.progress["settings"].get("voice_output", True)
        self.progress["settings"]["voice_output"] = value
        self.voice.set_output_enabled(value)
        save_progress(self.progress)

    def voice_volume_lower(self):
        volume = max(0.0, self.progress["settings"].get("voice_volume", 0.8) - 0.1)
        self.progress["settings"]["voice_volume"] = round(volume, 2)
        self.voice.set_volume(volume)
        save_progress(self.progress)

    def voice_volume_raise(self):
        volume = min(1.0, self.progress["settings"].get("voice_volume", 0.8) + 0.1)
        self.progress["settings"]["voice_volume"] = round(volume, 2)
        self.voice.set_volume(volume)
        save_progress(self.progress)

    def cycle_difficulty(self):
        current = self.progress["settings"].get("difficulty_bias", "normal")
        index = self.difficulty_options.index(current)
        new_value = self.difficulty_options[(index + 1) % len(self.difficulty_options)]
        self.progress["settings"]["difficulty_bias"] = new_value
        save_progress(self.progress)

    def reset_progress(self):
        settings = dict(self.progress.get("settings", {}))
        self.progress.clear()
        self.progress.update(default_progress())
        self.progress["settings"].update(settings)
        save_progress(self.progress)

    def go_back(self):
        from screens.menu import MenuScene

        self.context.audio.play_click()
        self.manager.go_to(MenuScene(self.context))

    def handle_event(self, event):
        for button in [
            self.back_button,
            self.volume_down,
            self.volume_up,
            self.voice_input_button,
            self.voice_output_button,
            self.voice_volume_down,
            self.voice_volume_up,
            self.difficulty_button,
            self.reset_button,
        ]:
            button.handle_event(event)

    def update(self, dt):
        self.difficulty_button.text = self._difficulty_label()
        self.voice_input_button.text = self._voice_input_label()
        self.voice_output_button.text = self._voice_output_label()
        self.voice_input_button.enabled = self.voice.input.available
        self.voice_output_button.enabled = self.voice.output.available
        self.voice_volume_down.enabled = self.voice.output.available
        self.voice_volume_up.enabled = self.voice.output.available

    def draw(self, surface):
        surface.fill(COLORS["background"])
        title = self.context.fonts["title"].render("Settings", True, COLORS["text"])
        surface.blit(title, (60, 80))

        draw_panel(surface, self.panel_rect, radius=24)

        volume = int(self.progress["settings"]["volume"] * 100)
        volume_label = self.text_font.render("Sound Volume", True, COLORS["muted"])
        surface.blit(volume_label, self.label_positions["volume"])
        value_label = self.text_font.render(f"{volume}%", True, COLORS["text"])
        surface.blit(value_label, (self.panel_rect.left + 360, self.panel_rect.top + 80))

        voice_volume = int(self.progress["settings"].get("voice_volume", 0.8) * 100)
        voice_label = self.text_font.render("Voice Volume", True, COLORS["muted"])
        surface.blit(voice_label, self.label_positions["voice_volume"])
        voice_value = self.text_font.render(f"{voice_volume}%", True, COLORS["text"])
        surface.blit(voice_value, (self.panel_rect.left + 360, self.panel_rect.top + 420))

        for button in [
            self.volume_down,
            self.volume_up,
            self.voice_input_button,
            self.voice_output_button,
            self.voice_volume_down,
            self.voice_volume_up,
            self.difficulty_button,
            self.reset_button,
            self.back_button,
        ]:
            button.draw(surface)
