import React, { useState, useEffect, useRef } from 'react';
import GameBoard from './GameBoard';
import Score from './Score';

const BOARD_SIZE = 20;
const INITIAL_SNAKE = [[10, 10], [10, 9], [10, 8]];

const getRandomFoodPosition = (snake) => {
  let newFood;
  while (true) {
    newFood = [
      Math.floor(Math.random() * BOARD_SIZE),
      Math.floor(Math.random() * BOARD_SIZE),
    ];
    // Ensure food does not spawn on the snake
    if (!snake.some(segment => segment[0] === newFood[0] && segment[1] === newFood[1])) {
      break;
    }
  }
  return newFood;
};

const DIRECTIONS = {
  ArrowUp: [-1, 0],
  ArrowDown: [1, 0],
  ArrowLeft: [0, -1],
  ArrowRight: [0, 1],
};

function App() {
  const [snake, setSnake] = useState(INITIAL_SNAKE);
  const [food, setFood] = useState(getRandomFoodPosition(INITIAL_SNAKE));
  const [direction, setDirection] = useState('ArrowRight');
  const [score, setScore] = useState(0);
  const [speed, setSpeed] = useState(200);
  const [gameOver, setGameOver] = useState(false);

  const directionRef = useRef(direction);
  directionRef.current = direction;

  // Handle keyboard input for direction change
  useEffect(() => {
    const handleKeyDown = (e) => {
      const newDirection = e.key;
      if (Object.keys(DIRECTIONS).includes(newDirection)) {
        // Prevent snake from reversing
        const [dx, dy] = DIRECTIONS[newDirection];
        const [cdx, cdy] = DIRECTIONS[directionRef.current];
        if (dx + cdx !== 0 || dy + cdy !== 0) {
          setDirection(newDirection);
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Game loop
  useEffect(() => {
    if (gameOver) return;

    const interval = setInterval(() => {
      setSnake(prevSnake => {
        const head = prevSnake[0];
        const [dx, dy] = DIRECTIONS[directionRef.current];
        const newHead = [head[0] + dx, head[1] + dy];

        // Check wall collision
        if (
          newHead[0] < 0 ||
          newHead[0] >= BOARD_SIZE ||
          newHead[1] < 0 ||
          newHead[1] >= BOARD_SIZE
        ) {
          setGameOver(true);
          return prevSnake;
        }

        // Check self collision
        if (prevSnake.some(segment => segment[0] === newHead[0] && segment[1] === newHead[1])) {
          setGameOver(true);
          return prevSnake;
        }

        let newSnake;
        // Check if food eaten
        if (newHead[0] === food[0] && newHead[1] === food[1]) {
          newSnake = [newHead, ...prevSnake];
          setScore(prevScore => prevScore + 1);
          setFood(getRandomFoodPosition(newSnake));
        } else {
          newSnake = [newHead, ...prevSnake.slice(0, -1)];
        }
        return newSnake;
      });
    }, speed);

    return () => clearInterval(interval);
  }, [food, speed, gameOver]);

  // Speed update on score change
  useEffect(() => {
    if (score > 0 && score % 5 === 0) {
      setSpeed(prevSpeed => (prevSpeed > 50 ? prevSpeed - 20 : prevSpeed));
    }
  }, [score]);

  const restartGame = () => {
    setSnake(INITIAL_SNAKE);
    setFood(getRandomFoodPosition(INITIAL_SNAKE));
    setDirection('ArrowRight');
    setScore(0);
    setSpeed(200);
    setGameOver(false);
  };

  return (
    <div style={{ textAlign: 'center', userSelect: 'none' }}>
      <h1>Snake Game</h1>
      <Score score={score} />
      <GameBoard snake={snake} food={food} boardSize={BOARD_SIZE} />
      {gameOver && (
        <div>
          <h2>Game Over!</h2>
          <button onClick={restartGame} style={{ fontSize: '16px', padding: '10px 20px', cursor: 'pointer' }}>
            Restart
          </button>
        </div>
      )}
      <p style={{ marginTop: '20px', fontSize: '14px', color: '#555' }}>
        Use arrow keys to control the snake.
      </p>
    </div>
  );
}

export default App;
