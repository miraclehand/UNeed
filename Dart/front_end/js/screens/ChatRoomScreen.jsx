import React from 'react';
import ChatRoomContainer from '../containers/ChatRoomContainer';

export class ChatRoomScreen extends React.Component {
    constructor(props) {
        super(props)
        this.handlePress = this.handlePress.bind(this)
    }

    handlePress(watch_id) {
        this.props.navigation.navigate('Chat', { 'watch_id': watch_id, })
    }

    componentDidMount() {
    }

    render () {
        return (
            <ChatRoomContainer handlePress={this.handlePress}/>
        )
    }
}

export default ChatRoomScreen
