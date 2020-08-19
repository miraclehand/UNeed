import React from 'react';
import { Platform } from 'react-native'
import { ScrollView } from 'react-native'
import { Button, ListItem } from 'react-native-elements'
import Constants from 'expo-constants';
import { GiftedChat } from 'react-native-gifted-chat'
import ChatMessage from './ChatMessage'
import ChatExample from './ChatExample'
/*
https://github.com/FaridSafi/react-native-gifted-chat/tree/656a700106923e7e92a5a4644e0729fef35f0a30/example-slack-message
*/
import emojiUtils from 'emoji-utils'

class AlertRoomComponent extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            messages: [
                {
                    _id: 1,
                    text: 'Hello developer',
                    createdAt: new Date(),
                    image:'http://www.prostj.com/_images/m_0427_1.jpg',
                    user: {
                        _id: 2,
                        name: 'React Native',
                        avatar: 'https://facebook.github.io/react/img/logo_og.png',
                    },
                },
            ],
        }
        this.onSend = this.onSend.bind(this)
        this.handlePress = this.handlePress.bind(this)
        this.renderMessage = this.renderMessage.bind(this)

    }

    onSend(messages = []) {
        this.setState((previousState) => ({
            messages: GiftedChat.append(previousState.messages, messages),
        }));
    }

    handlePress(watch_list_id) {
    }

    renderMessage(props) {
        const {
          currentMessage: { text: currText },
        } = props

        let messageTextStyle

        // Make "pure emoji" messages much bigger than plain text.
        if (currText && emojiUtils.isPureEmojiString(currText)) {
          messageTextStyle = {
            fontSize: 28,
            // Emoji get clipped if lineHeight isn't increased; make it consistent across platforms.
            lineHeight: Platform.OS === 'android' ? 34 : 30,
          }
        }
        return <ChatMessage {...props} messageTextStyle={messageTextStyle} />
    }

    render() {
        const { messages } = this.props
        const avatar_url =  'https://s3.amazonaws.com/uifaces/faces/twitter/ladylexy/128.jpg'
        console.log('render chat')
        return <ChatExample />

        return (
            <GiftedChat
                messages={this.props.messages}
                onSend={(messages) => this.onSend(messages)}
                user={{
                    _id: 1,
                }}
            />
        );

        return (
            <GiftedChat
                messages={this.props.messages}
                onSend={(messages) => this.onSend(messages)}
                user={{
                    _id: 1,
                }}
                renderMessage={this.renderMessage}
            />
        );
        return (
                <ScrollView>
                    { messages && messages.map((r, i) => {
                        return (
                          <ListItem
                              key={i}
                              leftAvatar={{ source: { uri: avatar_url } }}
                              title={r.title}
                              subtitle={r.content}
                              bottomDivider
                              onPress = {() => this.handlePress(r.title)}
                          />
                          )
                    })}
                </ScrollView>
        )
    }
}

export default AlertRoomComponent;
