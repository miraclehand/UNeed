import { Icon } from 'expo'
import React from 'react'
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import TabBarIcon from '../components/TabBarIcon'
import HomeScreen from '../screens/HomeScreen'
import MessagesScreen from '../screens/MessagesScreen'
import ProfileScreen from '../screens/ProfileScreen'
import TopPicksScreen from '../screens/TopPicksScreen'

const Stack = createStackNavigator();

export const HomeStack = (
    <Stack.Navigator>
        <Stack.Screen name='Home' component={HomeScreen} />
    </Stack.Navigator>
)

export const TopPicksStack = (
    <Stack.Navigator>
        <Stack.Screen name='TopPicks' component={TopPicksScreen} />
    </Stack.Navigator>
)

export const MessagesStack = (
    <Stack.Navigator>
        <Stack.Screen name='Messages' component={MessagesScreen} />
    </Stack.Navigator>
)

export const ProfileStack = createStackNavigator(
    <Stack.Navigator>
        <Stack.Screen name='Profile' component={ProfileScreen} />
    </Stack.Navigator>
)

