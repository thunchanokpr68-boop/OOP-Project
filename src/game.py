import pygame
import random
from config import *
from src.systems.ui import Button, ParticleSystem
from src.entities.card import Card

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = "START_MENU"
        self.current_level = 1
        self.levels_status = {i: (1 if i == 1 else 0) for i in range(1, 21)}
        
        self.cards = []
        self.selected = []
        self.matches = 0
        self.time_limit = 0
        self.start_ticks = 0
        
        self.particles = ParticleSystem()
        self.bg_circles = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(0.3, 1.2)] for _ in range(12)]

    def setup_level(self, level):
        selected_emojis = random.sample(EMOJIS_POOL, 8)
        items = selected_emojis * 2
        random.shuffle(items)
        
        self.cards = [Card(i, items[i], i // 4, i % 4) for i in range(16)]
        self.time_limit = max(8, 45 - (level * 2))
        self.start_ticks = pygame.time.get_ticks()
        self.matches = 0
        self.selected = []

    def draw_background(self):
        self.screen.fill(BG_COLOR)
        for c in self.bg_circles:
            c[1] -= c[2]
            if c[1] < -50: 
                c[1] = HEIGHT + 50
                c[0] = random.randint(0, WIDTH)
            pygame.draw.circle(self.screen, (25, 30, 45), (int(c[0]), int(c[1])), 50)

    def run(self):
        mouse_pos = pygame.mouse.get_pos()
        self.draw_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "START_MENU":
                    btn_start = Button("START", (200, 450, 200, 75), ACCENT)
                    if btn_start.is_clicked(mouse_pos, event):
                        self.state = "LEVEL_SELECT"
                
                elif self.state == "LEVEL_SELECT":
                    for lv in range(1, 21):
                        row, col = (lv-1)//4, (lv-1)%4
                        bx, by = 70 + col*120, 150 + row*100
                        btn = Button(str(lv), (bx, by, 90, 70), ACCENT)
                        if btn.is_clicked(mouse_pos, event) and self.levels_status[lv]:
                            self.current_level = lv
                            self.setup_level(lv)
                            self.state = "PLAYING"

                elif self.state == "PLAYING" and len(self.selected) < 2 and mouse_pos[1] < 600:
                    idx = (mouse_pos[1]//150)*4 + (mouse_pos[0]//150)
                    if self.cards[idx].state == 0:
                        self.cards[idx].state = 1
                        self.selected.append(self.cards[idx])
                
                elif self.state == "WON":
                    btn_next = Button("NEXT", (200, 450, 200, 75), SUCCESS)
                    if btn_next.is_clicked(mouse_pos, event):
                        if self.current_level < 20:
                            self.current_level += 1
                            self.setup_level(self.current_level)
                            self.state = "PLAYING"
                        else:
                            self.state = "START_MENU"

                elif self.state == "GAMEOVER":
                    btn_retry = Button("RETRY", (200, 450, 200, 75), FAIL)
                    btn_menu = Button("MENU", (200, 550, 200, 50), (100, 100, 100))
                    if btn_retry.is_clicked(mouse_pos, event):
                        self.setup_level(self.current_level)
                        self.state = "PLAYING"
                    elif btn_menu.is_clicked(mouse_pos, event):
                        self.state = "LEVEL_SELECT"

        # โค้ดส่วนวาดหน้าจอ (Rendering) ตาม Game State
        if self.state == "START_MENU":
            title = FONT_TITLE.render("EMOJI MATCH", True, ACCENT)
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
            Button("START", (200, 450, 200, 75), ACCENT).draw(self.screen, mouse_pos)

        elif self.state == "LEVEL_SELECT":
            label = FONT_UI.render("SELECT LEVEL (1-20)", True, TEXT_WHITE)
            self.screen.blit(label, (WIDTH//2 - label.get_width()//2, 70))
            for lv in range(1, 21):
                row, col = (lv-1)//4, (lv-1)%4
                rect = (70 + col*120, 150 + row*100, 90, 70)
                color = ACCENT if self.levels_status[lv] else (50, 50, 60)
                Button(str(lv), rect, color).draw(self.screen, mouse_pos)

        elif self.state == "PLAYING":
            for card in self.cards:
                card.update()
                card.draw(self.screen)

            if len(self.selected) == 2 and all(c.state == 2 for c in self.selected):
                pygame.display.flip()
                pygame.time.wait(300)
                if self.selected[0].emoji == self.selected[1].emoji:
                    self.matches += 1
                    self.particles.create(self.selected[1].rect.centerx, self.selected[1].rect.centery, SUCCESS)
                else:
                    self.selected[0].state = 3
                    self.selected[1].state = 3
                self.selected = []

            time_left = max(0, self.time_limit - (pygame.time.get_ticks() - self.start_ticks)//1000)
            if time_left == 0: 
                self.state = "GAMEOVER"
            
            if self.matches == 8:
                if self.current_level < 20: 
                    self.levels_status[self.current_level+1] = 1
                self.state = "WON"
                self.particles.create(WIDTH//2, HEIGHT//2, SUCCESS, 50)

            pygame.draw.rect(self.screen, (20, 20, 35), (0, 600, 600, 150))
            ui_text = FONT_UI.render(f"LV {self.current_level} | TIME: {time_left}s | MATCH: {self.matches}/8", True, TEXT_WHITE)
            self.screen.blit(ui_text, (120, 660))

        elif self.state == "WON":
            txt = FONT_TITLE.render("LEVEL CLEAR!", True, SUCCESS)
            self.screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 250))
            Button("NEXT", (200, 450, 200, 75), SUCCESS).draw(self.screen, mouse_pos)

        elif self.state == "GAMEOVER":
            txt = FONT_TITLE.render("TIME UP!", True, FAIL)
            self.screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 250))
            Button("RETRY", (200, 450, 200, 75), FAIL).draw(self.screen, mouse_pos)
            Button("MENU", (200, 550, 200, 50), (100, 100, 100)).draw(self.screen, mouse_pos)

        self.particles.update_and_draw(self.screen)
        pygame.display.flip()
        
        return True