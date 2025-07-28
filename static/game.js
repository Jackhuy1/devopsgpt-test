let direction = 'RIGHT';
let lastDirection = 'RIGHT';
let gameOver = false;
let gridSize = 20;
let cellSize = 20;
let pollingInterval = null;

// Utility: Safe DOM get
function getElementSafe(id) {
    const el = document.getElementById(id);
    if (!el) {
        console.error(`Element with id "${id}" not found in DOM.`);
    }
    return el;
}

function drawGame(state) {
    const canvas = getElementSafe('gameCanvas');
    const scoreElem = getElementSafe('score');
    if (!canvas || !scoreElem) return;

    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    gridSize = state.grid_size;
    // Use min of width/height to ensure square cells
    cellSize = Math.min(canvas.width, canvas.height) / gridSize;

    // Draw food
    ctx.fillStyle = 'red';
    ctx.fillRect(
        state.food[0] * cellSize,
        state.food[1] * cellSize,
        cellSize,
        cellSize
    );

    // Draw snake
    ctx.fillStyle = 'green';
    for (let i = 0; i < state.snake.length; i++) {
        ctx.fillRect(
            state.snake[i][0] * cellSize,
            state.snake[i][1] * cellSize,
            cellSize,
            cellSize
        );
    }

    // Draw score
    scoreElem.innerText = 'Score: ' + state.score;

    // Game over
    if (state.game_over) {
        ctx.fillStyle = 'rgba(0,0,0,0.5)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'white';
        ctx.font = '40px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Game Over', canvas.width / 2, canvas.height / 2);
        gameOver = true;
    } else {
        gameOver = false;
    }
}

function fetchState() {
    fetch('/state')
        .then(response => {
            if (!response.ok) throw new Error('Failed to fetch state');
            return response.json();
        })
        .then(state => {
            drawGame(state);
            lastDirection = direction;
        })
        .catch(err => {
            console.error('Error fetching state:', err);
            showError('Unable to fetch game state.');
        });
}

function sendMove(newDirection) {
    fetch('/move', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({direction: newDirection})
    })
    .then(response => {
        if (!response.ok) throw new Error('Failed to send move');
        return response.json();
    })
    .then(state => {
        drawGame(state);
        lastDirection = newDirection;
    })
    .catch(err => {
        console.error('Error sending move:', err);
        showError('Unable to send move to server.');
    });
}

function showError(msg) {
    let errorElem = document.getElementById('gameError');
    if (!errorElem) {
        errorElem = document.createElement('div');
        errorElem.id = 'gameError';
        errorElem.style.position = 'absolute';
        errorElem.style.top = '10px';
        errorElem.style.left = '50%';
        errorElem.style.transform = 'translateX(-50%)';
        errorElem.style.background = 'rgba(255,0,0,0.8)';
        errorElem.style.color = 'white';
        errorElem.style.padding = '8px 16px';
        errorElem.style.borderRadius = '4px';
        errorElem.style.zIndex = '1000';
        document.body.appendChild(errorElem);
    }
    errorElem.innerText = msg;
    errorElem.style.display = 'block';
    setTimeout(() => {
        errorElem.style.display = 'none';
    }, 3000);
}

document.addEventListener('keydown', (function() {
    let lastKeyTime = 0;
    return function(event) {
        if (gameOver) return;
        const now = Date.now();
        // Debounce: ignore keys pressed within 30ms of last
        if (now - lastKeyTime < 30) return;
        lastKeyTime = now;

        let newDirection = direction;
        if (event.key === 'ArrowUp' || event.key === 'w' || event.key === 'W') newDirection = 'UP';
        else if (event.key === 'ArrowDown' || event.key === 's' || event.key === 'S') newDirection = 'DOWN';
        else if (event.key === 'ArrowLeft' || event.key === 'a' || event.key === 'A') newDirection = 'LEFT';
        else if (event.key === 'ArrowRight' || event.key === 'd' || event.key === 'D') newDirection = 'RIGHT';

        // Prevent reversing direction
        if ((lastDirection === 'UP' && newDirection === 'DOWN') ||
            (lastDirection === 'DOWN' && newDirection === 'UP') ||
            (lastDirection === 'LEFT' && newDirection === 'RIGHT') ||
            (lastDirection === 'RIGHT' && newDirection === 'LEFT')) {
            return;
        }

        if (newDirection !== direction) {
            direction = newDirection;
            sendMove(direction);
        }
    };
})());

function restartGame() {
    fetch('/reset', {method: 'POST'})
        .then(response => {
            if (!response.ok) throw new Error('Failed to reset game');
            return response.json();
        })
        .then(state => {
            direction = 'RIGHT';
            lastDirection = 'RIGHT';
            drawGame(state);
        })
        .catch(err => {
            console.error('Error resetting game:', err);
            showError('Unable to reset game.');
        });
}

// Initial state fetch on page load
window.addEventListener('DOMContentLoaded', function() {
    fetchState();

    // Start polling only after initial fetch
    if (pollingInterval) clearInterval(pollingInterval);
    pollingInterval = setInterval(function() {
        if (!gameOver) {
            sendMove(direction);
        }
    }, 100);
});
