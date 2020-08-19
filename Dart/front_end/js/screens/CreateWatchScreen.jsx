import React from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import CreateWatchContainer from '../containers/CreateWatchContainer';

export class CreateWatchScreen extends React.Component {
    constructor(props) {
        super(props)
    }

    render () {
        return (
            <CreateWatchContainer />
        )
    }
}

export default CreateWatchScreen
