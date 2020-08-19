import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { Link, withRouter } from 'react-router-dom';
import classNames from 'classnames';
import Drawer from '@material-ui/core/Drawer';
import AppBar from '@material-ui/core/AppBar';
import Divider from '@material-ui/core/Divider';
import Grid from '@material-ui/core/Grid';
import IconButton from '@material-ui/core/IconButton';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import Button from '@material-ui/core/Button';
import Toolbar from '@material-ui/core/Toolbar';
import MenuList from '@material-ui/core/MenuList';
import MenuItem from '@material-ui/core/MenuItem';
import MenuIcon from '@material-ui/icons/Menu';
import LanguageIcon from '@material-ui/icons/Language';
import LanguageOutlinedIcon from '@material-ui/icons/LanguageOutlined';
import Routes from '../pages/routes';
import { HomePage, ChartPage, TradingPage, SimulaPage } from '../pages';

const drawerWidth = 240;
const styles = theme => ({
    appBar: {
        zIndex: theme.zIndex.drawer + 1,
        transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
    },
    appBarShift: {
        marginLeft: drawerWidth,
        width: `calc(100% - ${drawerWidth}px)`,
        transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
    },
    menuButton: {
        marginRight: 36,
    },
    hide: {
        display: 'none',
    },
    drawer: {
        width: drawerWidth,
        flexShrink: 0,
        whiteSpace: 'nowrap',
    },
    drawerOpen: {
        width: drawerWidth,
        transition: theme.transitions.create('width', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
    },
    drawerClose: {
        transition: theme.transitions.create('width', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
        overflowX: 'hidden',
        width: theme.spacing(7) + 1,
        [theme.breakpoints.up('sm')]: {
            width: theme.spacing(9) + 1,
        },
    },
    toolbar: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'flex-end',
        padding: '0 8px',
        ...theme.mixins.toolbar,
    },
});

function NavAppbar(props) {
    const { appBar, appBarShift, menuButton, hide } = props.classes;
    const { open, navbarName } = props
    const { handleCntry, handleSignOut, handleDrawerOpen } = props
    const { cntry } = props
    const color = cntry == 'kr' ? 'action' : 'secondary'

    return (
        <AppBar
            position='fixed'
            className={classNames(appBar, open && appBarShift)}
        >
            <Toolbar>
                <Grid justify='space-between' container alignItems='center'>
                    <Grid item>
                        <IconButton
                            color="inherit"
                            aria-label="Open drawer"
                            onClick={handleDrawerOpen}
                            edge="start"
                            className={classNames(menuButton, open && hide)}
                        >
                            <MenuIcon />
                        </IconButton>
                        { navbarName }
                    </Grid>
                    <Grid item>
                        <IconButton onClick={handleCntry}>
                            <LanguageIcon color={color} />
                        </IconButton>
                        <Button
                            color='inherit'
                            style={{textTransform:'none'}}
                            onClick={handleSignOut}
                        >
                            SignOut
                        </Button>
                    </Grid>
                </Grid>
            </Toolbar>
        </AppBar>
    )
}

function NavSidebar(props) {
    const { drawer, drawerOpen, drawerClose, toolbar } = props.classes;
    const { open } = props
    const { handleDrawerOpen, handleDrawerClose, activeRoute } = props
    const { handleMouseOver } = props

    return (
        <Drawer
            variant="permanent"
            className={classNames(drawer,
                                  open && drawerOpen,
                                 !open && drawerClose)}
            classes={{
                paper: classNames(open && drawerOpen,
                                 !open && drawerClose)
            }}
            open={open}
        >
            <div className={toolbar}>
                <IconButton onClick={handleDrawerClose}>
                    <ChevronLeftIcon />
                </IconButton>
            </div>
            <Divider />
            <List>
                {Routes.map((prop,key) => {
                    return (
                        <Link to={prop.path} style={{color:'#000'}} key={key}>
                            <ListItem 
                                selected={activeRoute(prop.path)}
                                onMouseOver={e=>handleMouseOver(prop.sidebarName)}
                            >
                                <ListItemIcon> <prop.icon /> </ListItemIcon>
                                <ListItemText primary={prop.sidebarName} />
                            </ListItem>
                        </Link>
                    );
                })}
            </List>
        </Drawer>
    )
}

export class NavigationComponent extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            open: false,
        };
        this.handleDrawerOpen = this.handleDrawerOpen.bind(this)
        this.handleDrawerClose = this.handleDrawerClose.bind(this)
        this.handleMouseOver = this.handleMouseOver.bind(this)
        this.activeRoute = this.activeRoute.bind(this);
        this.getNavbarName = this.getNavbarName.bind(this)
    }

    handleDrawerOpen() {
        this.setState({ open: true });
    };

    handleDrawerClose() {
        this.setState({ open: false });
    };
    
    handleMouseOver(sidebarName) {
        if (sidebarName == 'Home') {
            HomePage.preload();
        }
        else if (sidebarName == 'Chart') {
            ChartPage.preload();
        }
        else if (sidebarName == 'Trading') {
            TradingPage.preload();
        }
        else if (sidebarName == 'Simula') {
            SimulaPage.preload();
        }
    }

    activeRoute(routeName) {
        return this.props.location.pathname == routeName ? true : false
    }

    getNavbarName() {
        for (let i = 0 ; i < Routes.length ; ++i) {
            if (Routes[i].path == this.props.location.pathname) {
                return Routes[i].navbarName
            }
        }
        return 'None'
    }

    render () {
        const navbarName = this.getNavbarName()

        return (
            <>
                <NavAppbar
                    open={this.state.open}
                    classes={this.props.classes}
                    navbarName={navbarName}
                    handleDrawerOpen={this.handleDrawerOpen}
                    cntry={this.props.cntry}
                    handleCntry={this.props.handleCntry}
                    handleSignOut={this.props.handleSignOut}
                />
                <NavSidebar
                    open={this.state.open}
                    classes={this.props.classes}
                    handleDrawerOpen={this.handleDrawerOpen}
                    handleDrawerClose={this.handleDrawerClose}
                    activeRoute={this.activeRoute}
                    handleMouseOver={this.handleMouseOver}
                />
            </>
        )
    }
}

export default withRouter((withStyles(styles)(NavigationComponent)))
