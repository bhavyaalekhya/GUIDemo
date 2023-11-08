import React, { useEffect, useState } from "react";
import AppBar from "../atoms/AppBar";
import './Overview.css'; // Ensure this file includes the new CSS styles

//0: "Not Done", 1: "In Progress", 2: "Done", 3: "Missing", 4: "Ordering", 5: "Technique", 6: "Preparation",

const Overview = (props) => {
	const { recipeStepStates, recipeSubStepStates } = props;
	const [selectedRecipe, setSelectedRecipe] = useState(null);
	
	const handleRecipeClick = (recipe) => {
		setSelectedRecipe(recipe);
	};
	
	useEffect(() => {
		console.log("recipe sub steps changed");
		console.log(typeof(recipeSubStepStates));
	}, [recipeSubStepStates]);
	
	return (
		<div className="overviewContainer">
			<div className="header">
				<AppBar />
			</div>
			
			<div className="overviewBodyContainer">
				<div className="recipeSubStepStatesList">
					{recipeSubStepStates?.map((recipe, index) => (
						<div key={index} className="recipeBox" onClick={() => handleRecipeClick(recipe)}>
							{recipe?.recipe}
						</div>
					))}
				</div>
				<div className="detailsContainer">
					{selectedRecipe && selectedRecipe?.recipe_sub_step_states?.map((step, index) => (
						<div key={index} className="stepContainer">
							<h3>{step.step}</h3>
							{step.sub_steps?.map((subStep, subIndex) => (
								<div key={subIndex} className={`subStep state-${subStep.state}`}>
									<span className="subStepText">{subStep.sub_step}</span>
  									<span className="subStepState">{subStep.state}</span>
								</div>
							))}
						</div>
					))}
				</div>
			</div>
		</div>
	);
};

export default Overview;
