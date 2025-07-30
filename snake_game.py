import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 25)

def generate_food(snake_body):
    """
    Generates a new food position on the grid ensuring it does not overlap with the snake body.
    """
    while True:
        x = random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE + 1, BLOCK_SIZE)
        y = random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE + 1, BLOCK_SIZE)
        food = [x, y]
        if food not in snake_body:
            return food

def draw_snake(snake_body):
    """
    Draws the snake on the screen.
    """
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

def draw_food(food):
    """
    Draws the food on the screen.
    """
    pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))

def show_score(score):
    """
    Renders the current score on the screen.
    """
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, [0, 0])

def game_over_screen(score):
    """
    Displays a game over message and the final score.
    """
    screen.fill(BLACK)
    game_over_text = font.render("Game Over!", True, RED)
    score_text = font.render("Final Score: " + str(score), True, WHITE)
    screen.blit(game_over_text, [SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3])
    screen.blit(score_text, [SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2])
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

def main():
    # Initial snake configuration: head starting at center of screen, one segment
    snake_body = [[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]]
    # Initial movement direction: stationary at the start
    dx, dy = 0, 0
    # Generate first food item
    food = generate_food(snake_body)
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handling key events for direction changes
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, BLOCK_SIZE

        # Calculate new snake head position
        head = [snake_body[0][0] + dx, snake_body[0][1] + dy]
        snake_body.insert(0, head)

        # Check if snake has eaten the food
        if head == food:
            score += 1
            food = generate_food(snake_body)
        else:
            # Remove the tail segment if no food eaten
            snake_body.pop()

        # Collision detection with walls
        if (head[0] < 0 or head[0] >= SCREEN_WIDTH or
            head[1] < 0 or head[1] >= SCREEN_HEIGHT):
            running = False

        # Collision detection with itself
        if head in snake_body[1:]:
            running = False

        # Render game elements
        screen.fill(BLACK)
        draw_snake(snake_body)
        draw_food(food)
        show_score(score)
        pygame.display.update()

        clock.tick(FPS)

    # When game loop ends, show game over screen
    game_over_screen(score)

if __name__ == "__main__":
    main()
