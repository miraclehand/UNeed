import React from 'react';
import ChatContainer from '../containers/ChatContainer';

export class ChatScreen extends React.Component {
    constructor(props) {
        super(props)
    }

    render () {
        const { watch_id } = this.props.route.params
        return (
            <ChatContainer watch_id ={watch_id} />
        )
    }
}

export default ChatScreen
