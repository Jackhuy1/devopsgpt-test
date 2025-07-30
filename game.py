import pygame
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SEGMENT_SIZE = 20

# Snake class
class Snake:
    def __init__(self):
        self.size = SEGMENT_SIZE
        # Start with one segment located at the center of the screen.
        self.segments = [pygame.Rect(100, 100, self.size, self.size)]
        self.direction = "RIGHT"
        self.opposite_direction = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }

    def set_direction(self, new_direction):
        # Prevent the snake from reversing onto itself.
        if new_direction != self.opposite_direction.get(self.direction, ""):
            self.direction = new_direction

    def move(self):
        # Calculate new head position based on current direction.
        head = self.segments[0].copy()
        if self.direction == "UP":
            head.y -= self.size
        elif self.direction == "DOWN":
            head.y += self.size
        elif self.direction == "LEFT":
            head.x -= self.size
        elif self.direction == "RIGHT":
            head.x += self.size

        # Insert new head segment.
        self.segments.insert(0, head)
        # Remove the tail segment.
        self.segments.pop()

    def grow(self):
        # When growing, add a new segment at the same position as the tail.
        tail = self.segments[-1].copy()
        self.segments.append(tail)

    def check_collision(self):
        head = self.segments[0]
        # Check collision with boundaries.
        if head.left < 0 or head.right > SCREEN_WIDTH or head.top < 0 or head.bottom > SCREEN_HEIGHT:
            return True
        # Check collision with itself.
        for segment in self.segments[1:]:
            if head.colliderect(segment):
                return True
        return False

# Food class
class Food:
    def __init__(self):
        self.size = SEGMENT_SIZE
        self.position = pygame.Rect(0, 0, self.size, self.size)
        self.reposition([])

    def reposition(self, snake_segments):
        # Generate a new food position that does not collide with the snake.
        valid_position = False
        while not valid_position:
            x = random.randint(0, (SCREEN_WIDTH - self.size) // self.size) * self.size
            y = random.randint(0, (SCREEN_HEIGHT - self.size) // self.size) * self.size
            new_rect = pygame.Rect(x, y, self.size, self.size)
            valid_position = True
            for segment in snake_segments:
                if new_rect.colliderect(segment):
                    valid_position = False
                    break
        self.position = new_rect

# Scoreboard class
class Scoreboard:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 24)
        self.text_color = (255, 255, 255)

    def update_score(self):
        # Increase score by 10 for every food eaten.
        self.score += 10

    def draw(self, screen):
        score_surface = self.font.render("Score: " + str(self.score), True, self.text_color)
        screen.blit(score_surface, (10, 10))

# Game class
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.snake = Snake()
        self.food = Food()
        self.food.reposition(self.snake.segments)
        self.scoreboard = Scoreboard()
        self.speed = 10  # Starting FPS
        self.difficulty_level = 0

    def run(self):
        while self.running:
            self.handle_events()
            self.update_game_state()
            self.render()
            self.clock.tick(self.speed)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.set_direction('UP')
                elif event.key == pygame.K_DOWN:
                    self.snake.set_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    self.snake.set_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    self.snake.set_direction('RIGHT')

    def update_game_state(self):
        self.snake.move()

        if self.snake.check_collision():
            self.running = False

        # Check for collision between snake head and food.
        if self.snake.segments[0].colliderect(self.food.position):
            self.snake.grow()
            self.scoreboard.update_score()
            self.food.reposition(self.snake.segments)
            self.increase_difficulty()

    def render(self):
        self.screen.fill((0, 0, 0))
        
        # Draw the snake.
        for segment in self.snake.segments:
            pygame.draw.rect(self.screen, (0, 255, 0), segment)
        
        # Draw the food.
        pygame.draw.rect(self.screen, (255, 0, 0), self.food.position)
        
        # Draw the scoreboard.
        self.scoreboard.draw(self.screen)
        
        pygame.display.flip()

    def increase_difficulty(self):
        # Increase FPS for every 50 points achieved.
        milestone = self.scoreboard.score // 50
        if milestone > self.difficulty_level:
            self.difficulty_level = milestone
            self.speed += 1

if __name__ == "__main__":
    game = Game()
    game.run()