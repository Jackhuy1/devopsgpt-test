import pygame
import random

class Food:
    def __init__(self):
        self.size = 20
        self.position = pygame.Rect(0, 0, self.size, self.size)

    def reposition(self, snake_segments):
        grid_width = 800 // self.size
        grid_height = 600 // self.size
        valid = False
        while not valid:
            x = random.randint(0, grid_width - 1) * self.size
            y = random.randint(0, grid_height - 1) * self.size
            new_rect = pygame.Rect(x, y, self.size, self.size)
            valid = not any(new_rect.colliderect(segment) for segment in snake_segments)
        self.position = new_rect

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Food Placement Demo")
    clock = pygame.time.Clock()

    # Initialize food and snake segments for demonstration.
    food = Food()
    snake_segments = [
        pygame.Rect(100, 100, 20, 20),
        pygame.Rect(120, 100, 20, 20),
        pygame.Rect(140, 100, 20, 20)
    ]
    food.reposition(snake_segments)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Reposition the food when spacebar is pressed (for testing purposes).
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    food.reposition(snake_segments)

        screen.fill((0, 0, 0))
        # Draw the food in red.
        pygame.draw.rect(screen, (255, 0, 0), food.position)
        # Draw the snake segments in green.
        for segment in snake_segments:
            pygame.draw.rect(screen, (0, 255, 0), segment)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()