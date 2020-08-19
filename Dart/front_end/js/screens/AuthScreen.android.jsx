import React, { useEffect, useState } from 'react';
import { AsyncStorage, Button, StyleSheet, Text, View } from 'react-native';
import * as AppAuth from 'expo-app-auth';

const config = {
    issuer: 'https://accounts.google.com',
    scopes: ['openid', 'profile'],
    /* This is the CLIENT_ID generated from a Firebase project */
    /* TESET
    clientId: '603386649315-vp4revvrcgrcjme51ebuhbkbspl048l9.apps.googleusercontent.com',
    */
    clientId: '536908281748-mv9m95q5qm5oo5389b4bokscidbsdbc3.apps.googleusercontent.com',
};

const StorageKey = '@MyApp:CustomGoogleOAuthKey';

export default class AuthScreen extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            authState :null
        }
        this.signInAsync = this.signInAsync.bind(this)
        this.cacheAuthAsync = this.cacheAuthAsync.bind(this)
        this.getCachedAuthAsync = this.getCachedAuthAsync.bind(this)
        this.checkIfTokenExpired = this.checkIfTokenExpired.bind(this)
        this.refreshAuthAsync = this.refreshAuthAsync.bind(this)
    }

    async componentDidMount() {
        const cachedAuth = await getCachedAuthAsync();
        if (cachedAuth && !this.state.authState) {
            this.setState({authState:cachedAuth})
        }
    }

    async cacheAuthAsync(authState) {
        return await AsyncStorage.setItem(StorageKey, JSON.stringify(authState));
    }

    async signInAsync() {
        let authState = await AppAuth.authAsync(config);
        await cacheAuthAsync(authState);
        console.log('signInAsync', authState);
        this.setState({authState:authState})
        return authState;
    }

    async getCachedAuthAsync() {
        let value = await AsyncStorage.getItem(StorageKey);
        let authState = JSON.parse(value);
        console.log('getCachedAuthAsync', authState);
        if (authState) {
            if (checkIfTokenExpired(authState)) {
                return refreshAuthAsync(authState);
            } else {
                return authState;
            }
        }
        return null;
    }

    checkIfTokenExpired(accessTokenExpirationDate) {
        return new Date(accessTokenExpirationDate) < new Date();
    }

    async refreshAuthAsync(refreshToken) {
        let authState = await AppAuth.refreshAsync(config, refreshToken);
        console.log('refreshAuth', authState);
        await cacheAuthAsync(authState);
        return authState;
    }

    async signOutAsync(accessToken) {
        try {
            await AppAuth.revokeAsync(config, {
                token: accessToken,
                isClientIdProvided: true,
            });
            await AsyncStorage.removeItem(StorageKey);
            this.setState({authState:null})
            return null;
        } catch (e) {
            alert(`Failed to revoke token: ${e.message}`);
        }
    }

    render() {
        return (
            <View>
              <Text>Expo AppAuth Example2</Text>
              <Button
                title="Sign In with Google "
                onPress={this.signInAsync}
              />
              <Button
                title="Sign Out "
                onPress={this.signOutAsync}
              />
              <Text>authState:{this.state.authState}</Text>
            </View>
        )
    }
}
