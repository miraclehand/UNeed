import { Platform } from 'react-native'

export const SimulaComponent = Platform.select({
    web: require('./SimulaComponent.web'),
    android: require('./SimulaComponent.android'),
    ios: require('./SimulaComponent.ios'),
})
