# main.py
from flask import Flask
from snake_game import SnakeGame

app = Flask(__name__)

@app.route("/")
def home():
    # Render the homepage with navigation and game start option
    return (
        "<h1>Welcome to the Integrated Snake Game and Website!</h1>"
        "<p>Visit <a href='/game'>/game</a> to play the Snake game simulation.</p>"
    )

@app.route("/game")
def game():
    # Initialize the Snake game, run the simulation and return the final score
    game_instance = SnakeGame()
    final_score = game_instance.run()
    return f"<h2>Snake Game Finished!</h2><p>Your final score is: {final_score}</p>"

if __name__ == "__main__":
    # Run the Flask application on host 0.0.0.0 and port 5000
    app.run(host="0.0.0.0", port=5000)

# snake_game.py
import time
import random

class SnakeGame:
    def __init__(self):
        self.score = 0
        self.is_running = True

    def run(self):
        """
        Simulate a snake game. This function runs a simple game loop simulation,
        incrementing the score over a random number of iterations.
        """
        # Determine a random number of game iterations between 5 and 10.
        iterations = random.randint(5, 10)
        for _ in range(iterations):
            # Simulate processing time for each game iteration.
            time.sleep(0.2)
            # Increase score by a random value between 1 and 10.
            self.score += random.randint(1, 10)
        self.is_running = False
        return self.score
