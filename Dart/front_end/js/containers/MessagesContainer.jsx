import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestMessages, requestMessage } from '../actions/MessagesAction';
import MessagesComponent from '../components/MessagesComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)
    }

    componentDidMount() {
        const {email, token, cntry } = this.props

        this.props.requestMessages(email, token, cntry, '', '');
    }

    render() {
        const { messages } = this.props

        return <MessagesComponent messages={messages} />
   }
}

function mapStateToProps (state) {
    return {
        email: state.userReducer.email,
        cntry: state.baseReducer.cntry,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestMessage : bindActionCreators(requestMessage,  dispatch),
        requestMessages: bindActionCreators(requestMessages, dispatch),
    };
}

const MessagesContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default MessagesContainer;

