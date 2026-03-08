import pygame
import random
import math


pygame.init()
WIDTH, HEIGHT = 600, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Emoji Flip Master: 20 Levels Challenge")

BG_COLOR = (15, 15, 25)
CARD_BACK = (40, 44, 52)
CARD_FRONT = (255, 255, 255)
ACCENT = (0, 210, 255)
SUCCESS = (0, 255, 127)
FAIL = (255, 65, 54)
TEXT_WHITE = (240, 240, 240)

font_emoji = pygame.font.SysFont("segoe ui symbol", 60)
font_title = pygame.font.SysFont("tahoma", 65, bold=True)
font_ui = pygame.font.SysFont("tahoma", 24, bold=True)
font_small = pygame.font.SysFont("tahoma", 18, bold=True)


levels_status = {i: (1 if i == 1 else 0) for i in range(1, 21)}
EMOJIS_POOL = ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔"]

def setup_game_data(level):
    selected_emojis = random.sample(EMOJIS_POOL, 8)
    items = selected_emojis * 2
    random.shuffle(items)
    
    card_states = [0] * 16 
    flip_frames = [0] * 16
    
    
    time_limit = max(8, 45 - (level * 2)) 
    
    return items, card_states, flip_frames, time_limit, pygame.time.get_ticks()

particles = []
def create_particles(x, y, color, count=15):
    for _ in range(count):
        particles.append([x, y, random.uniform(-4, 4), random.uniform(-4, 4), 30, color])

game_state = "START_MENU"
current_level = 1
selected = []
matches = 0
bg_circles = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(0.3, 1.2)] for _ in range(12)]


