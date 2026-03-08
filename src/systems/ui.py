import pygame
import random
from config import FONT_UI, BG_COLOR, TEXT_WHITE

class Button:
    def __init__(self, text, rect, color):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.color = color

    def draw(self, screen, mouse_pos):
        hover = self.rect.collidepoint(mouse_pos)
        display_rect = self.rect.inflate(10, 10) if hover else self.rect
        draw_color = self.color if hover else tuple(c * 0.7 for c in self.color)
        
        pygame.draw.rect(screen, draw_color, display_rect, border_radius=20)
        txt = FONT_UI.render(self.text, True, BG_COLOR if hover else TEXT_WHITE)
        screen.blit(txt, (display_rect.centerx - txt.get_width()//2, display_rect.centery - txt.get_height()//2))

    def is_clicked(self, mouse_pos, event):
        return self.rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def create(self, x, y, color, count=15):
        for _ in range(count):
            self.particles.append([x, y, random.uniform(-4, 4), random.uniform(-4, 4), 30, color])

    def update_and_draw(self, screen):
        for p in self.particles[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[4] -= 1
            if p[4] <= 0:
                self.particles.remove(p)
            else:
                pygame.draw.circle(screen, p[5], (int(p[0]), int(p[1])), 3)