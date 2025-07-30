#!/usr/bin/env python3
import random

def generate_food(snake_body, width=600, height=400, grid_size=20):
    """
    Generate a random food position that is not on the snake's body.
    The game area is defined by width and height and is divided into a grid of cells of size grid_size.
    """
    while True:
        x = random.randrange(0, width, grid_size)
        y = random.randrange(0, height, grid_size)
        food = [x, y]
        if food not in snake_body:
            return food

def test_generate_food_not_on_snake():
    # Define a snake body that occupies some parts of the grid.
    snake_body = [[100, 100], [120, 100], [140, 100]]
    # Generate food several times to ensure it doesn't fall on the snake body.
    for _ in range(10):
        food = generate_food(snake_body)
        assert food not in snake_body, f"Food {food} is on the snake's body!"

if __name__ == "__main__":
    import pytest
    pytest.main()