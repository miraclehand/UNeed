import React from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import StatsSimulaContainer from '../containers/StatsSimulaContainer';

export class StatsSimulaScreen extends React.Component {
    constructor(props) {
        super(props)
    }

    render () {
        const { simula } = this.props.route.params

        return (
            <StatsSimulaContainer simula = {simula} />
        )
    }
}

export default StatsSimulaScreen
