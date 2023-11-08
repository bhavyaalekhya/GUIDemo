import React, { useState, useEffect } from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Overview from "./components/overview/Overview";
import Home from "./components/home/Home";
import { addListener, removeListener } from './socket';

function App() {
  const [recipeStepStates, setRecipeStepStates] = useState([]);
  const [recipeSubStepStates, setRecipeSubStepStates] = useState([]);

  useEffect(() => {
    const handleRecipeStepStates = (details) => {
      setRecipeStepStates(details);
    };

    const handleRecipeSubStepStates = (details) => {
      setRecipeSubStepStates(JSON.parse(details));
    };

    addListener("update_recipe_step_states", handleRecipeStepStates);
    addListener("update_recipe_sub_step_states", handleRecipeSubStepStates);

    // Cleanup function to remove the listeners when the component unmounts
    return () => {
      removeListener("update_recipe_step_states", handleRecipeStepStates);
      removeListener("update_recipe_sub_step_states", handleRecipeSubStepStates);
    };
  }, []);

  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          <Route
            exact
            path="/"
            element={<Home recipeStepStates={recipeStepStates} recipeSubStepStates={recipeSubStepStates} />}
          />
          <Route
            path="/timeline"
            element={<Home recipeStepStates={recipeStepStates} recipeSubStepStates={recipeSubStepStates} />}
          />
          <Route
            path="/overview"
            element={<Overview recipeStepStates={recipeStepStates} recipeSubStepStates={recipeSubStepStates} />}
          />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
