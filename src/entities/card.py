import pygame
import math
from config import CARD_BACK, CARD_FRONT, ACCENT, FONT_EMOJI

class Card:
    def __init__(self, index, emoji, r, c):
        self.index = index
        self.emoji = emoji
        self.rect = pygame.Rect(c * 150 + 10, r * 150 + 10, 130, 130)
        self.state = 0  # 0: hidden, 1: flipping open, 2: opened, 3: flipping closed
        self.flip_frame = 0

    def update(self):
        if self.state == 1:
            self.flip_frame += 15
            if self.flip_frame >= 180: self.flip_frame = 180; self.state = 2
        elif self.state == 3:
            self.flip_frame -= 15
            if self.flip_frame <= 0: self.flip_frame = 0; self.state = 0

    def draw(self, screen):
        angle = math.radians(self.flip_frame)
        width = 130 * abs(math.cos(angle))
        display_rect = pygame.Rect(self.rect.x + (130 - width) / 2, self.rect.y, width, 130)
        
        if self.flip_frame < 90:
            pygame.draw.rect(screen, CARD_BACK, display_rect, border_radius=15)
            pygame.draw.rect(screen, ACCENT, display_rect, 2, border_radius=15)
        else:
            pygame.draw.rect(screen, CARD_FRONT, display_rect, border_radius=15)
            if width > 20:
                e_surf = FONT_EMOJI.render(self.emoji, True, (0, 0, 0))
                e_scaled = pygame.transform.scale(e_surf, (int(width * 0.7), 80))
                screen.blit(e_scaled, (display_rect.centerx - e_scaled.get_width()//2, display_rect.centery - 40))