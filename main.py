import pygame
from config import WIDTH, HEIGHT
from src.game import Game

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Emoji Flip Master: 20 Levels Challenge")
    clock = pygame.time.Clock()
    
    # โหลดคลาส Game หลักมาใช้
    game = Game(screen)
    
    running = True
    while running:
        # สั่งรันลูปเกมจาก Game Class
        running = game.run()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()