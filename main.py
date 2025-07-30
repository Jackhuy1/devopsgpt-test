# File: game.py
import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # Update game logic here.
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        # Draw game elements here.
        pygame.display.flip()

# File: main.py
import pygame
from game import Game

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()