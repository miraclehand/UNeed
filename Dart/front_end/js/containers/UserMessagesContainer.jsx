import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestUserMessages } from '../actions/UserMessageAction';
import UserMessagesComponent from '../components/UserMessagesComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)
    }

    componentDidMount() {
        const {email, token, cntry } = this.props

        this.props.requestUserMessages(email, token, cntry);
    }

    render() {
        const { messages } = this.props

        return <UserMessagesComponent messages={messages} />
   }
}

function mapStateToProps (state) {
    return {
        email: state.userReducer.email,
        cntry: state.baseReducer.cntry,
        messages: state.userMessagesReducer.messages,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestUserMessages: bindActionCreators(requestUserMessages, dispatch),
    };
}

const MessagesContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default MessagesContainer;

