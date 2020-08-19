import React from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import CreateSimulaContainer from '../containers/CreateSimulaContainer';

export class CreateSimulaScreen extends React.Component {
    constructor(props) {
        super(props)
    }
    render () {
        return (
            <CreateSimulaContainer />
        )
    }
}

export default CreateSimulaScreen
