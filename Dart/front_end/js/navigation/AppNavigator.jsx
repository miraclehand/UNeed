import React, { useState } from 'react';
import { Text } from 'react-native';
import { useDispatch } from 'react-redux';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { getFocusedRouteNameFromRoute } from '@react-navigation/native';

import HeaderRight from './HeaderRight'

import { Updates } from 'expo';

import HomeTabs from './HomeTabNavigator';
import CreateWatchScreen from '../screens/CreateWatchScreen'
import SetupWatchScreen from '../screens/SetupWatchScreen'

import ChatScreen from '../screens/ChatScreen'
import CandleChartScreen from '../screens/CandleChartScreen'

import CreateSimulaScreen from '../screens/CreateSimulaScreen'
import SetupSimulaScreen from '../screens/SetupSimulaScreen'
import StatsSimulaScreen from '../screens/StatsSimulaScreen'
import { changeCntry, setNavigation } from '../actions/BaseAction'

const Stack = createStackNavigator();

//import WatchScreen from '../screens/WatchScreen'
//import AlertScreen from '../screens/AlertScreen'
//import SimulaScreen from '../screens/SimulaScreen'

//import { WatchStackScreen, AlertStackScreen, SimulaStackScreen } from './StackNavigator'

import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
const Tab = createBottomTabNavigator();

function getRouteName(route) {
    let routeName = ''

    if (route.name === 'Home') {
        routeName = getFocusedRouteNameFromRoute(route) ?? 'Watch';
    }
    else {
        routeName = route.name
    }
    return routeName
}

function getHeaderTitle(route) {
    const routeName = getRouteName(route)

    return <Text style={{fontWeight:'bold'}}> {routeName} </Text>
}

function getHeaderRight(route, navigation) {
    const routeName = getRouteName(route)

    return <HeaderRight route_name = {routeName} navigation = {navigation} />
}

const AppNavigator = (props) => {
    const [showUpdate, setShowUpdate] = useState(false);
    const navigationRef = React.useRef(null);
    //const [initialState, setInitialState] = useState();
    const dispatch = useDispatch();

    const doUpdate = () => {
        //Updates.reload();
    }

    React.useEffect(() => {
        /*
        Updates.checkForUpdateAsync().then(update => {
            if (update.isAvailable) {
                setShowUpdate(true);
            }
        });
        */
    }, [])

    React.useEffect(() => {
        dispatch(setNavigation(navigationRef)) 
    }, [navigationRef])

    return (
        <NavigationContainer
            ref = {navigationRef}
        >
            <Stack.Navigator
                screenOptions = {({ route, navigation }) => ({
                    headerTitle: getHeaderTitle(route),
                    headerRight: ()=>getHeaderRight(route,navigation),
                })}
            >
              <Stack.Screen name='Home' component={HomeTabs} />
              <Stack.Screen name='Chat'   component={ChatScreen} />
              <Stack.Screen name='CreateWatch' component={CreateWatchScreen} />
              <Stack.Screen name='SetupWatch'  component={SetupWatchScreen} />
              <Stack.Screen name='CreateSimula'component={CreateSimulaScreen} />
              <Stack.Screen name='SetupSimula' component={SetupSimulaScreen} />
              <Stack.Screen name='StatsSimula' component={StatsSimulaScreen} />
              <Stack.Screen name='CandleChart' component={CandleChartScreen} />
            </Stack.Navigator>
        </NavigationContainer>
    )
}

export default AppNavigator;
