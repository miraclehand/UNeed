import { Notifications } from 'expo';
import * as Permissions from 'expo-permissions';
import Constants from 'expo-constants'
import { Platform } from 'react-native'

export async function registerForPushNotificationsAsync() {
    if (Platform.OS === 'web') {
        return null;
    }
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

