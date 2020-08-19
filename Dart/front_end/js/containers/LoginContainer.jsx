import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import * as AppAuth from 'expo-app-auth';
/*
import { AUTH_CONFIG, cacheAuthAsync, signOutAsync } from '../init/InitUser';
*/
import { requestPostUser } from '../actions/UserAction';
import { signInAsync } from '../init/InitUser';
import LoginComponent from '../components/LoginComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)

        this.handleSignIn = this.handleSignIn.bind(this)
        this.handleSignOut = this.handleSignOut.bind(this)
    }

    handleSignIn() {
        (async () => {
            const cachedUser = await signInAsync()
            this.props.requestPostUser(cachedUser)
           // alert(_authState)
        /*
            const _authState = await AppAuth.authAsync(AUTH_CONFIG);
            if (_authState != null) {
                alert(_authState)
                */
            /*
                await cacheAuthAsync(_authState);
                this.props.loadAuthState(_authState);
                */
                /* push token */
           // }
        })()
    }

    handleSignOut() {
        (async () => {
            //await signOutAsync(this.props.authState)
            //this.props.loadAuthState(null);
        })()
    }

    componentDidMount() {
    }

    render() {
        return (
            <LoginComponent
                handleSignIn = {this.handleSignIn}
                handleSignOut= {this.handleSignOut}
            />
        )
   }
}

function mapStateToProps (state) {
    return {
        cntry: state.baseReducer.cntry,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestPostUser: bindActionCreators(requestPostUser, dispatch),
    };
}

const LoginContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default LoginContainer;

