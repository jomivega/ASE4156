import React from 'react';

import { storiesOf } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import { linkTo } from '@storybook/addon-links';

import { muiTheme } from 'storybook-addon-material-ui';
import appTheme from '../web/js/theme/muiTheme'
import { Button, Welcome } from '@storybook/react/demo';

import Shares from '../web/js/components/shares';
import AppBar from '../web/js/components/appbar';
import {CardWF, MediaCardWF} from '../web/js/components/card_wf';


storiesOf('Shares', module)
  .addDecorator(muiTheme(appTheme))
  .add('simple', () => <Shares />);


storiesOf('AppBar', module)
.addDecorator(muiTheme(appTheme))
.add('Main app bar', () => <AppBar/>);

storiesOf('Cards', module)
  .addDecorator(muiTheme(appTheme))
  .add('Simple card', () => <CardWF title="Title" subtitle="sub" cardText="fdsa"/>)
  .add('Content card', () => <MediaCardWF content = {<h1>Content</h1>}/>);
