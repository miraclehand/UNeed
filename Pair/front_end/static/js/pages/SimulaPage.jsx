import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import ListContainer from '../containers/ListContainer';
import SimulaContainer from '../containers/SimulaContainer';
import dayjs from 'dayjs'

const styles = theme => ({
    paper: {
        padding: theme.spacing.unit * 2,
        textAlign: 'center',
        color: theme.palette.text.secondary,
    },
});

class SimulaPage extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            component: '',
        }

        this.handleListItemClick  = this.handleListItemClick.bind(this)
        this.handleListItemRemove = this.handleListItemRemove.bind(this)
        this.handleComponent = this.handleComponent.bind(this)
    }

    handleListItemClick(strainer) {
        strainer.date1 = dayjs(strainer.date1).format('YYYY-MM-DD')
        strainer.date2 = dayjs(strainer.date2).format('YYYY-MM-DD')
        this.state.component.setState({strainer:strainer})
    }

    handleListItemRemove(strainer) {
        this.state.component.handleDeleteStrainer(strainer)
    }

    handleComponent(component) {
        this.state.component = component
    }

    render () {
        const { paper } = this.props.classes
        const { handleListItemClick, handleListItemRemove } = this
        const { handleComponent } = this

        return (
            <Grid container spacing={3} >
                <Grid item xs={4} >
                    <Paper className={paper}>
                        <ListContainer target={'Simula'} />
                    </Paper>
                    <br/>
                    <Paper className={paper}>
                        <ListContainer
                            target={'Strainer'}
                            handleListItemClick ={handleListItemClick}
                            handleListItemRemove={handleListItemRemove}
                        />
                    </Paper>
                </Grid>
                <Grid item xs={8}>
                    <Paper className={paper}>
                        <SimulaContainer
                            handleComponent={handleComponent}
                        />
                    </Paper>
                </Grid>
            </Grid>
        )
    }
};

export default withStyles(styles)(SimulaPage);
