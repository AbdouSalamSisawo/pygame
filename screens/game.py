import queue
import time

import pygame

from ai.adaptive import AdaptiveTracker
from assets import draw_card, draw_star, hex_to_rgb
from config import COLORS, SCREEN_HEIGHT, SCREEN_WIDTH
from gameplay.rounds import build_round
from scene import BaseScene
from storage.progress import save_progress
from ui import Button, draw_button, draw_panel


class GameScene(BaseScene):
    def __init__(self, context):
        super().__init__(context)
        self.progress = context.progress
        self.voice = context.voice
        self.tracker = AdaptiveTracker(self.progress)
        self.bias = self.progress["settings"].get("difficulty_bias", "normal")
        self.score = 0
        self.stars = 0
        self.rounds_played = 0
        self.target_rounds = 10
        self.session_correct = 0
        self.session_wrong = 0
        self.session_start = time.time()
        self.message = ""
        self.message_color = COLORS["text"]
        self.message_timer = 0.0
        self.next_round_timer = 0.0
        self.session_complete = False
        self.highlight_correct = False
        self.option_layout = []
        self.prompt_text = ""
        self.selected_index = 0
        self.voice_status = ""
        self.voice_status_timer = 0.0
        self.voice_events = queue.Queue()

        self.back_button = Button(
            (30, 24, 160, 52),
            "Menu",
            context.fonts["text"],
            self.go_menu,
            base_color=COLORS["secondary"],
        )
        self.mic_button = Button(
            (SCREEN_WIDTH - 170, 140, 110, 44),
            "Mic",
            context.fonts["text"],
            self.toggle_listening,
            base_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
        )
        self.continue_button = Button(
            (
                SCREEN_WIDTH // 2 - 240,
                SCREEN_HEIGHT // 2 + 120,
                220,
                64,
            ),
            "Play Again",
            context.fonts["button"],
            self.start_new_session,
            base_color=COLORS["accent"],
        )
        self.exit_button = Button(
            (
                SCREEN_WIDTH // 2 + 20,
                SCREEN_HEIGHT // 2 + 120,
                220,
                64,
            ),
            "Return Home",
            context.fonts["button"],
            self.go_menu,
            base_color=COLORS["secondary"],
        )
        self.top_bar_rect = pygame.Rect(24, 20, SCREEN_WIDTH - 48, 86)
        self.play_rect = pygame.Rect(80, 120, SCREEN_WIDTH - 160, SCREEN_HEIGHT - 200)
        if self.voice:
            self.voice.speak("Let's play! Use the mouse or arrow keys to choose.")
        self.start_new_round()

    def go_menu(self):
        from screens.menu import MenuScene

        self.context.audio.play_click()
        if self.voice:
            self.voice.stop_listening()
        save_progress(self.progress)
        self.manager.go_to(MenuScene(self.context))

    def exit_game(self):
        self.context.audio.play_click()
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def start_new_session(self):
        self.context.audio.play_click()
        self.score = 0
        self.stars = 0
        self.rounds_played = 0
        self.session_correct = 0
        self.session_wrong = 0
        self.session_start = time.time()
        self.session_complete = False
        self.selected_index = 0
        self.start_new_round()

    def start_new_round(self):
        self.bias = self.progress["settings"].get("difficulty_bias", "normal")
        self.round_state = build_round(self.context.vocab, self.tracker, self.bias)
        if self.round_state["activity"] == "image_to_word":
            self.prompt_text = "Match the picture to the word"
        else:
            self.prompt_text = "Match the word to the picture"
        if self.voice:
            self.voice.speak(self.prompt_text)
        self.message = ""
        self.message_timer = 0.0
        self.next_round_timer = 0.0
        self.highlight_correct = False
        self.option_layout = self.compute_option_layout()
        self.ensure_selection()

    def compute_option_layout(self):
        options = self.round_state["options"]
        count = len(options)
        spacing = 24

        if self.round_state["activity"] == "image_to_word":
            button_w = 240 if count <= 3 else 200
            button_h = 70
            total_w = count * button_w + (count - 1) * spacing
            start_x = self.play_rect.centerx - total_w // 2
            y = self.play_rect.bottom - 120
            layout = []
            for index, item in enumerate(options):
                rect = pygame.Rect(start_x + index * (button_w + spacing), y, button_w, button_h)
                enabled = index not in self.round_state["eliminated"]
                layout.append({"rect": rect, "item": item, "enabled": enabled})
            return layout

        card_size = 200 if count <= 3 else 170
        total_w = count * card_size + (count - 1) * spacing
        start_x = self.play_rect.centerx - total_w // 2
        y = self.play_rect.centery + 40
        layout = []
        for index, item in enumerate(options):
            rect = pygame.Rect(start_x + index * (card_size + spacing), y, card_size, card_size)
            enabled = index not in self.round_state["eliminated"]
            layout.append({"rect": rect, "item": item, "enabled": enabled})
        return layout

    def apply_hint(self):
        self.highlight_correct = True
        if self.round_state["round_wrong"] >= 2:
            for index, option in enumerate(self.round_state["options"]):
                if option["word"] != self.round_state["target"]["word"]:
                    if index not in self.round_state["eliminated"]:
                        self.round_state["eliminated"].add(index)
                        break
        self.option_layout = self.compute_option_layout()
        self.ensure_selection()

    def ensure_selection(self):
        if not self.option_layout:
            self.selected_index = 0
            return
        if self.selected_index >= len(self.option_layout):
            self.selected_index = 0
        if not self.option_layout[self.selected_index]["enabled"]:
            for index, option in enumerate(self.option_layout):
                if option["enabled"]:
                    self.selected_index = index
                    break

    def move_selection(self, delta):
        self.option_layout = self.compute_option_layout()
        enabled_indices = [i for i, option in enumerate(self.option_layout) if option["enabled"]]
        if not enabled_indices:
            return
        if self.selected_index not in enabled_indices:
            self.selected_index = enabled_indices[0]
            return
        current_pos = enabled_indices.index(self.selected_index)
        new_pos = (current_pos + delta) % len(enabled_indices)
        self.selected_index = enabled_indices[new_pos]

    def activate_selection(self):
        self.option_layout = self.compute_option_layout()
        if 0 <= self.selected_index < len(self.option_layout):
            option = self.option_layout[self.selected_index]
            if option["enabled"]:
                self.evaluate_choice(option["item"])

    def handle_event(self, event):
        self.back_button.handle_event(event)
        self.mic_button.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.go_menu()
                return
            if self.session_complete:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.start_new_session()
                return
            if self.next_round_timer > 0:
                return
            if event.key == pygame.K_LEFT:
                self.move_selection(-1)
                return
            if event.key == pygame.K_RIGHT:
                self.move_selection(1)
                return
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.activate_selection()
                return
        if self.session_complete:
            self.continue_button.handle_event(event)
            self.exit_button.handle_event(event)
            return
        if self.next_round_timer > 0:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.option_layout = self.compute_option_layout()
            for index, option in enumerate(self.option_layout):
                if option["enabled"] and option["rect"].collidepoint(event.pos):
                    self.selected_index = index
                    self.evaluate_choice(option["item"])
                    break

    def toggle_listening(self):
        if not self.voice:
            return
        if self.voice.listening:
            self.voice.stop_listening()
            self.set_voice_status("Listening stopped.")
            return
        started = self.voice.start_listening(self.on_voice_text, self.on_voice_error, timeout=6)
        if not started:
            status = self.voice.status or "Voice input not ready."
            self.set_voice_status(status)

    def on_voice_text(self, text):
        self.voice_events.put(("text", text))

    def on_voice_error(self, message):
        self.voice_events.put(("error", message))

    def handle_voice_text(self, text):
        if self.session_complete:
            return
        self.set_voice_status(f"You said: {text}")
        normalized = text.lower()
        if "menu" in normalized or "home" in normalized or "exit" in normalized:
            self.go_menu()
            return
        if "repeat" in normalized:
            if self.voice:
                self.voice.speak(self.prompt_text)
            return
        for index, option in enumerate(self.round_state["options"]):
            if index in self.round_state["eliminated"]:
                continue
            if option["word"] in normalized:
                self.selected_index = index
                # `option` here is a vocab item (dict with keys like 'word', 'icon', 'color').
                # Pass the vocab item directly to `evaluate_choice` (it expects the item).
                self.evaluate_choice(option)
                return
        self.set_voice_status("I didn't hear a game word. Try again.")
        if self.voice:
            self.voice.speak("I did not hear a game word. Try again.")

    def handle_voice_error(self, message):
        self.set_voice_status(message)
        if self.voice and message:
            self.voice.speak(message)

    def set_voice_status(self, text):
        self.voice_status = text
        self.voice_status_timer = 2.5

    def evaluate_choice(self, selected_item):
        target = self.round_state["target"]
        correct = selected_item["word"] == target["word"]
        self.tracker.record(target["word"], correct)

        if correct:
            self.context.audio.play_success()
            if self.voice:
                self.voice.speak(f"Great job! {target['word']} is correct.")
            self.progress["totals"]["correct"] += 1
            self.score += 1
            self.session_correct += 1
            self.rounds_played += 1
            new_stars = self.score // 5
            if new_stars > self.stars:
                self.stars = new_stars
                self.progress["totals"]["stars"] += 1
            self.message = "Great job!"
            self.message_color = COLORS["accent"]
            self.message_timer = 1.0
            if self.rounds_played >= self.target_rounds:
                self.complete_session()
            else:
                self.next_round_timer = 0.8
        else:
            self.context.audio.play_fail()
            if self.voice:
                hint = f"Try again. The word starts with {target['word'][0]}."
                self.voice.speak(hint)
            self.progress["totals"]["wrong"] += 1
            self.session_wrong += 1
            self.round_state["round_wrong"] += 1
            self.message = "Try again! Here's a hint."
            self.message_color = COLORS["danger"]
            self.message_timer = 1.0
            self.apply_hint()

        save_progress(self.progress)

    def complete_session(self):
        duration = int(time.time() - self.session_start)
        self.progress["sessions"].append(
            {
                "timestamp": time.time(),
                "duration": duration,
                "correct": self.session_correct,
                "wrong": self.session_wrong,
            }
        )
        if len(self.progress["sessions"]) > 20:
            self.progress["sessions"] = self.progress["sessions"][-20:]
        self.session_complete = True
        self.next_round_timer = 0.0
        if self.voice:
            self.voice.stop_listening()
            self.voice.speak("Session complete! You did amazing.")
        save_progress(self.progress)

    def update(self, dt):
        if self.message_timer > 0:
            self.message_timer = max(0.0, self.message_timer - dt)
        if self.next_round_timer > 0:
            self.next_round_timer -= dt
            if self.next_round_timer <= 0 and not self.session_complete:
                self.start_new_round()
        if self.voice_status_timer > 0:
            self.voice_status_timer = max(0.0, self.voice_status_timer - dt)
        if self.voice and self.voice.status:
            self.voice_status = self.voice.status
        while not self.voice_events.empty():
            event_type, payload = self.voice_events.get_nowait()
            if event_type == "text":
                self.handle_voice_text(payload)
            elif event_type == "error":
                self.handle_voice_error(payload)

    def draw_top_bar(self, surface):
        draw_panel(surface, self.top_bar_rect, radius=20)
        font = self.context.fonts["text"]
        score_text = font.render(f"Score {self.score}", True, COLORS["text"])
        surface.blit(score_text, (self.top_bar_rect.left + 170, self.top_bar_rect.top + 28))

        round_text = font.render(f"Round {self.rounds_played}/{self.target_rounds}", True, COLORS["muted"])
        surface.blit(round_text, (self.top_bar_rect.left + 330, self.top_bar_rect.top + 28))

        star_x = self.top_bar_rect.right - 220
        for i in range(self.stars):
            draw_star(surface, (star_x + i * 26, self.top_bar_rect.top + 32), 10, COLORS["secondary"])

        progress_ratio = self.rounds_played / self.target_rounds
        bar_width = 300
        bar_rect = pygame.Rect(self.top_bar_rect.right - bar_width - 40, self.top_bar_rect.top + 52, bar_width, 12)
        pygame.draw.rect(surface, COLORS["outline"], bar_rect, border_radius=8)
        fill_width = int(bar_width * progress_ratio)
        fill_rect = pygame.Rect(bar_rect.x, bar_rect.y, fill_width, bar_rect.height)
        pygame.draw.rect(surface, COLORS["primary"], fill_rect, border_radius=8)
        if self.voice_status_timer > 0 and self.voice_status:
            status_font = self.context.fonts["small"]
            status = status_font.render(self.voice_status, True, COLORS["muted"])
            surface.blit(status, (self.top_bar_rect.left + 40, self.top_bar_rect.top + 54))

    def draw_prompt(self, surface):
        prompt = self.context.fonts["subtitle"].render(self.prompt_text, True, COLORS["text"])
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, self.play_rect.top + 40))
        surface.blit(prompt, prompt_rect)

    def draw_message(self, surface):
        if self.message_timer > 0:
            font = self.context.fonts["text"]
            text = font.render(self.message, True, self.message_color)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, self.play_rect.bottom - 40))
            surface.blit(text, rect)

    def draw_target(self, surface):
        target = self.round_state["target"]
        if self.round_state["activity"] == "image_to_word":
            card_rect = pygame.Rect(0, 0, 260, 260)
            card_rect.center = (SCREEN_WIDTH // 2, self.play_rect.centery - 40)
            color = hex_to_rgb(target["color"])
            draw_card(
                surface,
                card_rect,
                target["word"],
                color,
                target["icon"],
                self.context.fonts["text"],
                show_word=False,
                border_color=COLORS["highlight"],
            )
        else:
            word_font = self.context.fonts["title"]
            pill_rect = pygame.Rect(0, 0, 420, 96)
            pill_rect.center = (SCREEN_WIDTH // 2, self.play_rect.centery - 70)
            draw_panel(surface, pill_rect, radius=24, fill_color=COLORS["highlight"], shadow=False)
            text = word_font.render(target["word"].upper(), True, COLORS["text"])
            rect = text.get_rect(center=pill_rect.center)
            surface.blit(text, rect)

    def draw_options(self, surface):
        target_word = self.round_state["target"]["word"]
        for index, option in enumerate(self.option_layout):
            item = option["item"]
            rect = option["rect"]
            enabled = option["enabled"]
            is_correct = item["word"] == target_word
            is_selected = index == self.selected_index and enabled
            if self.round_state["activity"] == "image_to_word":
                base_color = COLORS["primary"] if enabled else COLORS["outline"]
                if self.highlight_correct and is_correct:
                    outline = COLORS["accent"]
                elif is_selected:
                    outline = COLORS["primary_dark"]
                else:
                    outline = COLORS["outline"]
                draw_button(
                    surface,
                    rect,
                    item["word"],
                    self.context.fonts["text"],
                    base_color,
                    COLORS["panel"],
                    outline_color=outline,
                    shadow=True,
                    disabled=not enabled,
                )
            else:
                color = hex_to_rgb(item["color"])
                draw_card(
                    surface,
                    rect,
                    item["word"],
                    color,
                    item["icon"],
                    self.context.fonts["small"],
                    show_word=False,
                )
                if self.highlight_correct and is_correct:
                    pygame.draw.rect(surface, COLORS["accent"], rect, width=4, border_radius=18)
                elif is_selected:
                    pygame.draw.rect(surface, COLORS["primary"], rect, width=4, border_radius=18)

            if not enabled:
                overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 170))
                surface.blit(overlay, rect.topleft)

    def draw_session_overlay(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((30, 30, 40, 160))
        surface.blit(overlay, (0, 0))
        title_font = self.context.fonts["title"]
        message = title_font.render("Session Complete!", True, COLORS["panel"])
        rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        surface.blit(message, rect)
        info_font = self.context.fonts["text"]
        info = info_font.render("You did amazing!", True, COLORS["panel"])
        info_rect = info.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        surface.blit(info, info_rect)
        self.continue_button.draw(surface)
        self.exit_button.draw(surface)

    def draw(self, surface):
        surface.fill(COLORS["background"])
        self.back_button.draw(surface)
        self.draw_top_bar(surface)
        draw_panel(surface, self.play_rect, radius=28)
        self.draw_prompt(surface)
        self.draw_target(surface)
        self.option_layout = self.compute_option_layout()
        self.draw_options(surface)
        self.draw_message(surface)
        if self.voice:
            if self.voice.listening:
                self.mic_button.text = "Listening"
                self.mic_button.base_color = COLORS["accent"]
            else:
                self.mic_button.text = "Mic"
                self.mic_button.base_color = COLORS["primary"]
            self.mic_button.enabled = self.voice.input_enabled and self.voice.input.available
            self.mic_button.draw(surface)
        if self.session_complete:
            self.draw_session_overlay(surface)
