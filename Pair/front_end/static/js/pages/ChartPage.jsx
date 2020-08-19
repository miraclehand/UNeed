import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import ListContainer from '../containers/ListContainer';
import ChartFormContainer from '../containers/ChartFormContainer';
import ChartContainer from '../containers/ChartContainer';

const styles = theme => ({
    paper: {
        padding: theme.spacing.unit * 2,
        textAlign: 'center',
        color: theme.palette.text.secondary,
    },
});

export class ChartPage extends React.Component {
    constructor(props) {
        super(props)
    }

    render () {
        const { paper } = this.props.classes

        return (
            <div>
                <h1 align='center'>Welcome SpreadChart !</h1>
                <Grid container spacing={3} >
                    <Grid item xs={6} >
                        <Paper className={paper}>
                            <ListContainer target={'PickedPair'} />
                        </Paper>
                    </Grid>
                    <Grid item xs={6}>
                        <Paper className={paper}>
                            <ChartFormContainer />
                        </Paper>
                    </Grid>
                    <Grid item xs={12} >
                        <Paper className={paper}>
                            <ChartContainer />
                        </Paper>
                    </Grid>
                </Grid>
            </div>
        )
    }
}

export default withStyles(styles)(ChartPage);
