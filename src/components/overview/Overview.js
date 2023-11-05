import AppBar from "../atoms/AppBar";
import React from "react";

const Overview = (props) => {
	
	const { recipeStepStates, recipeSubStepStates } = props;
	
	return (
		<div className="comprehensiveContainer">
			<div className="header">
				<AppBar/>
			</div>
			
			<div className="homeBodyContainer">
			

			
			</div>
		</div>
	);
}

export default Overview;