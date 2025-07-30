import pygame
import sys

class Snake:
    def __init__(self):
        self.size = 20
        self.direction = 'RIGHT'
        initial_x = 400
        initial_y = 300
        self.segments = [pygame.Rect(initial_x, initial_y, self.size, self.size)]
        self.speed = self.size

    def move(self):
        head = self.segments[0]
        new_head = head.copy()
        if self.direction == 'UP':
            new_head.y -= self.speed
        elif self.direction == 'DOWN':
            new_head.y += self.speed
        elif self.direction == 'LEFT':
            new_head.x -= self.speed
        elif self.direction == 'RIGHT':
            new_head.x += self.speed
        self.segments.insert(0, new_head)
        self.segments.pop()

    def grow(self):
        tail = self.segments[-1]
        new_segment = tail.copy()
        self.segments.append(new_segment)

    def check_collision(self):
        head = self.segments[0]
        if head.left < 0 or head.right > 800 or head.top < 0 or head.bottom > 600:
            return True
        for segment in self.segments[1:]:
            if head.colliderect(segment):
                return True
        return False

    def set_direction(self, new_direction):
        opposite_directions = {
            'UP': 'DOWN',
            'DOWN': 'UP',
            'LEFT': 'RIGHT',
            'RIGHT': 'LEFT'
        }
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    snake = Snake()
    running = True

    while running:
        clock.tick(10)  # Set game speed (frames per second)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.set_direction('UP')
                elif event.key == pygame.K_DOWN:
                    snake.set_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    snake.set_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction('RIGHT')

        snake.move()
        if snake.check_collision():
            running = False

        screen.fill((0, 0, 0))  # Clear screen with black
        for segment in snake.segments:
            pygame.draw.rect(screen, (255, 255, 255), segment)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()