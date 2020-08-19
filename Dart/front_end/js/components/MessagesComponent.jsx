import React from 'react';
import { ScrollView } from 'react-native'
import { Button, ListItem } from 'react-native-elements'
import Constants from 'expo-constants';

class MessagesComponent extends React.Component {
    constructor(props) {
        super(props);
        this.handlePress = this.handlePress.bind(this)
    }

    handlePress() {
        this.props.handlePress(this.state.text)
    }

    render() {
    const { messages } = this.props
 const avatar_url =  'https://s3.amazonaws.com/uifaces/faces/twitter/ladylexy/128.jpg'

        return (
                <ScrollView>
                    { messages && messages.map((k, i) => {
                        return (
                          <ListItem
                              key={i}
                              leftAvatar={{ source: { uri: avatar_url } }}
                              title={k.corp.corp_name}
                              subtitle={k.rcept_dt + ' ' + k.reg_time + ' ' + k.report_nm}
                              bottomDivider
                              onPress = {this.handlePress}
                          />
                          )
                    })}
                </ScrollView>
        )
    }
}

export default MessagesComponent;
