import React from 'react';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import './TimelineStep.css';

const TimelineStep = ({ step, index, totalSteps}) => {
  return (
    <React.Fragment>
      <div className='marker'>{index + 1}</div>
      <Paper className='description'>
        <Typography variant="h6">{step.title}</Typography>
        <Typography variant="body1">{step.description}</Typography>
      </Paper>
      {index < totalSteps - 1 && <div className='connector'></div>}
    </React.Fragment>
  );
};

export default TimelineStep;
