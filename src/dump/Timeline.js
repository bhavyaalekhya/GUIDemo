import React from 'react';
import TimelineStep from './TimelineStep';
import './Timeline.css'

const timelineData = [
  {
    title: 'Step 1',
    description: 'Description for Step 1',
  },
  {
    title: 'Step 2',
    description: 'Description for Step 2',
  },
  {
    title: 'Step 3',
    description: 'Description for Step 3',
  },
  {
    title: 'Step 4',
    description: 'Description for Step 4',
  },
];

const Timeline =  () => {
  return (
    <div className='timeline'>
      {timelineData.map((step, index) => (
        <TimelineStep key={index} step={step} index={index} totalSteps={timelineData.length} />
      ))}
    </div>
  );
};

export default Timeline;
