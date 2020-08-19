import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import SwipeableViews from 'react-swipeable-views';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Collapse from '@material-ui/core/Collapse';
import SaveAlt from '@material-ui/icons/SaveAlt';
import Send from '@material-ui/icons/Send';
import IconButton from '@material-ui/core/IconButton';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import DeleteOutlinedIcon from '@material-ui/icons/DeleteOutlined';
import StarBorder from '@material-ui/icons/StarBorder';
import ExpandLess from '@material-ui/icons/ExpandLess';
import ExpandMore from '@material-ui/icons/ExpandMore';
import Divider from '@material-ui/core/Divider';
import Add from '@material-ui/icons/Add';
import Remove from '@material-ui/icons/Remove';
import { changeStock } from '../actions/ListAction';
import * as CONST from '../constants/constants';

import '../../css/BaseStyle.css';

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

class ListComponent extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            tabIndex: 0,
            labels: this.props.labels,
            lists: [],
        };
        this.handleChangeTab = this.handleChangeTab.bind(this)
        this.handleChangeTabIndex = this.handleChangeTabIndex.bind(this)
        this.handleListItemRemove = this.handleListItemRemove.bind(this)
        this.genNewLists = this.genNewLists.bind(this)
        this.genListFileItem = this.genListFileItem.bind(this)
        this.genListObjectItem = this.genListObjectItem.bind(this)
    }

    genListFileItem(row, handleListItemClick) {
        return (
            <ListItem button divider component='a' href={row['link']} >
                <ListItemIcon>
                    <SaveAlt />
                </ListItemIcon>
                <ListItemText primary={row['label']} />
            </ListItem>
        )
    }

    genListObjectItem(row, handleListItemClick) {
        return (
            <ListItem divider >
                <ListItem button onClick={(e)=>handleListItemClick(row)} >
                    <ListItemIcon>
                        <Send />
                    </ListItemIcon>
                    <ListItemText primary={row['label']} />
                </ListItem>
                <IconButton onClick={(e)=> this.handleListItemRemove(row)} >
                    <DeleteOutlinedIcon />
                </IconButton>
            </ListItem>
        )
    }

    genNewLists(nextProps) {
        const list_type = nextProps.list_type
        const lists = nextProps.lists
        const handleListItemClick = nextProps.handleListItemClick
        const genListItem = list_type == 'File' ? this.genListFileItem : this.genListObjectItem

        let new_lists = {}
        Object.keys(lists).map((key) => {
            new_lists[key] = []
            for (let i = 0 ; i < lists[key].length ; ++i) {
                new_lists[key].push(genListItem(lists[key][i], handleListItemClick))
            }
        })
        return new_lists

        for (let i = 0 ; lists && i < lists.length ; ++i) {
            const new_list = []
            const list = lists[i]

            for (let j = 0 ; list && j < list.length ; ++j) {
                const row = list[j]

                new_list.push(genListItem(row, handleListItemClick))
            }
            new_lists[i] = new_list
        }
        return new_lists
    }

    handleListItemRemove(row) {
        this.props.handleListItemRemove(row)
    }

    handleChangeTab(event, tabIndex) {
        this.setState({ tabIndex });
    };

    handleChangeTabIndex(tabIndex) {
        this.setState({ tabIndex });
    };

    shouldComponentUpdate(nextProps, nextState) {
        const vitalPropsChange = this.props.lists !== nextProps.lists;
        const vitalStateChange = this.state.tabIndex !== nextState.tabIndex;

        if (vitalPropsChange) {
            this.state.lists = this.genNewLists(nextProps)
        }
        return vitalPropsChange || vitalStateChange;
    }

    render() {
        const { classes, theme } = this.props;
        const { labels } = this.state
        const { handleChangeTab, handleChangeTabIndex } = this

        return (
            <div className={classes.root}>
                <AppBar position="static" color="default" >
                    <Tabs
                        indicatorColor='primary'
                        textColor='primary'
                        variant='fullWidth'
                        value={this.state.tabIndex}
                        onChange={handleChangeTab}
                    >
                        {labels.map((label, i) => {
                            return (<Tab label={label} />);
                        })}
                    </Tabs>
                </AppBar>
                <SwipeableViews
                    axis={theme.direction === 'rtl' ? 'x-reverse' :'x'}
                    index={this.state.tabIndex}
                    onChangeIndex={handleChangeTabIndex}
                    style={{ height:400, WebkitOverflowScrolling:'touch' }}
                >
                    <div> <List> {this.state.lists['kr']} </List> </div>
                    <div> <List> {this.state.lists['us']} </List> </div>
                    <div> <List> {this.state.lists['cn']} </List> </div>
                    <div> <List> {this.state.lists['jp']} </List> </div>
                </SwipeableViews>
            </div>
        );
    }
}

export default withStyles(styles, {withTheme:true})(ListComponent);

