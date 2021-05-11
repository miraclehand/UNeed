import { Platform } from 'react-native'
import { AsyncStorage } from '@react-native-community/async-storage'
import * as AppAuth from 'expo-app-auth';
import { Notifications } from 'expo';
import * as Permissions from 'expo-permissions';
import Constants from 'expo-constants'
import jwtDecoder from 'jwt-decode';

const KEY_AUTH_STATE = 'KEY_AUTH_STATE'
const KEY_PUSH_TOKEN = 'KEY_PUSH_TOKEN'
const KEY_LEVEL      = 'KEY_LEVEL'

export const AUTH_CONFIG = {
    issuer: 'https://accounts.google.com',
    scopes: ['openid', 'profile', 'email'],
    /* This is the CLIENT_ID generated from a Firebase project */
    clientId: Platform.select({
        web:'web',
        android:'536908281748-8p9tp8fh36b2qm15t1n94ukk4vfig3e4.apps.googleusercontent.com',
        ios:'536908281748-8qq0i8214u4r5i5orap99num9lh6oeoc.apps.googleusercontent.com',
    })
};

export async function getCachedUserAsync() {
    const authState = await getCachedAuthAsync()

    if (authState == null) {
        return null
    }

    const pushToken  = JSON.parse(await AsyncStorage.getItem(KEY_PUSH_TOKEN));
    const level      = JSON.parse(await AsyncStorage.getItem(KEY_LEVEL));
    const decodedJwt = jwtDecoder(authState['idToken'])

    return {
        'name'      : decodedJwt['name'],
        'email'     : decodedJwt['email'],
        'pushToken' : JSON.stringify(pushToken),
        'level'     : 0,
    }
}

export async function cacheAuthAsync(authState) {
    return await AsyncStorage.setItem(KEY_AUTH_STATE,JSON.stringify(authState));
}

export async function getCachedAuthAsync() {
    const value = await AsyncStorage.getItem(KEY_AUTH_STATE);
    const authState = JSON.parse(value);

    if (authState) {
        if (checkIfTokenExpired(authState)) {
            return refreshAuthAsync(authState);
        } else {
            return authState;
        }
    }
    return null;
}

export async function cachePushTokenAsync(pushToken) {
    return await AsyncStorage.setItem(KEY_PUSH_TOKEN,JSON.stringify(pushToken));
}

export async function signInAsync() {
    const authState  = await AppAuth.authAsync(AUTH_CONFIG);
    const pushToken  = await registerForPushNotificationsAsync()
    const decodedJwt = jwtDecoder(authState['idToken'])

    await cacheAuthAsync(authState);
    await cachePushTokenAsync(pushToken)

    return {
        'name'      : decodedJwt['name'],
        'email'     : decodedJwt['email'],
        'pushToken' : JSON.stringify(pushToken),
        'level'     : 0,
    }
}

export async function signOutAsync({ accessToken }) {
    try {
        await AppAuth.revokeAsync(AUTH_CONFIG, {
            token: accessToken,
            isClientIdProvided: true,
        });
        await AsyncStorage.removeItem(KEY_AUTH_STATE);
        return null;
    } catch (e) {
        alert(`Failed to revoke token: ${e.message}`);
    }
}

function checkIfTokenExpired({accessTokenExpirationDate}) {
    return new Date(accessTokenExpirationDate) < new Date();
}

async function refreshAuthAsync({refreshToken}) {
    const authState = await AppAuth.refreshAsync(AUTH_CONFIG, refreshToken);
    await cacheAuthAsync(authState);
    return authState;
}


async function registerForPushNotificationsAsync() {
/*
    if (Platform.OS === 'web') {
        return null;
    }
*/
    if (Constants.isDevice) {
        const { status: existingStatus } = await Permissions.getAsync(Permissions.NOTIFICATIONS);
        let finalStatus = existingStatus;
        if (existingStatus !== 'granted') {
            const { status } = await Permissions.askAsync(Permissions.NOTIFICATIONS);
            finalStatus = status;
        }
        if (finalStatus !== 'granted') {
            alert('Failed to get push token for push notification!');
            return null;
        }
        const expoPushToken = await Notifications.getExpoPushTokenAsync();
        return expoPushToken
        //console.log(token);
        //this.setState({ expoPushToken: token });
    } else {
        alert('Must use physical device for Push Notifications');
        return null;
    }
    if (Platform.OS === 'android') {
        Notifications.createChannelAndroidAsync('default', {
            name: 'default',
            sound: true,
            priority: 'max',
            vibrate: [0, 250, 250, 250],
        });
    }
    return null
};
