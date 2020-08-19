import React from 'react';
import { SafeAreaView, ScrollView, StyleSheet } from 'react-native'
import { Button, ListItem } from 'react-native-elements'
import Constants from 'expo-constants';

class KeywordsComponent extends React.Component {
    constructor(props) {
        super(props);
        this.handlePress = this.handlePress.bind(this)

    }
    componentDidMount() {
    }

    handlePress() {
        console.log('handlePress2')
    }

    render() {
        const { keywords } = this.props
        const avatar_url =  'https://s3.amazonaws.com/uifaces/faces/twitter/ladylexy/128.jpg'

        /*
            <SafeAreaView>
            </SafeAreaView>
        */
        return (
                <ScrollView>
                    { keywords && keywords.map((k, i) => {
                        return (
                          <ListItem
                              key={i}
                              leftAvatar={{ source: { uri: avatar_url } }}
                              title={k.keyword}
                              subtitle={k.keyword}
                              bottomDivider
                              onPress = {this.handlePress}
                          />
                          )
                    })}
                </ScrollView>
        )
    }
    
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: Constants.statusBarHeight,
  },
  item: {
    backgroundColor: '#f9c2ff',
    padding: 20,
    marginVertical: 8,
    marginHorizontal: 16,
  },
  title: {
    fontSize: 32,
  },
});
export default KeywordsComponent;

