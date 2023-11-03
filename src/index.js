import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';

// Function to fetch and load JSON data
// Function to fetch and load JSON data
const fetchRecipes = async () => {
  try {
    // Import recipes.json directly from the src directory
    const data = require('./recipes.json');
    return data;
  } catch (error) {
    console.error('Error fetching data:', error);
    return [];
  }
};


// Render the app with fetched recipes
fetchRecipes()
  .then((recipes) => {
    ReactDOM.render(
      <React.StrictMode>
        <App recipes={recipes} />
      </React.StrictMode>,
      document.getElementById('root')
    );
  })
  .catch((error) => {
    console.error('Error rendering app:', error);
  });
