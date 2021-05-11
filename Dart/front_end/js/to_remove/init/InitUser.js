/*
import React from 'react';
import * as WebBrowser from 'expo-web-browser';
import * as Google from 'expo-auth-session/providers/google';
import { Text, Button } from 'react-native';
import { useDispatch, useSelector } from 'react-redux'

WebBrowser.maybeCompleteAuthSession();

const cacheUser = () => {
    const dispatch = useDispatch();
    const [request, response, promptAsync] = Google.useAuthRequest({
        expoClientId: '536908281748-teiiu4iu80p3romorrcj90pivgkbvkev.apps.googleusercontent.com',
        iosClientId: '536908281748-n5190ntbccf3gklu3f7h4im226edbjpc.apps.googleusercontent.com',
        androidClientId: '536908281748-jjtno1de0mpknm2nohh594o7q2oiasa5.apps.googleusercontent.com',
        webClientId: '536908281748-iut4mcukcfn8agn19iu2ioiqpfu2gces.apps.googleusercontent.com'
    });
    React.useEffect(() => {
        if (response?.type === 'success') {
            const { authentication } = response;
            dispatch(authentication)
        }
    }, [response]);

}
*/



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

// REMOVEME
function getIdToken2(authState) {
    if (authState == null) {
        return null
    }
    /*
    alert( JSON.parse(authState))
    alert( JSON.parse(authState)['idToken'])

    const authState2  = JSON.stringify(authState)
    const p = JSON.parse(authState2)
    alert(p['idToken'])
    */
    //alert(authState['idToken'])
    //const idToken    = JSON.parse(authState)['idToken']
    //const idToken    = JSON.stringify(authState)['idToken']
    const authState2  = JSON.stringify(authState)
    //alert(authState2)
    //alert(idToken)
    //alert('case1)' + authState)                  // case1 OK
    //alert(JSON.parse(authState))                 // case2 (fail)
    //alert('case2)' + JSON.parse(authState))    // case2 (fail)
    //alert('case3)' + JSON.stringify(authState))    // case3 OK
    //alert('case4)' + authState['idToken']) // case4 OK)
    //alert('case5)' + JSON.parse(authState)['idToken']) //case 5 (fail)
    //alert('case6)' + JSON.stringify(authState)['idToken']) // case6(undefined)

 const token = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZG1pbkB0LW1vbmV0LmNvbSIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwidXNlcklkIjoiODNiYmEzNDAtMDI3ZC0xMWU4LWI4ZmEtYWY1YjU0OTEyMDA0IiwiZmlyc3ROYW1lIjoi7ISx64Ko7IucIiwibGFzdE5hbWUiOiLqtIDrpqzsnpAiLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiMzkwMTNjNzAtMDI3ZC0xMWU4LWI4ZmEtYWY1YjU0OTEyMDA0IiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCIsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNTM1OTU1NDE2LCJleHAiOjM2NzU5NTU0MTZ9.N1Ms0LA7WtOel1pg6lTMRNDJosY3qfR6Q4SVuAUwmDPmTj4uYnKU0B-9Wdlqmg4HQRUXa23edOTU-TnAxfBoyg'

    const jwt_decode = require('jwt-decode');
    const idToken    = authState['idToken']
    const jwtBody    = idToken.split('.')[1];
    const aa = jwt_decode(token)
    //alert(JSON.stringify(aa))
    //alert('aa)' + typeof(aa))
    //alert('jwtBody)' + typeof(jwtBody))
    alert(jwtBody)
    const bb = jwt_decode(jwtBody)
    alert(JSON.stringify(bb))


    //const base64     = jwtBody.replace('-', '+').replace('_', '/');
    //const p0 = JSON.parse(atob(idToken.split('.')[1]));
    //const p1 = Buffer.from(base64, 'base64')
    const p1 = Buffer.from(base64).toString('base64')
    alert(p1)
    const p2 = Buffer.from(base64, 'base64').toString('binary')
    alert('p2)' + p2)
    const decodedJwt = JSON.parse(Buffer.from(base64, 'base64').toString('binary'));
    alert('decodedJwt)' + decodedJwt)
    return decodedJwt
}

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
