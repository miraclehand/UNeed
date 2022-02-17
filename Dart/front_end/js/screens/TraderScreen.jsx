import React from 'react';
import TraderContainer from '../containers/TraderContainer';
import { View, Button, Text } from 'react-native';

export class TraderScreen extends React.Component {
    constructor(props) {
        super(props)
    }
    render () {
        return (
            <TraderContainer /> 
        )
    }
}

export default TraderScreen
