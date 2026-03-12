import pygame
from config import WIDTH, HEIGHT
from src.game import Game

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Emoji Flip Master: OOP Edition")
    clock = pygame.time.Clock()
    game = Game(screen)
    
    running = True
    while running:
        running = game.run()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()