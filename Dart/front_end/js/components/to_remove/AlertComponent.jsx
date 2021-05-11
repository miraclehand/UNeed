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
                    console.log(r.badge_count)
                    return (
                      <ListItem
                          key={r.watch_id}
                          bottomDivider
                          onPress = {() => this.handlePress(r.watch_id)}
                      >
                        <ListItem.Content>
                            <ListItem.Title> {r.watch_name} </ListItem.Title>
                            <ListItem.Subtitle> {r.last_disc_label} </ListItem.Subtitle>
                        </ListItem.Content>
                      </ListItem>
                  )
                })}
            </ScrollView>
        )
    }
}

export default AlertComponent;
