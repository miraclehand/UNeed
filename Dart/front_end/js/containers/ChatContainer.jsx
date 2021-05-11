import React from 'react';
import { connect } from 'react-redux'
import { Text } from 'react-native'
import { bindActionCreators } from 'redux';
import { requestChat } from '../actions/ChatAction';
import { updateBadge } from '../actions/ChatRoomAction';
import ChatComponent from '../components/ChatComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)
    }

    componentDidMount() {
        const { os, db, email, token, cntry, watch_id, chats } = this.props
        
        this.props.requestChat(os, db, email, token, cntry, watch_id);
        this.props.updateBadge(os, db, watch_id, 0);
    }

    render() {
        return <ChatComponent chats = {this.props.chats} />
   }
}

function mapStateToProps (state) {
    return {
        email: state.userReducer.email,
        cntry: state.baseReducer.cntry,
        os: state.baseReducer.os,
        db: state.dbReducer.db,
        chats: state.chatReducer.chats,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestChat : bindActionCreators(requestChat, dispatch),
        updateBadge : bindActionCreators(updateBadge, dispatch),
        
    };
}

const ChatContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default ChatContainer;

