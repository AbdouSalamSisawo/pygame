import pygame
from config import COLORS


def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            line = test_line
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_text_lines(surface, lines, font, color, topleft, line_height=None):
    x, y = topleft
    height = line_height or font.get_linesize()
    for line in lines:
        text_surf = font.render(line, True, color)
        surface.blit(text_surf, (x, y))
        y += height


def draw_panel(surface, rect, radius=18, fill_color=None, outline=True, shadow=True):
    fill = fill_color or COLORS["panel"]
    if shadow:
        shadow_rect = rect.move(0, 6)
        pygame.draw.rect(surface, COLORS["shadow"], shadow_rect, border_radius=radius)
    pygame.draw.rect(surface, fill, rect, border_radius=radius)
    if outline:
        pygame.draw.rect(surface, COLORS["outline"], rect, width=2, border_radius=radius)


def draw_button(
    surface,
    rect,
    text,
    font,
    base_color,
    text_color,
    outline_color=None,
    shadow=True,
    disabled=False,
):
    if shadow:
        shadow_rect = rect.move(0, 4)
        pygame.draw.rect(surface, COLORS["shadow"], shadow_rect, border_radius=14)

    if disabled:
        base_color = COLORS["outline"]
        text_color = COLORS["muted"]

    if outline_color:
        pygame.draw.rect(surface, outline_color, rect, border_radius=14)
        inner = rect.inflate(-4, -4)
        pygame.draw.rect(surface, base_color, inner, border_radius=12)
    else:
        pygame.draw.rect(surface, base_color, rect, border_radius=14)

    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)


class Button:
    def __init__(
        self,
        rect,
        text,
        font,
        on_click,
        base_color=None,
        hover_color=None,
        text_color=None,
        enabled=True,
        outline_color=None,
        shadow=True,
    ):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.on_click = on_click
        self.base_color = base_color or COLORS["primary"]
        self.hover_color = hover_color or COLORS["primary_dark"]
        self.text_color = text_color or COLORS["panel"]
        self.enabled = enabled
        self.outline_color = outline_color
        self.shadow = shadow

    def handle_event(self, event):
        if not self.enabled:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.enabled and self.rect.collidepoint(mouse_pos)
        color = self.hover_color if is_hover else self.base_color
        draw_button(
            surface,
            self.rect,
            self.text,
            self.font,
            color,
            self.text_color,
            outline_color=self.outline_color,
            shadow=self.shadow,
            disabled=not self.enabled,
        )
