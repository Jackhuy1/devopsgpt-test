const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const gridSize = 20;
const tileCount = Math.floor(canvas.width / gridSize);

let snake = [{ x: 10, y: 10 }];
let velocity = { x: 1, y: 0 }; // Start moving right by default
let food = { x: 15, y: 15 };
let score = 0;
let gameOver = false;

function resetGame() {
    snake = [{ x: 10, y: 10 }];
    velocity = { x: 1, y: 0 };
    score = 0;
    gameOver = false;
    placeFood();
}

function gameLoop() {
    if (gameOver) {
        drawGameOver();
        return;
    }
    update();
    draw();
}

function update() {
    // Move snake by velocity
    let head = { x: snake[0].x + velocity.x, y: snake[0].y + velocity.y };

    // Check wall collision
    if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
        gameOver = true;
        return;
    }

    // Check self collision
    for (let segment of snake) {
        if (segment.x === head.x && segment.y === head.y) {
            gameOver = true;
            return;
        }
    }

    snake.unshift(head);

    // Check food collision
    if (head.x === food.x && head.y === food.y) {
        score++;
        placeFood();
    } else {
        snake.pop();
    }
}

function draw() {
    // Clear canvas
    ctx.fillStyle = '#fff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw snake
    ctx.fillStyle = '#00FF00';
    for (let segment of snake) {
        ctx.fillRect(segment.x * gridSize, segment.y * gridSize, gridSize, gridSize);
    }

    // Draw food
    ctx.fillStyle = '#FF0000';
    ctx.fillRect(food.x * gridSize, food.y * gridSize, gridSize, gridSize);

    // Draw score if element exists
    const scoreElement = document.getElementById('score');
    if (scoreElement) {
        scoreElement.innerText = 'Score: ' + score;
    }
}

function drawGameOver() {
    // Clear canvas
    ctx.fillStyle = '#fff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw final snake
    ctx.fillStyle = '#00FF00';
    for (let segment of snake) {
        ctx.fillRect(segment.x * gridSize, segment.y * gridSize, gridSize, gridSize);
    }

    // Draw food
    ctx.fillStyle = '#FF0000';
    ctx.fillRect(food.x * gridSize, food.y * gridSize, gridSize, gridSize);

    // Draw Game Over text
    ctx.fillStyle = '#000';
    ctx.font = '30px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('Game Over!', canvas.width / 2, canvas.height / 2 - 20);
    ctx.font = '20px Arial';
    ctx.fillText('Your score: ' + score, canvas.width / 2, canvas.height / 2 + 10);
    ctx.fillText('Press Enter to Restart', canvas.width / 2, canvas.height / 2 + 40);
}

function placeFood() {
    let validPosition = false;
    while (!validPosition) {
        food.x = Math.floor(Math.random() * tileCount);
        food.y = Math.floor(Math.random() * tileCount);

        validPosition = true;
        for (let segment of snake) {
            if (segment.x === food.x && segment.y === food.y) {
                validPosition = false;
                break;
            }
        }
    }
}

window.addEventListener('keydown', function (e) {
    if (gameOver) {
        if (e.key === 'Enter') {
            resetGame();
        }
        return;
    }

    switch (e.key) {
        case 'ArrowUp':
            if (velocity.y === 1) break;
            velocity = { x: 0, y: -1 };
            break;
        case 'ArrowDown':
            if (velocity.y === -1) break;
            velocity = { x: 0, y: 1 };
            break;
        case 'ArrowLeft':
            if (velocity.x === 1) break;
            velocity = { x: -1, y: 0 };
            break;
        case 'ArrowRight':
            if (velocity.x === -1) break;
            velocity = { x: 1, y: 0 };
            break;
    }
});

placeFood();
setInterval(gameLoop, 100);
