import pygame
import sys

class Scoreboard:
    def __init__(self):
        self.score = 0
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)

    def update_score(self):
        self.score += 10

    def draw(self, screen):
        score_surface = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Scoreboard Example")
    clock = pygame.time.Clock()
    scoreboard = Scoreboard()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    scoreboard.update_score()

        screen.fill((0, 0, 0))
        scoreboard.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()