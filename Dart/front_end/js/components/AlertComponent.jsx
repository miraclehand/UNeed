import React from 'react';
import { ScrollView } from 'react-native'
import { Button, ListItem } from 'react-native-elements'
import Constants from 'expo-constants';
import { Avatar, Badge, Icon, withBadge } from 'react-native-elements'

class AlertComponent extends React.Component {
    constructor(props) {
        super(props);
        this.handlePress = this.handlePress.bind(this)
    }

    handlePress(watch_id) {
        this.props.handlePress(watch_id)
    }

    render() {
        const { rooms } = this.props
        const avatar_url =  'https://s3.amazonaws.com/uifaces/faces/twitter/ladylexy/128.jpg'

        return (
                <ScrollView>
                    { rooms && rooms.map((r, i) => {
                        return (
                          <ListItem
                              key={r.watch_id}
                              leftAvatar={{ source: { uri: avatar_url } }}
                              title={r.watch_name}
                              subtitle={r.last_disc_label}
                              bottomDivider
                              badge={{ value: 3, status:'error' }}
                              onPress = {() => this.handlePress(r.watch_id)}
                          />
                          )
                    })}
                </ScrollView>
        )
    }
}

export default AlertComponent;
