#!/usr/bin/env python3
import pygame
import random
import sys

# Window settings
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
CELL_SIZE = 20

# Colors (RGB tuples)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Gameplay options
WRAP_AROUND = False  # Set to True for snake to wrap around the screen

class Snake:
    def __init__(self):
        # Starting position in the middle
        self.head_x = WINDOW_WIDTH // 2
        self.head_y = WINDOW_HEIGHT // 2
        # The snake body starts with a single segment (the head)
        self.body = [(self.head_x, self.head_y)]
        # Initial direction: moving to the right
        self.direction = "RIGHT"

    def move(self):
        # Determine new head position based on the current direction
        if self.direction == "UP":
            self.head_y -= CELL_SIZE
        elif self.direction == "DOWN":
            self.head_y += CELL_SIZE
        elif self.direction == "LEFT":
            self.head_x -= CELL_SIZE
        elif self.direction == "RIGHT":
            self.head_x += CELL_SIZE

        # If wrap-around is enabled, wrap the snake's head position around the window
        if WRAP_AROUND:
            self.head_x %= WINDOW_WIDTH
            self.head_y %= WINDOW_HEIGHT

        # Insert new head position at the beginning of the body list
        self.body.insert(0, (self.head_x, self.head_y))
        # Remove the last segment to simulate movement
        self.body.pop()

    def grow(self):
        # When growing, simply add a new segment at the tail (duplicate of last segment)
        self.body.append(self.body[-1])

    def check_collision(self):
        # If wrap-around is disabled, check if snake head collides with the window boundaries
        if not WRAP_AROUND:
            if (self.head_x < 0 or self.head_x >= WINDOW_WIDTH or
                self.head_y < 0 or self.head_y >= WINDOW_HEIGHT):
                return True
        # Check if the snake head collides with its body (excluding the head itself)
        if (self.head_x, self.head_y) in self.body[1:]:
            return True
        return False

class Food:
    def __init__(self):
        # Spawn food immediately on instantiation
        self.x = 0
        self.y = 0
        self.spawn([])

    def spawn(self, snake_body):
        # Generate random positions ensuring food does not collide with the snake body
        while True:
            self.x = random.randint(0, (WINDOW_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            self.y = random.randint(0, (WINDOW_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            if (self.x, self.y) not in snake_body:
                break

def main():
    pygame.init()
    pygame.display.set_caption("Snake Game")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                # Prevent the snake from reversing
                if event.key == pygame.K_UP and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif event.key == pygame.K_DOWN and snake.direction != "UP":
                    snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                    snake.direction = "RIGHT"

        snake.move()

        # Check collision with food: if snake head is at the same position as food
        if snake.body[0] == (food.x, food.y):
            snake.grow()
            food.spawn(snake.body)

        # Check for collisions with boundaries or itself
        if snake.check_collision():
            running = False

        # Draw everything
        screen.fill(BLACK)
        # Draw snake segments
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
        # Draw food
        pygame.draw.rect(screen, RED, (food.x, food.y, CELL_SIZE, CELL_SIZE))

        pygame.display.update()
        # Increase game speed gradually based on snake length for increasing difficulty
        game_speed = 10 + (len(snake.body) - 1) // 5
        clock.tick(game_speed)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()