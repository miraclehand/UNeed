import React from 'react';
import BalanceContainer from '../containers/BalanceContainer';
import { View, Button, Text } from 'react-native';

export class BalanceScreen extends React.Component {
    constructor(props) {
        super(props)
    }
    render () {
        return (
            <BalanceContainer /> 
        )
    }
}

export default BalanceScreen
