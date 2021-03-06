// @flow
import React from 'react';
import { createFragmentContainer, graphql } from 'react-relay';
import { ConnectionHandler } from 'relay-runtime';
import Grid from 'material-ui/Grid';
import Button from 'material-ui/Button';
import AddIcon from 'material-ui-icons/Add';

import type { RelayContext } from 'react-relay';

import InvestBucketRelay from './InvestBucketRelay';
import EditBucket from '../EditBucket/EditBucket';
import createBucket from '../../mutations/BucketEdit/CreateBucket';

import type { InvestBucketGridRelay_profile } from './__generated__/InvestBucketGridRelay_profile.graphql';

type Props = {
  profile: InvestBucketGridRelay_profile,
  relay: RelayContext,
}
type State = {
  showDialog: bool,
  errors: ?Array<Error>,
}

class InvestBucketGridRelay extends React.Component<Props, State> {
  constructor() {
    super();
    this.state = {
      showDialog: false,
      errors: [],
    };
  }
  dialogAction = diagState => () => {
    this.setState(() => ({
      showDialog: diagState,
    }));
  }
  dialogSave = (name: string, publicBucket: bool, investment: number) => {
    let updater = null;
    if (publicBucket) {
      updater = (store) => {
        const connection = ConnectionHandler.getConnection(
          store.get(this.props.profile.id),
          'InvestBucketGridRelay_investSuggestions',
        );
        const newEdge = ConnectionHandler.createEdge(
          store,
          connection,
          store.getRootField('addBucket').getLinkedRecord('bucket'),
          'GInvestmentBucketConnection',
        );
        ConnectionHandler.insertEdgeAfter(connection, newEdge);
      };
    }
    createBucket(
      updater,
      updater,
      (response: ?Object, errors: ?[Error]) => {
        if (errors) {
          const e = errors[0];
          this.setState(() => ({ errors: [e] }));
        } else {
          this.dialogAction(false)();
        }
      },
    )(
      this.props.relay.environment,
    )(
      { name, public: publicBucket, investment },
    );
  }
  render() {
    if (!this.props.profile.investSuggestions) {
      return null;
    }
    return (
      <Grid container spacing={16} align="stretch">
        {
          this.props.profile.investSuggestions.edges.map(b => (b && b.node ? (
            <Grid item xs={12} sm={8} lg={4} key={b.node.id}>
              <InvestBucketRelay profile={this.props.profile} bucket={b.node} />
            </Grid>
          ) : null))
        }
        <Grid item xs={12} sm={8} lg={4}>
          <Button fab color="primary" aria-label="add" onClick={this.dialogAction(true)}>
            <AddIcon />
          </Button>
        </Grid>
        {
          this.state.showDialog ?
            <EditBucket
              save={this.dialogSave}
              cancel={this.dialogAction(false)}
              errors={this.state.errors}
            /> :
            null
        }
      </Grid>
    );
  }
}

export default createFragmentContainer(InvestBucketGridRelay, {
  profile: graphql`
    fragment InvestBucketGridRelay_profile on GProfile {
      id
      investSuggestions(first: 3) @connection(key: "InvestBucketGridRelay_investSuggestions") {
        edges {
          node {
            id
            ...InvestBucketRelay_bucket
          }
        }
      }
      ...InvestBucketRelay_profile
    }
  `,
});
