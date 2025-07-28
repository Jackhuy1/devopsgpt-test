import React from 'react';

function Score({ score }) {
  return (
    <div
      style={{
        fontSize: '24px',
        fontWeight: 'bold',
        marginBottom: '10px',
        color: '#333',
      }}
    >
      Score: {score ?? 0}
    </div>
  );
}

export default Score;
