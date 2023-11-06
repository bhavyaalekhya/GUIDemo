import {useNavigate} from "react-router-dom";
import AppBar from "../atoms/AppBar";
import React, {useEffect, useState} from "react";
import * as PropTypes from "prop-types";
import AlternateReverseTimeline from "../timeline/AlternateReverseTimeline";
import TimelineComponent from "../timeline/TimelineComponent";

const Home = (props) => {
	const { recipeStepStates, recipeSubStepStates } = props;
	const navigate = useNavigate();

	return (
		<div className="homeContainer">
			<div className="header">
				<AppBar/>
			</div>
			
			<div className="homeBodyContainer">
				
				{
					recipeStepStates?.map((recipeStepState, listIndex) => (
						<TimelineComponent key={listIndex} steps={recipeStepState.recipe_states} />
					))
				}
			
			</div>
		</div>
	);
};

export default Home;