import { Platform } from 'react-native'

export const CreateSimulaComponent = Platform.select({
    web: require('./CreateSimulaComponent.web'),
    android: require('./CreateSimulaComponent.android'),
    ios: require('./CreateSimulaComponent.ios'),
})
