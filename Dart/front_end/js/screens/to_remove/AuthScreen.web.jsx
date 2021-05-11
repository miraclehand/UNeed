import React, { useEffect, useState } from 'react';
import { AsyncStorage, Button, StyleSheet, Text, View } from 'react-native';
import * as AppAuth from 'expo-app-auth';

export default class AuthScreen extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            authState :''
        }
    }

    componentDidMount() {
        (async () => {
            let cachedAuth = await getCachedAuthAsync();
            if (cachedAuth && !authState) {
                setAuthState(cachedAuth);
            }
        })();
    }

    render() {
        console.log('web')
        return (
            <>
            </>
        )
    }
}
