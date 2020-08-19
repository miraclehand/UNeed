import React from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import SetupWatchContainer from '../containers/SetupWatchContainer';

export class SetupWatchScreen extends React.Component {
    constructor(props) {
        super(props)
    }

    render () {
        return (
            <SetupWatchContainer />
        )
    }
}

export default SetupWatchScreen
