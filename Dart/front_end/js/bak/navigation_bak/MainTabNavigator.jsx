import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { MaterialCommunityIcons, MaterialIcons } from 'react-native-vector-icons';

import WatchListScreen from '../screens/WatchListScreen'
import AlertScreen from '../screens/AlertScreen'

import SimulaScreen from '../screens/SimulaScreen'
import AuthScreen from '../screens/AuthScreen'

import { View, Text, Button, TouchableOpacity } from 'react-native';
import { Avatar, Badge, Icon, withBadge } from 'react-native-elements'


const Tab = createBottomTabNavigator();
/*
https://snack.expo.io/?platform=android&name=Screen%20options%20resolution%20%7C%20React%20Navigation&dependencies=%40react-native-community%2Fmasked-view%40%5E0.1.1%2C%40react-navigation%2Fnative%40%5E5.0.5%2C%40react-navigation%2Fbottom-tabs%40%5E5.0.5%2C%40react-navigation%2Fdrawer%40%5E5.0.5%2C%40react-navigation%2Fmaterial-bottom-tabs%40%5E5.0.5%2C%40react-navigation%2Fmaterial-top-tabs%40%5E5.0.5%2C%40react-navigation%2Fstack%40%5E5.0.5%2Creact-native-gesture-handler%401.5.2%2Creact-native-reanimated%401.4.0%2Creact-native-safe-area-context%400.6.0%2Creact-native-screens%402.0.0-alpha.12&sourceUrl=https%3A%2F%2Freactnavigation.org%2Fexamples%2F5.x%2Ftab-based-navigation-badges.js
*/

class MainTabs extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <>
            <Tab.Navigator>
                <Tab.Screen name='WatchList' component={WatchListScreen}
                    options = {{
                        tabBarIcon: ({ color, size }) => (
                            <MaterialCommunityIcons name="star-outline" color={color} size={size} />
                        ),
                    }}
                />
                <Tab.Screen name='Alert' component={AlertScreen}
                    options = {{
                        tabBarIcon: ({ color, size }) => (
                            <>
                            <MaterialIcons name="chat-bubble-outline" color={color} size={size} />
                             { 3 &&
                             <Badge value={3} status="error" containerStyle={{position:'absolute', top:3, left:17}} />
                             }
                            </>
                        ),
                    }}
                />
                <Tab.Screen name='Simula' component={SimulaScreen}
                    options = {{
                        tabBarIcon: ({ color, size }) => (
                            <MaterialCommunityIcons name="filter-outline" color={color} size={size} />
                        ),
                    }}
                />
                <Tab.Screen name='Auth' component={AuthScreen}
                    options = {{
                        tabBarIcon: ({ color, size }) => (
                            <MaterialCommunityIcons name="shield-search" color={color} size={size} />
                        ),
                    }}
                />
            </Tab.Navigator>
            </>
        )
    }
}

export default MainTabs
