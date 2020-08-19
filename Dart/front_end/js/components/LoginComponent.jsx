import React from 'react';
import { StyleSheet, Text, View, Button, TouchableOpacity } from 'react-native'
import { SocialIcon } from 'react-native-elements'

class LoginComponent extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <View style={styles.container}>
                <TouchableOpacity onPress={this.props.handleSignIn} >
                    <SocialIcon
                        title='Sign In With Google'
                        button
                        type='google'
                    />
                </TouchableOpacity>
            </View>
        )
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
    },
    button: {
        flex: 1,
    },
})

export default LoginComponent;
