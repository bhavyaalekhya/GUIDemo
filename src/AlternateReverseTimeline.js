import React, { useState, useEffect } from 'react';
import Timeline from '@mui/lab/Timeline';
import TimelineItem from '@mui/lab/TimelineItem';
import TimelineSeparator from '@mui/lab/TimelineSeparator';
import TimelineConnector from '@mui/lab/TimelineConnector';
import TimelineContent from '@mui/lab/TimelineContent';
import TimelineDot from '@mui/lab/TimelineDot';
import './AlternateReverseTimeline.css';

export default function AlternateReverseTimeline({ steps = [] }) {
  const [segments, setSegments] = useState([]);

  useEffect(() => {
    // The check for Array.isArray(steps) is not needed here anymore as we have default value []
    const newSegments = steps.map((step) => {
      // Verify that SubSteps is defined and is an array
      if (Array.isArray(step.SubSteps)) {
        // Determine the color based on the Done, Error, and NotSure values in SubSteps
        let color_dot = 'inherit'; // Default color mapped to Material-UI's default
        if (step.SubSteps.some(substep => substep.Error === 1)) {
          color_dot = 'error'; // Mapped to Material-UI's error color
        } else if (step.SubSteps.some(substep => substep.NotSure === 1)) {
          color_dot = 'primary'; // Use primary or secondary as an equivalent to your blue
        } else if (step.SubSteps.every(substep => substep.Done === 1)) {
          color_dot = 'success'; // Use secondary or primary as an equivalent to your green
        }
        return { state: color_dot, description: step.Step_ID };
      } else {
        // If SubSteps is not an array, log an error and return a default segment
        console.error('SubSteps is undefined or not an array', step);
        return { state: 'inherit', description: 'Undefined Step' };
      }
    }).reverse(); // Reverse the array to get the alternate reverse timeline effect
    setSegments(newSegments);
  }, [steps]);

  return (
    <Timeline className="timeline" position="alternate">
      {segments.map((segment, index) => (
        <TimelineItem key={index}>
          <TimelineSeparator>
          <TimelineDot
            style={{ transform: 'scale(3)' }}
            color={
              segment.state === 'inherit'
                ? 'inherit' // assuming 'inherit' is a valid color
                : segment.state === 'primary'
                ? 'primary' // 'primary' is usually a valid color
                : segment.state === 'error'
                ? 'error' // 'error' is usually a valid color
                : segment.state === 'success'
                ? 'success' // 'success' is a valid color in MUI v5+
                : 'inherit'
            }
          />
            {index < segments.length - 1 ? <TimelineConnector /> : null}
          </TimelineSeparator>
          <TimelineContent className="timelineContentContainer">{segment.description}</TimelineContent>
        </TimelineItem>
      ))}
    </Timeline>
  );
}
