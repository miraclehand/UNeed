import React from 'react';
import { connect } from 'react-redux'
import { Text } from 'react-native'
import { bindActionCreators } from 'redux';
import { requestAlertRoom } from '../actions/AlertRoomAction';
import AlertRoomComponent from '../components/AlertRoomComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)
    }

    componentDidMount() {
        const { os, db, email, token, cntry, watch_id } = this.props

        this.props.requestAlertRoom(os, db, email, token, cntry, watch_id);
    }

    render() {
        return <AlertRoomComponent discs = {this.props.discs} />
   }
}

function mapStateToProps (state) {
    return {
        email: state.userReducer.email,
        cntry: state.baseReducer.cntry,
        os: state.baseReducer.os,
        db: state.dbReducer.db,
        discs: state.alertRoomReducer.discs,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestAlertRoom : bindActionCreators(requestAlertRoom, dispatch),
    };
}

const AlertRoomContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default AlertRoomContainer;

