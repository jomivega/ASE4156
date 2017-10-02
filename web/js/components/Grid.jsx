import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from 'material-ui/styles';
import Paper from 'material-ui/Paper';
import Grid from 'material-ui/Grid';
import {CardWF, MediaCardWF} from './Cards';
import StockGraph from './StockGraph/StockGraph';
import {select} from '@storybook/addon-knobs';

const values = [
  {
    name: 'Chart 1',
    data: [
      {
        date: new Date(2007, 1),
        value: 1
      }, {
        date: new Date(2008, 1),
        value: 2
      }, {
        date: new Date(2009, 1),
        value: 4
      }, {
        date: new Date(2011, 1),
        value: 6
      }
    ]
  }, {
    name: 'Chart 2',
    data: [
      {
        date: new Date(2007, 1),
        value: 5
      }, {
        date: new Date(2008, 1),
        value: 2
      }, {
        date: new Date(2009, 1),
        value: 1
      }, {
        date: new Date(2010, 1),
        value: 7
      }
    ]
  }
];

const styles = theme => ({
  root: {
    flexGrow: 1,
    marginTop: 0,
  },
  paper: {
    padding: 5,
    textAlign: 'center',
    color: theme.palette.text.secondary
  },
  grid: {

  }
});

function WFAutoGrid(props) {
  const classes = props.classes;

  return (
    <div className={classes.root}>
      <Grid container spacing={8}>
        <Grid item xs>

          <Grid container spacing={8}>
            <Grid item xs>
              <MediaCardWF content={<h1> Content </h1>} />
            </Grid>
            <Grid item xs>
              <MediaCardWF content={<h1> Content </h1>} />
            </Grid>
          </Grid>

          <Grid container spacing={8}>
            <Grid item xs>
              <MediaCardWF content={<h1> Content </h1>} />
            </Grid>
            <Grid item xs>
              <MediaCardWF content={<h1> Content </h1>} />
            </Grid>
          </Grid>
        </Grid>

        <Grid item xs>
          <Paper className={classes.paper}><StockGraph id={'chart'} compare={select('Compare type', [
      'PERCENT', 'ABSOLUTE'
    ], 'ABSOLUTE')} quotes={values} />
          </Paper>
        </Grid>
      </Grid>

      <Grid container spacing={8}>

        <Grid item xs>
          <Grid container spacing={8}>
            <Grid item xs>
              <MediaCardWF  content={<h1 > Content </h1>} />
            </Grid>
            <Grid item xs>
              <MediaCardWF content={<h1 > Content </h1>} />
            </Grid>
          </Grid>

          <Grid container spacing={8}>
            <Grid item xs>
              <MediaCardWF content={<h1 > Content </h1>} />
            </Grid>
            <Grid item xs>
              <MediaCardWF content={<h1 > Content </h1>} />
            </Grid>
          </Grid>
        </Grid>

        <Grid item xs>
          <Grid container spacing={8}>
            <Grid item xs>
              <CardWF title="Risk 1" cardText = "fs"/>
            </Grid>
            <Grid item xs>
              <CardWF title="Risk 2" cardText = "fs"/>
            </Grid>
            <Grid item xs>
              <CardWF title="Risk 3" cardText = "fs"/>
            </Grid>
          </Grid>
        </Grid>

      </Grid>

    </div>
  );
}

WFAutoGrid.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(WFAutoGrid);
