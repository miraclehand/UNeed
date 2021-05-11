import React from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import StatsSimulaContainer from '../containers/StatsSimulaContainer';

export class StatsSimulaScreen extends React.Component {
    constructor(props) {
        super(props)
        this.handlePress = this.handlePress.bind(this)
    }

    handlePress(stock_code) {
        this.props.navigation.navigate('CandleChart', {
            'stock_code': stock_code,
        })
    }

    render () {
        const { simula } = this.props.route.params

        return (
            <StatsSimulaContainer
                simula = {simula}
                handlePress={this.handlePress}
            />
        )
    }
}

export default StatsSimulaScreen
