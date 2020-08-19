import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestAlert } from '../actions/AlertAction';
import AlertComponent from '../components/AlertComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)
        this.handlePress = this.handlePress.bind(this)
    }

    handlePress(watch_id) {
        this.props.handlePress(watch_id)
    }

    componentDidMount() {
        const { email, token, cntry } = this.props

        this.props.requestAlert(email, token, cntry);
    }

    render() {
        return <AlertComponent rooms = {this.props.rooms} handlePress={this.handlePress} />
   }
}

function mapStateToProps (state) {
    return {
        email: state.userReducer.email,
        cntry: state.baseReducer.cntry,
        rooms: state.alertReducer.rooms,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestAlert : bindActionCreators(requestAlert, dispatch),
    };
}

const AlertContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default AlertContainer;

