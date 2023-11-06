import React, { useState, useEffect } from 'react';
import './App.css';

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Overview from "./components/overview/Overview";
import Home from "./components/home/Home";
import {w3cwebsocket} from "websocket";


function App() {
    
    const [recipeStepStates, setRecipeStepStates] = useState([]);
    const [recipeSubStepStates, setRecipeSubStepStates] = useState([]);
    
    const UPDATE_RECIPE_STEP_STATES = "update_recipe_step_states"
    const UPDATE_RECIPE_SUB_STEP_STATES = "update_recipe_sub_step_states"
    
    useEffect(() => {
        const web_client = new w3cwebsocket('ws://localhost:8000')
    
        web_client.onopen = () => console.log("Connected to WebSocket");
    
        web_client.onmessage = (message) => {
            const server_message = JSON.parse(message.data);
            const message_type  = server_message.type;
        
            // console.log(server_message)
            if (message_type === UPDATE_RECIPE_STEP_STATES){
                // console.log(server_message?.details)
                setRecipeStepStates(server_message?.details)
            } else if (message_type === UPDATE_RECIPE_SUB_STEP_STATES){
                // console.log(server_message?.details)
                setRecipeSubStepStates(JSON.parse(server_message?.details))
            }
        };
    
        web_client.onerror = (event) => {
            console.error("WebSocket error:");
        };
    
        web_client.onclose = () => console.log("Disconnected from WebSocket");
        
        
    });
    

  return (
      <BrowserRouter>
          <div className="App">
                <Routes>
                    <Route
                        exact
                        path="/"
                        element={
                            <Home
                                recipeStepStates={recipeStepStates}
                                recipeSubStepStates={recipeSubStepStates}
                            />
                        }
                    />
                    <Route
                        path="/timeline"
                        element={
                            <Home
                                recipeStepStates={recipeStepStates}
                                recipeSubStepStates={recipeSubStepStates}
                            />
                        }
                    />
                    <Route
                        path="/overview"
                        element={
                            <Overview
                                recipeStepStates={recipeStepStates}
                                recipeSubStepStates={recipeSubStepStates}
                            />
                        }
                    />
                </Routes>
          </div>
      </BrowserRouter>
  );
}

export default App;
