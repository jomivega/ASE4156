import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import CircularProgress from 'material-ui/CircularProgress';


import Paper from 'material-ui/Paper';


export class Card_WF extends React.Component {
  render() {
    return (
        <Card zDepth={3}>
          <CardTitle title= {this.props.title} subtitle = {this.props.subtitle} />
          <CardText>
            {this.props.cardText}
          </CardText>
        </Card>
    );
  }
}

export class Media_Card_WF extends React.Component {
    render() {
        return (
        <Card zDepth={3}>
            <div>
                {this.props.content}
            </div>
        </Card>
        );
    }
}
