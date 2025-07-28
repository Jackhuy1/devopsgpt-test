const express = require('express');
const path = require('path');
const helmet = require('helmet');
const morgan = require('morgan');

const app = express();
const PORT = process.env.PORT || 5000;

// Use Helmet to set security-related HTTP headers
app.use(helmet());

// Use morgan for HTTP request logging
app.use(morgan('combined'));

// Serve static files from the React app build directory
app.use(express.static(path.join(__dirname, 'build')));

// For any other requests, send back React's index.html file.
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Internal Server Error');
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
