import React from 'react';
import './TimelineComponent.css'; // Import your CSS file

// 0 - Incomplete, 1 - Error Present, 2 - Complete

const TimelineComponent = ({ steps }) => {

	return (
		<div className="timeline-container">
			{/* Place the timeline line here and make sure it starts from the first item */}
			<div className="timeline-line"></div>

			{steps?.map((step, index) => (
				<div key={index} className="timeline-item">
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
