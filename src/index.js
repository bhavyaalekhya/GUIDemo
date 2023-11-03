import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';

// Set up a WebSocket connection
const setupWebSocket = (setRecipes) => {
  const socket = new WebSocket('ws://localhost:8000'); // Adjust the URL to match your server.py WebSocket address
  
    socket.onopen = () => {
      console.log('WebSocket Connected');
    };
  
    socket.onmessage = (event) => {
      try {
        // Assuming the server sends individual JSON recipe objects
        const recipe = JSON.parse(event.data);
        setRecipes((prevRecipes) => [...prevRecipes, recipe]);
      } catch (error) {
        console.error('Error parsing data:', error);
      }
    };
  
    // ...
  
    return socket; // Return socket if you need to send messages to the server
  };
  

const Main = () => {
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    // Initialize WebSocket connection and handle incoming data
    const socket = setupWebSocket(setRecipes);

    // Clean up the WebSocket connection when this component is unmounted
    return () => {
      if (socket) {
        socket.close();
      }
    };
  }, []);

  return (
    <React.StrictMode>
      <App recipes={recipes} />
    </React.StrictMode>
  );
};

ReactDOM.render(
  <Main />,
  document.getElementById('root')
);

