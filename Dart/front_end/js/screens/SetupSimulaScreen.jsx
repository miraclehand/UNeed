import React from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import SetupSimulaContainer from '../containers/SetupSimulaContainer';

export class SetupSimulaScreen extends React.Component {
    constructor(props) {
        super(props)
    }

    render () {
        return (
            <SetupSimulaContainer />
        )
    }
}

export default SetupSimulaScreen
