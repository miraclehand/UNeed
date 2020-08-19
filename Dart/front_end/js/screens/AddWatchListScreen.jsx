import React from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import AddWatchListContainer from '../containers/AddWatchListContainer';

export class AddWatchListScreen extends React.Component {
    constructor(props) {
        super(props)
    }
    render () {
        return (
            <AddWatchListContainer />
        )
    }
}

export default AddWatchListScreen
