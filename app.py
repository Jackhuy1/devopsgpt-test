from flask import Flask, render_template, request, jsonify, session, abort
from flask_cors import CORS
from functools import wraps
import threading
import uuid

# --- SnakeGame Implementation ---
# Minimal, fully functional SnakeGame class for demonstration.
# In production, replace with your actual game logic.

import random

class SnakeGame:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.direction = 'RIGHT'
        self.snake = [(self.width // 2, self.height // 2)]
        self.spawn_food()
        self.score = 0
        self.game_over = False

    def spawn_food(self):
        while True:
            food = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if food not in self.snake:
                self.food = food
                break

    def change_direction(self, direction):
        # Only allow valid direction changes (no direct reversal)
        valid_directions = {'UP', 'DOWN', 'LEFT', 'RIGHT'}
        opposite = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if direction in valid_directions and direction != opposite[self.direction]:
            self.direction = direction

    def update(self):
        if self.game_over:
            return
        head_x, head_y = self.snake[0]
        move = {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0)
        }[self.direction]
        new_head = (head_x + move[0], head_y + move[1])

        # Check for collisions
        if (
            new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height or
            new_head in self.snake
        ):
            self.game_over = True
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()

    def get_state(self):
        return {
            'snake': self.snake,
            'food': self.food,
            'score': self.score,
            'game_over': self.game_over,
            'direction': self.direction,
            'width': self.width,
            'height': self.height
        }

# --- End SnakeGame Implementation ---

app = Flask(__name__)
app.secret_key = 'replace-this-with-a-secure-random-secret-key'
CORS(app, supports_credentials=True)

# Thread-safe per-session game storage
games = {}
games_lock = threading.Lock()

def get_user_id():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return session['user_id']

def get_game():
    user_id = get_user_id()
    with games_lock:
        if user_id not in games:
            games[user_id] = SnakeGame()
        return games[user_id]

def require_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            abort(400, description="Request must be JSON")
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/state', methods=['GET'])
def get_state():
    game = get_game()
    return jsonify(game.get_state())

@app.route('/move', methods=['POST'])
@require_json
def move():
    data = request.get_json()
    direction = data.get('direction')
    valid_directions = {'UP', 'DOWN', 'LEFT', 'RIGHT'}
    if not direction or direction not in valid_directions:
        return jsonify({'error': 'Invalid direction'}), 400
    game = get_game()
    game.change_direction(direction)
    game.update()
    return jsonify(game.get_state())

@app.route('/reset', methods=['POST'])
def reset():
    game = get_game()
    game.reset()
    return jsonify(game.get_state())

@app.route('/healthz')
def healthz():
    return 'ok', 200

# Optional: Clean up old games (not strictly necessary for demo)
import time

GAME_TTL = 60 * 60  # 1 hour

class GameEntry:
    def __init__(self, game):
        self.game = game
        self.last_access = time.time()

def get_game():
    user_id = get_user_id()
    now = time.time()
    with games_lock:
        # Clean up old games
        to_delete = [uid for uid, entry in games.items() if now - entry.last_access > GAME_TTL]
        for uid in to_delete:
            del games[uid]
        if user_id not in games:
            games[user_id] = GameEntry(SnakeGame())
        games[user_id].last_access = now
        return games[user_id].game

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
