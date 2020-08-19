import React from 'react';
import WatchContainer from '../containers/WatchContainer';
import { View, Button } from 'react-native';

export class WatchScreen extends React.Component {
    constructor(props) {
        super(props)
    }
    render () {
        return (
            <WatchContainer /> 
        )
    }
}

export default WatchScreen
