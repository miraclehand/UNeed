import React from 'react';
import { View, Text, Button, TouchableOpacity } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import HeaderRight from './HeaderRight'

/*
import { Updates, Constants } from 'expo';
*/

import HomeTabs from './HomeTabNavigator';
import CreateWatchScreen from '../screens/CreateWatchScreen'
import SetupWatchScreen from '../screens/SetupWatchScreen'

import AlertRoomScreen from '../screens/AlertRoomScreen'

import CreateSimulaScreen from '../screens/CreateSimulaScreen'
import SetupSimulaScreen from '../screens/SetupSimulaScreen'
import StatsSimulaScreen from '../screens/StatsSimulaScreen'

const Stack = createStackNavigator();

import WatchScreen from '../screens/WatchScreen'
import AlertScreen from '../screens/AlertScreen'
import SimulaScreen from '../screens/SimulaScreen'

//import { WatchStackScreen, AlertStackScreen, SimulaStackScreen } from './StackNavigator'

import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
const Tab = createBottomTabNavigator();

function getRouteName(route) {
    if (route.state) {
        return route.state.routes[route.state.index].name
    }
    if (route.name === 'Home') return 'Watch'
    return route.name
}

function getHeaderTitle(route) {
    const route_name = getRouteName(route)

    return <Text style={{fontWeight:'bold'}}> { route_name } </Text>
}

function getHeaderRight(route, navigation) {
    const route_name = getRouteName(route)

    return <HeaderRight route_name = {route_name} navigation = {navigation} />
}

class AppNavigator extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            showUpdate: false
        }

        this.doUpdate = this.doUpdate.bind(this)
    }

    componentDidMount() {
    /*
        Updates.checkForUpdateAsync().then(update => {
        if (update.isAvailable) {
            this.setState({showUpdate: true});
        }
        });
        */
    }

    doUpdate() {
    /*
        Updates.reload();
        */
    }

    render() {
        return (
            <NavigationContainer>
                <Stack.Navigator
                    screenOptions = {({ route, navigation }) => ({
                        headerTitle: getHeaderTitle(route),
                        headerRight: ()=>getHeaderRight(route,navigation),
                    })}
                >
                    <Stack.Screen name='Home' component={HomeTabs} />

                    <Stack.Screen name='AlertRoom'   component={AlertRoomScreen} />
                    <Stack.Screen name='CreateWatch' component={CreateWatchScreen} />
                    <Stack.Screen name='SetupWatch'  component={SetupWatchScreen} />
                    <Stack.Screen name='CreateSimula'component={CreateSimulaScreen} />
                    <Stack.Screen name='SetupSimula' component={SetupSimulaScreen} />
                    <Stack.Screen name='StatsSimula' component={StatsSimulaScreen} />
                </Stack.Navigator>
            </NavigationContainer>
        )
    }
}

export default AppNavigator
