import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import { Switch, Route, BrowserRouter } from 'react-router-dom'
import NavigationContainer from './containers/NavigationContainer';
import { HomePage, ChartPage, TradingPage, SimulaPage, SignInPage, PopupPage } from './pages';

const styles = theme => ({
    root: {
        display: 'flex',
    },
    content: {
        flexGrow: 1,
        paddingLeft: theme.spacing(1),
        paddingRight: theme.spacing(1),
        paddingTop: theme.spacing(10),
    },
});

export class App extends React.Component {
    constructor(props) {
        super(props)
    }

    render () {
        const { root, content } = this.props.classes;

        return (
            <BrowserRouter>
                <div className={root}>
                    <CssBaseline />
                    <NavigationContainer />
                    <SignInPage />
                    <div className={content}>
                        <Switch>
                            <Route exact path='/' component={HomePage} />
                            <Route path='/chart' component={ChartPage} />
                            <Route path='/trading' component={TradingPage} />
                            <Route path='/simula' component={SimulaPage} />
                        </Switch>
                    </div>
                    <PopupPage />
                </div>
            </BrowserRouter>
        )
    }
}

export default withStyles(styles)(App);
