import pygame
import random

# Initialize pygame
pygame.init()

# Game window dimensions
window_width = 800
window_height = 600
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Snake properties
snake_block = 10

# Clock for controlling game speed
clock = pygame.time.Clock()

# Font for displaying score
font_style = pygame.font.SysFont("bahnschrift", 25)

# Function to display the score
def display_score(score):
    value = font_style.render("Your Score: " + str(score), True, white)
    game_window.blit(value, [0, 0])

# Function to handle input
def handle_input(event, x1_change, y1_change, snake_block):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT and x1_change == 0:
            x1_change = -snake_block
            y1_change = 0
        elif event.key == pygame.K_RIGHT and x1_change == 0:
            x1_change = snake_block
            y1_change = 0
        elif event.key == pygame.K_UP and y1_change == 0:
            y1_change = -snake_block
            x1_change = 0
        elif event.key == pygame.K_DOWN and y1_change == 0:
            y1_change = snake_block
            x1_change = 0
    return x1_change, y1_change

# Function to generate food
def generate_food(snake_list, window_width, window_height, snake_block):
    while True:
        foodx = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0
        if [foodx, foody] not in snake_list:
            return foodx, foody

# Function to handle game over
def handle_game_over():
    game_window.fill(black)
    message = font_style.render("Game Over! Press Q-Quit or C-Play Again", True, red)
    game_window.blit(message, [window_width / 6, window_height / 3])
    pygame.display.update()

# Main game loop
def game_loop():
    game_over = False
    game_close = False

    # Initial position of the snake
    x1 = window_width / 2
    y1 = window_height / 2

    # Change in position
    x1_change = 0
    y1_change = 0

    # Snake body
    snake_list = []
    length_of_snake = 1

    # Food position
    foodx, foody = generate_food(snake_list, window_width, window_height, snake_block)

    while not game_over:
        while game_close:
            handle_game_over()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        return  # Exit the current game loop to restart the game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            x1_change, y1_change = handle_input(event, x1_change, y1_change, snake_block)

        if x1 >= window_width or x1 < 0 or y1 >= window_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        game_window.fill(black)
        pygame.draw.rect(game_window, green, [foodx, foody, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        for block in snake_list:
            pygame.draw.rect(game_window, white, [block[0], block[1], snake_block, snake_block])

        display_score(length_of_snake - 1)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food(snake_list, window_width, window_height, snake_block)
            length_of_snake += 1

        # Dynamically adjust snake speed based on score
        snake_speed = 15 + (length_of_snake // 5)
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game
while True:
    game_loop()
