import pygame
import random
from config import *
from src.entities.card import Card
from src.systems.ui import ParticleSystem

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
        
        # พื้นหลังขยับได้ (Background Effect)
        self.bg_circles = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(0.3, 1.2)] for _ in range(12)]

        # ระบบ Particle System
        self.particle_system = ParticleSystem()

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

    def draw_button(self, text, rect, color, mouse_pos):
        hover = rect.collidepoint(mouse_pos)
        display_rect = rect.inflate(10, 10) if hover else rect
        pygame.draw.rect(self.screen, color if hover else tuple(c*0.7 for c in color), display_rect, border_radius=20)
        txt = FONT_UI.render(text, True, BG_COLOR if hover else TEXT_WHITE)
        self.screen.blit(txt, (display_rect.centerx - txt.get_width()//2, display_rect.centery - txt.get_height()//2))
        return hover

    def run(self):
        mouse_pos = pygame.mouse.get_pos()
        self.draw_background() # วาดพื้นหลัง

        # ---------------- 1. จัดการการคลิกเมาส์ ----------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "START_MENU":
                    if pygame.Rect(200, 450, 200, 75).collidepoint(mouse_pos):
                        self.state = "LEVEL_SELECT"
                
                elif self.state == "LEVEL_SELECT":
                    for lv in range(1, 21):
                        row, col = (lv-1)//4, (lv-1)%4
                        rect = pygame.Rect(70 + col*120, 150 + row*100, 90, 70)
                        if rect.collidepoint(mouse_pos) and self.levels_status[lv]:
                            self.current_level = lv
                            self.setup_level(lv)
                            self.state = "PLAYING"

                elif self.state == "PLAYING" and len(self.selected) < 2 and mouse_pos[1] < 600:
                    idx = (mouse_pos[1]//150)*4 + (mouse_pos[0]//150)
                    if idx < 16 and self.cards[idx].state == 0:
                        self.cards[idx].state = 1
                        self.selected.append(self.cards[idx])
                        # ✨ เอาเอฟเฟกต์ตอนกดการ์ดออกแล้ว ตามที่ขอครับ ✨

                elif self.state == "WON" and pygame.Rect(200, 450, 200, 75).collidepoint(mouse_pos):
                    if self.current_level < 20:
                        self.current_level += 1
                        self.setup_level(self.current_level)
                        self.state = "PLAYING"
                    else: self.state = "START_MENU"

                elif self.state == "GAMEOVER":
                    if pygame.Rect(200, 450, 200, 75).collidepoint(mouse_pos):
                        self.setup_level(self.current_level)
                        self.state = "PLAYING"
                    elif pygame.Rect(200, 550, 200, 50).collidepoint(mouse_pos):
                        self.state = "LEVEL_SELECT"

        # ---------------- 2. วาดหน้าจอตามสถานะ ----------------
        if self.state == "START_MENU":
            title = FONT_TITLE.render("EMOJI MATCH", True, ACCENT)
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
            self.draw_button("START", pygame.Rect(200, 450, 200, 75), ACCENT, mouse_pos)

        elif self.state == "LEVEL_SELECT":
            label = FONT_UI.render("SELECT LEVEL (1-20)", True, TEXT_WHITE)
            self.screen.blit(label, (WIDTH//2 - label.get_width()//2, 70))
            for lv in range(1, 21):
                row, col = (lv-1)//4, (lv-1)%4
                rect = pygame.Rect(70 + col*120, 150 + row*100, 90, 70)
                color = ACCENT if self.levels_status[lv] else (50, 50, 60)
                self.draw_button(str(lv), rect, color, mouse_pos)

        elif self.state == "PLAYING":
            # วาดการ์ด
            for card in self.cards:
                card.update()
                card.draw(self.screen)

            # คำนวณเวลาที่เหลือ
            time_left = max(0, self.time_limit - (pygame.time.get_ticks() - self.start_ticks)//1000)

            # ✨ แก้อาการกะพริบ: โดยการสั่งวาด UI แถบด้านล่างก่อนที่จะหยุดรอ ✨
            pygame.draw.rect(self.screen, (20, 20, 35), (0, 600, 600, 150))
            ui_txt = FONT_UI.render(f"LV {self.current_level} | TIME: {time_left}s | MATCH: {self.matches}/8", True, TEXT_WHITE)
            self.screen.blit(ui_txt, (120, 660))

            # เช็กการจับคู่ไพ่
            if len(self.selected) == 2 and all(c.state == 2 for c in self.selected):
                pygame.display.flip() # วาดภาพทั้งหมดขึ้นจอก่อน
                pygame.time.wait(300) # หยุดรอ 300ms (คราวนี้ด้านล่างจะไม่กะพริบแหว่งๆ แล้ว)
                
                if self.selected[0].emoji == self.selected[1].emoji:
                    self.matches += 1
                    # ✨ มีเอฟเฟกต์เฉพาะตอนจับคู่สำเร็จ ✨
                    idx = self.cards.index(self.selected[1])
                    card_x = (idx % 4) * 150 + 75
                    card_y = (idx // 4) * 150 + 75
                    self.particle_system.create(card_x, card_y, SUCCESS, count=20)
                else:
                    self.selected[0].state = 3
                    self.selected[1].state = 3
                self.selected = []

            # เช็กแพ้ชนะ
            if time_left == 0: self.state = "GAMEOVER"
            if self.matches == 8:
                if self.current_level < 20: self.levels_status[self.current_level+1] = 1
                self.state = "WON"
                # เอฟเฟกต์ตอนชนะด่าน (พลุระเบิดตรงกลางจอ)
                self.particle_system.create(WIDTH//2, HEIGHT//2, SUCCESS, count=50)

        elif self.state == "WON":
            txt = FONT_TITLE.render("LEVEL CLEAR!", True, SUCCESS)
            self.screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 250))
            self.draw_button("NEXT", pygame.Rect(200, 450, 200, 75), SUCCESS, mouse_pos)

        elif self.state == "GAMEOVER":
            txt = FONT_TITLE.render("TIME UP!", True, FAIL)
            self.screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 250))
            self.draw_button("RETRY", pygame.Rect(200, 450, 200, 75), FAIL, mouse_pos)
            self.draw_button("MENU", pygame.Rect(200, 550, 200, 50), (100, 100, 100), mouse_pos)

        # อัปเดตและวาด Particle Effect ลงบนหน้าจอ
        self.particle_system.update_and_draw(self.screen)

        pygame.display.flip()
        return True