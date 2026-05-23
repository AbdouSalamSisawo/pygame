import math
from array import array

import pygame


def pre_init():
    pygame.mixer.pre_init(44100, -16, 1, 512)


def tone(frequency, duration_ms, volume=0.5, sample_rate=44100):
    total_samples = int(sample_rate * (duration_ms / 1000.0))
    amplitude = int(32767 * volume)
    buffer = array("h")
    for i in range(total_samples):
        sample = int(amplitude * math.sin(2 * math.pi * frequency * i / sample_rate))
        buffer.append(sample)
    return pygame.mixer.Sound(buffer=buffer)


class AudioManager:
    def __init__(self, volume=0.6):
        if not pygame.mixer.get_init():
            pygame.mixer.init(44100, -16, 1, 512)
        self.success = tone(660, 180, volume)
        self.fail = tone(220, 180, volume)
        self.click = tone(520, 80, volume)
        self.set_volume(volume)

    def set_volume(self, volume):
        self.success.set_volume(volume)
        self.fail.set_volume(volume)
        self.click.set_volume(volume)

    def play_success(self):
        self.success.play()

    def play_fail(self):
        self.fail.play()

    def play_click(self):
        self.click.play()
