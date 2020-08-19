import React from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import SimulaContainer from '../containers/SimulaContainer';

export class SimulaScreen extends React.Component {
    constructor(props) {
        super(props)
        this.handlePress = this.handlePress.bind(this)
    }

    handlePress(simula) {
        this.props.navigation.navigate('StatsSimula', { 'simula': simula })
    }

    render () {
        return (
            <SimulaContainer handlePress={this.handlePress} />
        )
    }
}

export default SimulaScreen
