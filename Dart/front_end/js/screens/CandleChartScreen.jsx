import React from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import CandleChartContainer from '../containers/CandleChartContainer';

export class ChartScreen extends React.Component {
    constructor(props) {
        super(props)
    }
    render () {
        const { stock_code } = this.props.route.params
        console.log(stock_code)
        return (
            <CandleChartContainer stock_code = {stock_code} />
        )
    }
}

export default ChartScreen
