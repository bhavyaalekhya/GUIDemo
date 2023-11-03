import React from 'react';
import './App.css';
import AlternateReverseTimeline from './AlternateReverseTimeline';

function App({ recipes }) {
  const segmentStyle = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'flex-start',
    height: '600px',
  };

  return (
    <div className="App">
      {recipes.map((recipe) => (
        // Use a unique identifier for each recipe as the key
        <div key={recipe.Steps_ID} className="segment" style={segmentStyle}>
          {/* Pass the SubSteps array to the component */}
          <AlternateReverseTimeline steps={recipe.Steps} />
        </div>
      ))}
    </div>
  );
}

export default App;
