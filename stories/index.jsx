import React from 'react';

import { storiesOf, addDecorator } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import { linkTo } from '@storybook/addon-links';

<<<<<<< HEAD
import { number, text } from '@storybook/addon-knobs';

import AppBar from '../web/js/components/AppBar';
import { CardWF, MediaCardWF } from '../web/js/components/Cards';
import PageTest from './PageTest';

storiesOf('AppBar', module).add('Main app bar', () => <AppBar />);

storiesOf('Cards', module).add('Simple card', () => <CardWF title="Title" subtitle="sub" cardText="fdsa" />).add('Content card', () => <MediaCardWF content={<h1 > Content </h1>} />);

storiesOf('Page', module).add('Test page', () => {
  const res = <PageTest />;
  return res;
});
=======
import { muiTheme } from 'storybook-addon-material-ui';
import appTheme from '../web/js/theme/muiTheme'
import { Button, Welcome } from '@storybook/react/demo';

import Shares from '../web/js/components/shares';
import AppBar from '../web/js/components/appbar';
import {Card_WF, Media_Card_WF} from '../web/js/components/card_wf';


storiesOf('Shares', module)
  .addDecorator(muiTheme(appTheme))
  .add('simple', () => <Shares />);


storiesOf('AppBar', module)
.addDecorator(muiTheme(appTheme))
.add('Main app bar', () => <AppBar/>);

storiesOf('Cards', module)
  .addDecorator(muiTheme(appTheme))
  .add('Simple card', () => <Card_WF title="Title" subtitle="sub" cardText="fdsa"/>)
  .add('Content card', () => <Media_Card_WF content = {<h1>Content</h1>}/>);
>>>>>>> Adding App Bar and Cards
