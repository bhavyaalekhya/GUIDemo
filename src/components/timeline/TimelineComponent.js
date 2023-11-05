import React from 'react';
import './TimelineComponent.css'; // Import your CSS file

const TimelineComponent = ({ steps }) => {
	return (
		<div className="timeline-container">
			{steps.map((step, index) => (
				<div key={index} className="timeline-item">
					<div className={`timeline-marker ${step.state === 0 ? 'inactive' : 'active'}`}></div>
					<div className="timeline-content">
						<p>{step.step}</p>
					</div>
				</div>
			))}
		</div>
	);
};

export default TimelineComponent;
