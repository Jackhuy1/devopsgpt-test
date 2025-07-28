import React from 'react';
import PropTypes from 'prop-types';
import './gameboard.css';

function GameBoard({ snake, food, boardSize }) {
  // Convert snake array to a Set for O(1) lookup
  const snakeSet = React.useMemo(() => {
    const set = new Set();
    snake.forEach(([row, col]) => set.add(`${row}-${col}`));
    return set;
  }, [snake]);

  const cells = [];
  for (let row = 0; row < boardSize; row++) {
    for (let col = 0; col < boardSize; col++) {
      let className = 'cell';
      if (snakeSet.has(`${row}-${col}`)) {
        className = 'cell snake';
      } else if (food[0] === row && food[1] === col) {
        className = 'cell food';
      }
      cells.push(<div key={`${row}-${col}`} className={className} />);
    }
  }

  return (
    <div
      className="game-board"
      style={{
        gridTemplateRows: `repeat(${boardSize}, 1fr)`,
        gridTemplateColumns: `repeat(${boardSize}, 1fr)`,
      }}
    >
      {cells}
    </div>
  );
}

GameBoard.propTypes = {
  snake: PropTypes.arrayOf(
    PropTypes.arrayOf(PropTypes.number.isRequired).isRequired
  ).isRequired,
  food: PropTypes.arrayOf(PropTypes.number.isRequired).isRequired,
  boardSize: PropTypes.number.isRequired,
};

export default GameBoard;
