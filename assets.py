import pygame
from config import COLORS


def hex_to_rgb(hex_color):
    value = hex_color.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def draw_icon(surface, rect, icon_id, color, background=None):
    cx, cy = rect.center
    radius = min(rect.width, rect.height) // 3
    bg = background or COLORS["panel"]
    if icon_id == "sun":
        pygame.draw.circle(surface, color, (cx, cy), radius)
        for angle in range(0, 360, 45):
            vec = pygame.math.Vector2(radius + 8, 0).rotate(angle)
            start = (cx + vec.x * 0.75, cy + vec.y * 0.75)
            end = (cx + vec.x, cy + vec.y)
            pygame.draw.line(surface, color, start, end, width=3)
    elif icon_id == "moon":
        pygame.draw.circle(surface, color, (cx, cy), radius)
        offset = radius // 2
        pygame.draw.circle(surface, bg, (cx + offset, cy - offset // 2), radius)
    elif icon_id == "leaf":
        leaf_rect = pygame.Rect(0, 0, radius * 2, radius * 1.4)
        leaf_rect.center = (cx, cy)
        pygame.draw.ellipse(surface, color, leaf_rect)
        pygame.draw.line(
            surface,
            COLORS["panel"],
            (leaf_rect.centerx - radius // 2, leaf_rect.centery),
            (leaf_rect.centerx + radius // 2, leaf_rect.centery),
            width=3,
        )
    elif icon_id == "tree":
        trunk = pygame.Rect(0, 0, radius * 0.6, radius * 1.1)
        trunk.center = (cx, cy + radius // 2)
        pygame.draw.rect(surface, (139, 94, 60), trunk, border_radius=4)
        pygame.draw.circle(surface, color, (cx, cy - radius // 4), int(radius * 1.1))
    elif icon_id == "ball":
        pygame.draw.circle(surface, color, (cx, cy), radius)
        highlight = pygame.Rect(0, 0, radius, radius)
        highlight.center = (cx - radius // 3, cy - radius // 3)
        pygame.draw.circle(surface, COLORS["panel"], highlight.center, radius // 3)
    elif icon_id == "kite":
        points = [
            (cx, cy - radius),
            (cx - radius, cy),
            (cx, cy + radius),
            (cx + radius, cy),
        ]
        pygame.draw.polygon(surface, color, points)
        pygame.draw.line(surface, color, (cx, cy + radius), (cx, cy + radius * 1.6), width=3)
        pygame.draw.circle(surface, color, (cx, int(cy + radius * 1.8)), 4)
    elif icon_id == "fish":
        body = pygame.Rect(0, 0, radius * 2, radius * 1.2)
        body.center = (cx, cy)
        pygame.draw.ellipse(surface, color, body)
        tail = [
            (body.right, cy),
            (body.right + radius // 1, cy - radius // 2),
            (body.right + radius // 1, cy + radius // 2),
        ]
        pygame.draw.polygon(surface, color, tail)
        pygame.draw.circle(surface, COLORS["panel"], (body.left + radius // 2, cy - 4), 4)
    elif icon_id == "bird":
        body = pygame.Rect(0, 0, radius * 1.8, radius * 1.1)
        body.center = (cx, cy)
        pygame.draw.ellipse(surface, color, body)
        wing = pygame.Rect(0, 0, radius, radius // 1)
        wing.center = (cx - radius // 4, cy)
        pygame.draw.ellipse(surface, COLORS["panel"], wing)
        beak = [(body.right, cy), (body.right + 8, cy - 4), (body.right + 8, cy + 4)]
        pygame.draw.polygon(surface, color, beak)
    elif icon_id == "apple":
        pygame.draw.circle(surface, color, (cx, cy), radius)
        stem = pygame.Rect(0, 0, radius // 3, radius // 1)
        stem.center = (cx, cy - radius)
        pygame.draw.rect(surface, (120, 80, 40), stem, border_radius=4)
        leaf = pygame.Rect(0, 0, radius, radius // 2)
        leaf.center = (cx + radius // 2, cy - radius)
        pygame.draw.ellipse(surface, (76, 175, 80), leaf)
    elif icon_id == "book":
        book = pygame.Rect(0, 0, radius * 2, radius * 1.5)
        book.center = (cx, cy)
        pygame.draw.rect(surface, color, book, border_radius=6)
        pygame.draw.line(surface, COLORS["panel"], (cx, book.top + 6), (cx, book.bottom - 6), width=3)
    elif icon_id == "car":
        body = pygame.Rect(0, 0, radius * 2.2, radius * 1.1)
        body.center = (cx, cy + radius // 6)
        pygame.draw.rect(surface, color, body, border_radius=10)
        top = pygame.Rect(0, 0, radius * 1.4, radius * 0.8)
        top.midbottom = (cx, body.top + 4)
        pygame.draw.rect(surface, color, top, border_radius=8)
        wheel_y = body.bottom + 2
        pygame.draw.circle(surface, COLORS["text"], (body.left + radius // 2, wheel_y), radius // 3)
        pygame.draw.circle(surface, COLORS["text"], (body.right - radius // 2, wheel_y), radius // 3)
    elif icon_id == "hat":
        cap = pygame.Rect(0, 0, radius * 2, radius)
        cap.midbottom = (cx, cy + radius // 2)
        pygame.draw.ellipse(surface, color, cap)
        brim = pygame.Rect(0, 0, radius * 2.4, radius * 0.5)
        brim.midtop = (cx, cy + radius // 2)
        pygame.draw.ellipse(surface, color, brim)
    elif icon_id == "circle":
        pygame.draw.circle(surface, color, (cx, cy), radius)
    elif icon_id == "square":
        square = pygame.Rect(0, 0, radius * 2, radius * 2)
        square.center = rect.center
        pygame.draw.rect(surface, color, square, border_radius=6)
    elif icon_id == "triangle":
        points = [
            (cx, cy - radius),
            (cx - radius, cy + radius),
            (cx + radius, cy + radius),
        ]
        pygame.draw.polygon(surface, color, points)
    elif icon_id == "diamond":
        points = [
            (cx, cy - radius),
            (cx - radius, cy),
            (cx, cy + radius),
            (cx + radius, cy),
        ]
        pygame.draw.polygon(surface, color, points)
    elif icon_id == "star":
        draw_star(surface, (cx, cy), radius, color)
    elif icon_id == "heart":
        left = pygame.Rect(cx - radius, cy - radius // 2, radius, radius)
        right = pygame.Rect(cx, cy - radius // 2, radius, radius)
        pygame.draw.circle(surface, color, left.center, radius // 2)
        pygame.draw.circle(surface, color, right.center, radius // 2)
        points = [(cx - radius, cy), (cx + radius, cy), (cx, cy + radius)]
        pygame.draw.polygon(surface, color, points)
    else:
        pygame.draw.circle(surface, color, (cx, cy), radius)


def draw_card(surface, rect, word, color, icon_id, font, show_word=True, border_color=None):
    shadow_rect = rect.move(0, 6)
    pygame.draw.rect(surface, COLORS["shadow"], shadow_rect, border_radius=18)
    pygame.draw.rect(surface, COLORS["panel"], rect, border_radius=18)
    border = border_color or COLORS["outline"]
    pygame.draw.rect(surface, border, rect, width=2, border_radius=18)
    icon_rect = pygame.Rect(0, 0, rect.width * 0.6, rect.height * 0.55)
    icon_rect.center = (rect.centerx, rect.centery - rect.height * 0.1)
    draw_icon(surface, icon_rect, icon_id, color, background=COLORS["panel"])
    if show_word:
        text_surf = font.render(word, True, COLORS["text"])
        text_rect = text_surf.get_rect(center=(rect.centerx, rect.bottom - rect.height * 0.2))
        surface.blit(text_surf, text_rect)


def draw_star(surface, center, radius, color):
    cx, cy = center
    points = []
    for i in range(10):
        angle = i * 36
        point_radius = radius if i % 2 == 0 else radius * 0.45
        x = cx + point_radius * pygame.math.Vector2(1, 0).rotate(angle).x
        y = cy + point_radius * pygame.math.Vector2(1, 0).rotate(angle).y
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)
