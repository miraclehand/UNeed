import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import Modal from '@material-ui/core/Modal';
import SignInComponent from '../components/SignInComponent';
import AlertComponent from '../components/AlertComponent';
import { loadAuth, requestSignIn } from "../actions/AuthAction";

class Connected extends React.Component {
    constructor(props) {
        super(props)
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    componentDidMount() {
        this.props.loadAuth()
    }

    handleSubmit(username, password) {
        this.props.requestSignIn(username, password)
    }

    render () {
        const { handleSubmit } = this
        const { token, failed } = this.props
        const enabled = token ? false : true

        return (
            <Modal open={enabled}>
                <AlertComponent component = {
                    <SignInComponent
                        failed={failed}
                        handleSubmit={handleSubmit}/>
                }/>
            </Modal>
        )
    }
};

function mapStateToProps (state) {
    return {
        failed: state.authReducer.failed,
        token: state.authReducer.token,
        username: state.authReducer.username,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        loadAuth: bindActionCreators(loadAuth, dispatch),
        requestSignIn: bindActionCreators(requestSignIn, dispatch),
    };
}

const SignInContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default SignInContainer;
