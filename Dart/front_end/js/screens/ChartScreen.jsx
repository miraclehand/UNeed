import React from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import ChartContainer from '../containers/ChartContainer';

export class ChartScreen extends React.Component {
    constructor(props) {
        super(props)
    }
    render () {
        return (
            <ChartContainer />
        )
    }
}

export default ChartScreen
