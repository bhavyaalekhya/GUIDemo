import React, { useEffect, useState } from "react";
import AppBar from "../atoms/AppBar";
import './Overview.css'; // Ensure this file includes the new CSS styles

const Overview = (props) => {
	const { recipeStepStates, recipeSubStepStates } = props;
	const [selectedRecipe, setSelectedRecipe] = useState(null);

	// State descriptions mapping
	const stateDescriptions = {
		0: "Not Done",
		1: "In Progress",
		2: "Done",
		3: "Missing Error",
		4: "Ordering Error",
		5: "Technique Error",
		6: "Preparation Error",
		7: "Not Done"
	};
	
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
				<div className="gridContainer">
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
									<div className="stateBox">
										{stateDescriptions[subStep.state]}
									</div>
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
