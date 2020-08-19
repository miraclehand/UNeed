import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import SwipeableViews from 'react-swipeable-views';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import DiscPage from './DiscPage';

const styles = theme => ({
    root: {
        backgroundColor: theme.palette.background.paper,
        flexGrow: 1,
    },
    tabs: {
        indicatorColor: 'primary',
        textColor: 'primary',
        variant: 'fullWidth',
    },
    nested: {
        paddingLeft: theme.spacing.unit * 4,
    },
});

export class HomePage extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            value: 0,
        };

        this.handleChangeTab = this.handleChangeTab.bind(this)
        this.handleChangeTabIndex = this.handleChangeTabIndex.bind(this)

    }

    handleChangeTab(event, value){
        this.setState({ value });
    };

    handleChangeTabIndex(index) {
        this.setState({ value: index });
    };

    render () {
        const { classes, theme } = this.props;
        const { handleChangeTab, handleChangeTabIndex } = this

        return (
            <div className={classes.root}>
                <AppBar position="static" color="default" >
                    <Tabs
                        indicatorColor='primary'
                        textColor='primary'
                        variant='fullWidth'
                        value={this.state.value}
                        onChange={handleChangeTab}
                    >
                        <Tab label='키워드' />
                        <Tab label='오오미' />
                        <Tab label='히이이' />
                    </Tabs>
                </AppBar>
                <SwipeableViews
                    axis={theme.direction === 'rtl' ? 'x-reverse' :'x'}
                    index={this.state.value}
                    onChangeIndex={handleChangeTabIndex}
                    style={{ height:400, WebkitOverflowScrolling:'touch' }}
                >
                </SwipeableViews>

            </div>
        )
        return (
            <DiscPage />
        )
    }
}

export default withStyles(styles, {withTheme:true})(HomePage);