def draw_button(text, rect, color, hover=False):
    display_rect = rect.inflate(10, 10) if hover else rect
    pygame.draw.rect(screen, color if hover else tuple(c*0.7 for c in color), display_rect, border_radius=20)
    txt = font_ui.render(text, True, BG_COLOR if hover else TEXT_WHITE)
    screen.blit(txt, (display_rect.centerx - txt.get_width()//2, display_rect.centery - txt.get_height()//2))


running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BG_COLOR)
    mouse_pos = pygame.mouse.get_pos()
    
    for c in bg_circles:
        c[1] -= c[2]
        if c[1] < -50: c[1] = HEIGHT + 50; c[0] = random.randint(0, WIDTH)
        pygame.draw.circle(screen, (25, 30, 45), (int(c[0]), int(c[1])), 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "START_MENU":
                btn_start = pygame.Rect(200, 450, 200, 75)
                if btn_start.collidepoint(mouse_pos): game_state = "LEVEL_SELECT"
            
            elif game_state == "LEVEL_SELECT":
                for lv in range(1, 21):
                    row, col = (lv-1)//4, (lv-1)%4
                    bx, by = 70 + col*120, 150 + row*100
                    if pygame.Rect(bx, by, 90, 70).collidepoint(mouse_pos) and levels_status[lv]:
                        current_level = lv
                        game_items, card_states, flip_frames, time_limit, start_ticks = setup_game_data(lv)
                        matches = 0; selected = []; game_state = "PLAYING"

            elif game_state == "PLAYING" and len(selected) < 2 and mouse_pos[1] < 600:
                idx = (mouse_pos[1]//150)*4 + (mouse_pos[0]//150)
                if card_states[idx] == 0:
                    card_states[idx] = 1
                    selected.append(idx)
            
            elif game_state == "WON":
                btn_next = pygame.Rect(200, 450, 200, 75)
                if btn_next.collidepoint(mouse_pos):
                    if current_level < 20:
                        current_level += 1
                        game_items, card_states, flip_frames, time_limit, start_ticks = setup_game_data(current_level)
                        matches = 0; selected = []; game_state = "PLAYING"
                    else: game_state = "START_MENU"

            elif game_state == "GAMEOVER":
                btn_retry = pygame.Rect(200, 450, 200, 75)
                if btn_retry.collidepoint(mouse_pos):
                    game_items, card_states, flip_frames, time_limit, start_ticks = setup_game_data(current_level)
                    matches = 0; selected = []; game_state = "PLAYING"
                elif pygame.Rect(200, 550, 200, 50).collidepoint(mouse_pos):
                    game_state = "LEVEL_SELECT"

  
    if game_state == "START_MENU":
        title = font_title.render("EMOJI MATCH", True, ACCENT)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
        draw_button("START", pygame.Rect(200, 450, 200, 75), ACCENT, pygame.Rect(200, 450, 200, 75).collidepoint(mouse_pos))

    elif game_state == "LEVEL_SELECT":
        label = font_ui.render("SELECT LEVEL (1-20)", True, TEXT_WHITE)
        screen.blit(label, (WIDTH//2 - label.get_width()//2, 70))
        for lv in range(1, 21):
            row, col = (lv-1)//4, (lv-1)%4
            rect = pygame.Rect(70 + col*120, 150 + row*100, 90, 70)
            color = ACCENT if levels_status[lv] else (50, 50, 60)
            draw_button(str(lv), rect, color, rect.collidepoint(mouse_pos) and levels_status[lv])

    elif game_state == "PLAYING":
        for i in range(16):
            if card_states[i] == 1:
                flip_frames[i] += 15
                if flip_frames[i] >= 180: flip_frames[i] = 180; card_states[i] = 2
            elif card_states[i] == 3:
                flip_frames[i] -= 15
                if flip_frames[i] <= 0: flip_frames[i] = 0; card_states[i] = 0

        for i in range(16):
            r, c = i // 4, i % 4
            angle = math.radians(flip_frames[i])
            width = 130 * abs(math.cos(angle))
            rect = pygame.Rect(c*150 + 10 + (130-width)/2, r*150 + 10, width, 130)
            if flip_frames[i] < 90:
                pygame.draw.rect(screen, CARD_BACK, rect, border_radius=15)
                pygame.draw.rect(screen, ACCENT, rect, 2, border_radius=15)
            else:
                pygame.draw.rect(screen, CARD_FRONT, rect, border_radius=15)
                if width > 20:
                    e_surf = font_emoji.render(game_items[i], True, (0,0,0))
                    e_scaled = pygame.transform.scale(e_surf, (int(width*0.7), 80))
                    screen.blit(e_scaled, (rect.centerx - e_scaled.get_width()//2, rect.centery - 40))

        if len(selected) == 2 and all(card_states[i] == 2 for i in selected):
            pygame.display.flip()
            pygame.time.wait(300)
            if game_items[selected[0]] == game_items[selected[1]]:
                matches += 1
                create_particles((selected[1]%4)*150 + 75, (selected[1]//4)*150 + 75, SUCCESS)
            else:
                card_states[selected[0]] = 3; card_states[selected[1]] = 3
            selected = []

        time_left = max(0, time_limit - (pygame.time.get_ticks() - start_ticks)//1000)
        if time_left == 0: game_state = "GAMEOVER"
        if matches == 8:
            if current_level < 20: levels_status[current_level+1] = 1
            game_state = "WON"; create_particles(WIDTH//2, HEIGHT//2, SUCCESS, 50)

        pygame.draw.rect(screen, (20, 20, 35), (0, 600, 600, 150))
        screen.blit(font_ui.render(f"LV {current_level} | TIME: {time_left}s | MATCH: {matches}/8", True, TEXT_WHITE), (120, 660))

    elif game_state == "WON":
        txt = font_title.render("LEVEL CLEAR!", True, SUCCESS)
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 250))
        btn_next = pygame.Rect(200, 450, 200, 75)
        draw_button("NEXT", btn_next, SUCCESS, btn_next.collidepoint(mouse_pos))

    elif game_state == "GAMEOVER":
        txt = font_title.render("TIME UP!", True, FAIL)
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 250))
        btn_retry = pygame.Rect(200, 450, 200, 75)
        draw_button("RETRY", btn_retry, FAIL, btn_retry.collidepoint(mouse_pos))
        btn_menu = pygame.Rect(200, 550, 200, 50)
        draw_button("MENU", btn_menu, (100, 100, 100), btn_menu.collidepoint(mouse_pos))

    for p in particles[:]:
        p[0] += p[2]; p[1] += p[3]; p[4] -= 1
        if p[4] <= 0: particles.remove(p)
        else: pygame.draw.circle(screen, p[5], (int(p[0]), int(p[1])), 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()