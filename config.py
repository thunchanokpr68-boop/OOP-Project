import pygame

# ต้อง init เพื่อให้โหลด Font ได้ตั้งแต่แรก
pygame.init()

WIDTH, HEIGHT = 600, 750

BG_COLOR = (15, 15, 25)
CARD_BACK = (40, 44, 52)
CARD_FRONT = (255, 255, 255)
ACCENT = (0, 210, 255)
SUCCESS = (0, 255, 127)
FAIL = (255, 65, 54)
TEXT_WHITE = (240, 240, 240)

# กำหนด Font
FONT_EMOJI = pygame.font.SysFont("segoe ui symbol", 60)
FONT_TITLE = pygame.font.SysFont("tahoma", 65, bold=True)
FONT_UI = pygame.font.SysFont("tahoma", 24, bold=True)
FONT_SMALL = pygame.font.SysFont("tahoma", 18, bold=True)

# ข้อมูลเกม
EMOJIS_POOL = ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔"]