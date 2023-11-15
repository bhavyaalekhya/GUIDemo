import React from 'react';
import './TimelineComponent.css'; // Import your CSS file

const TimelineComponent = ({ steps, name }) => {

	return (
		<div>
            <h2>{name}</h2>

			<div className="timeline-container">
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
		</div>
	);
};

export default TimelineComponent;
