import { Platform } from 'react-native'

export const AuthScreen = Platform.select({
    web: require('./AuthScreen.web'),
    android: require('./AuthScreen.android'),
    ios: require('./AuthScreen.ios'),
})

