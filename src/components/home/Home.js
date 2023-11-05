import {useNavigate} from "react-router-dom";
import AppBar from "../atoms/AppBar";
import React, {useEffect, useState} from "react";
import * as PropTypes from "prop-types";
import AlternateReverseTimeline from "../timeline/AlternateReverseTimeline";
import TimelineComponent from "../timeline/TimelineComponent";

const Home = (props) => {
	const { recipeStepStates, recipeSubStepStates } = props;
	const navigate = useNavigate();
	
	// const segmentStyle = {
	// 	display: 'flex',
	// 	justifyContent: 'center',
	// 	alignItems: 'flex-start',
	// 	height: 'auto',
	// };
	//
	// const UPDATE_RECIPE = "update recipe";
	// const UPDATE_STATUS = "update status";
	// const UPDATE_ERRORS = "update errors";
	// const [recipeMap, setRecipeMap] = useState(() => initializeRecipeMap(recipes));
	//
	// const initializeRecipeMap = (recipes) => {
	// 	let map = new Map();
	// 	recipes.forEach((recipe) => {
	// 		console.log("Type:",typeof(recipe.Details.RecipeState));
	// 		map.set(recipe.Details.Recipe, {
	// 			Recipe: recipe.Details.Recipe,
	// 			RecipeState: recipe.Details.RecipeState, // Assuming RecipeState is a JSON string
	// 			Errors: recipe.Details.Errors || []
	// 		});
	// 	});
	// 	return map;
	// };
	//
	// initializeRecipeMap(recipes);
	//
	// useEffect(() => {
	// 	recipes.forEach((recipe) => {
	// 		if (recipe.Type === UPDATE_RECIPE) {
	// 			const existingRecipe = recipeMap.get(recipe.Details.Recipe);
	// 			if (existingRecipe) {
	// 				// Update the existing recipe
	// 				existingRecipe.RecipeState = recipe.Details.RecipeState;
	// 			} else {
	// 				// Add a new recipe to the map
	// 				const newRecipe = {
	// 					Recipe: recipe.Details.Recipe,
	// 					RecipeState: recipe.Details.RecipeState,
	// 				};
	// 				setRecipeMap((prevRecipeMap) => new Map(prevRecipeMap.set(recipe.Details.Recipe, newRecipe)));
	// 			}
	// 		} else if (recipe.Type === UPDATE_STATUS) {
	// 			const existingRecipe = recipeMap.get(recipe.Details.Recipe);
	// 			if (existingRecipe) {
	// 				existingRecipe.RecipeState = recipe.Details.RecipeState;
	// 			} else {
	// 				const newRecipe = {
	// 					Recipe: recipe.Details.Recipe,
	// 					RecipeState: recipe.Details.RecipeState,
	// 				};
	// 				setRecipeMap((prevRecipeMap) => new Map(prevRecipeMap.set(recipe.Details.Recipe, newRecipe)));
	// 			}
	// 		} else if (recipe.Type === UPDATE_ERRORS) {
	// 			const existingRecipe = recipeMap.get(recipe.Details.Recipe);
	// 			if (existingRecipe) {
	// 				existingRecipe.Errors = recipe.Details.Errors;
	// 			} else {
	// 				const newRecipe = {
	// 					Recipe: recipe.Details.Recipe,
	// 					RecipeState: [],
	// 					Errors: recipe.Details.Errors,
	// 				};
	// 				setRecipeMap((prevRecipeMap) => new Map(prevRecipeMap.set(recipe.Details.Recipe, newRecipe)));
	// 			}
	// 		}
	// 	});
	// }, [recipes, recipeMap]);
	
	return (
		<div className="homeContainer">
			<div className="header">
				<AppBar/>
			</div>
			
			<div className="homeBodyContainer">
				
				{
					recipeStepStates.map((recipeStepState, listIndex) => (
							<TimelineComponent key={listIndex} steps={recipeStepState.recipe_states} />
					))
				}
				
				{/*<TimelineComponent steps={recipeStepStates.recipe_states} />*/}
				
				{/*{[...recipeMap.values()].map((recipe) => (*/}
				{/*	<div key={recipe.Recipe} className="segment" style={segmentStyle}>*/}
				{/*		<AlternateReverseTimeline steps={recipe.RecipeState} />*/}
				{/*	</div>*/}
				{/*))}*/}

			</div>
		</div>
	);
};

export default Home;