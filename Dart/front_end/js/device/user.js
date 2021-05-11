import { Platform } from 'react-native'
import Constants from 'expo-constants'
//import * as Permissions from 'expo-permissions';
//import { Notifications } from 'expo';
import * as Notifications from 'expo-notifications';
import * as SecureStore from 'expo-secure-store';
//import jwtDecoder from 'jwt-decode';

const KEY_AUTH_STATE = 'KEY_AUTH_STATE'
const KEY_PUSH_TOKEN = 'KEY_PUSH_TOKEN'

export async function cacheAuthState() {
    const authState = JSON.parse(await cacheAuthAsync())
    
    if (authState === null) {
        return {
            'name'      : '',
            'email'     : '',
            'level'     : '',
        }
    }
    return {
        'name'      : authState['name'],
        'email'     : authState['email'],
        'level'     : authState['level'],
    }
}

export async function cacheAuthAsync() {
    const authState = SecureStore.getItemAsync(KEY_AUTH_STATE);

    if (authState) {
        return authState;
    /*
        if (checkIfTokenExpired(authState)) {
            return refreshAuthAsync(authState);
        } else {
            return authState;
        }
        */
    }
    return null;
}

function checkIfTokenExpired({accessTokenExpirationDate}) {
    return new Date(accessTokenExpirationDate) < new Date();
}

async function refreshAuthAsync({refreshToken}) {
    const authState = await AppAuth.refreshAsync(AUTH_CONFIG, refreshToken);
    await cacheAuthAsync(authState);
    return authState;
}

/*
export async function cacheUserAsync() {
    const pushToken = JSON.parse(await cachePushTokenAsync())
    const authState = JSON.parse(await cacheAuthAsync())
    let name = ''
    let email = ''
    if (authState != null) {
        //const decodedJwt = jwtDecoder(authState['idToken'])
        name  = authState['name']
        email = authState['email']
    }
    //name  = 'yepark'
    //email = 'miraclehand@gmail.com'

    return {
        'name'      : name,
        'email'     : email,
        'pushToken' : JSON.stringify(pushToken),
        'level'     : 0,
    }
}
*/


export async function saveAuthState(authState) {
    await SecureStore.setItemAsync(KEY_AUTH_STATE, JSON.stringify(authState));
}

/*
async function cachePushTokenAsync() {
    let pushToken = await SecureStore.getItemAsync(KEY_PUSH_TOKEN);

    if (!pushToken) {
        pushToken = registerForPushNotificationsAsync()

        await SecureStore.setItemAsync(KEY_PUSH_TOKEN, JSON.stringify(pushToken));
    }
    return pushToken
}
*/

/*
export async function registerForPushNotificationsAsync() {
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
*/

export async function registerForPushNotificationsAsync() {
    let token;
    if (Constants.isDevice) {
        const { status: existingStatus } = await Notifications.getPermissionsAsync();
        let finalStatus = existingStatus;
        if (existingStatus !== 'granted') {
            const { status } = await Notifications.requestPermissionsAsync();
            finalStatus = status;
        }
        if (finalStatus !== 'granted') {
            alert('Failed to get push token for push notification!');
            return;
        }
        token = (await Notifications.getExpoPushTokenAsync()).data;
        console.log(token);
    } else {
        alert('Must use physical device for Push Notifications');
    }

    if (Platform.OS === 'android') {
        Notifications.setNotificationChannelAsync('default', {
            name: 'default',
            importance: Notifications.AndroidImportance.MAX,
            vibrationPattern: [0, 250, 250, 250],
            lightColor: '#FF231F7C',
        });
    }

    return token;
}

export async function deleteAuthState() {
    await SecureStore.deleteItemAsync(KEY_AUTH_STATE);
}


/*

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
*/


