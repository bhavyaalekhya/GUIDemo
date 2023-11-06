import React from 'react';
import './TimelineComponent.css'; // Import your CSS file

const TimelineComponent = ({ steps }) => {
	return (
		<div className="timeline-container">
			{steps?.map((step, index) => (
				<div key={index} className="timeline-item">
					{/* Add line element here */}
					{index < steps.length - 1 && <div className="timeline-line"></div>}
					<div className={`timeline-marker state-${step.state}`}></div>
					<div className="timeline-content">
						<p>{step.step}</p>
					</div>
				</div>
			))}
		</div>
	);
};

export default TimelineComponent;
