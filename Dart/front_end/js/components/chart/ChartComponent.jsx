import { Platform } from 'react-native'

export const ChartComponent = Platform.select({
    web: require('./ChartComponent.web'),
    android: require('./ChartComponent.android'),
    ios: require('./ChartComponent.ios'),
})
