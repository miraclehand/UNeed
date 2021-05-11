import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux'
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { View, Text } from 'react-native';
import { Avatar, Badge, Icon, withBadge } from 'react-native-elements'
import { Ionicons } from '@expo/vector-icons';
//https://ionicons.com/

import WatchScreen from '../screens/WatchScreen'
import ChatRoomScreen from '../screens/ChatRoomScreen'
import SimulaScreen from '../screens/SimulaScreen'

const Tab = createBottomTabNavigator();

function IconWithBadge({ name, badge, color, size }) {
    const len = String(badge).length
    const width = 13 + len * 3

    return (
        <View style={{ width: 24, height: 24, margin: 5 }}>
            <Ionicons name={name} size={size} color={color} />
                {badge > 0 && 
                <View style={[styles.badgeCycle, {width:width}] } >
                    <Text style={styles.badgeText}> {badge} </Text>
                </View>
                }
        </View>
    );
}

function TabBarIcon(name, focused, size, color, rooms) {
    const badge = rooms.reduce((acc, cur, i) => {
            return acc + cur.badge
    },0)

    if (name === 'ChatRoom') {
        return (
            <IconWithBadge 
                size={size} color={color}
                badge={badge}
                name={focused ? 'chatbubble' : 'chatbubble-outline'}
            />
        )
    } else if (name === 'Watch') {
        return (
            <Ionicons
                size={size} color={color}
                name={focused ? 'star' : 'star-outline'}
            />
        )
    } else if (name === 'Simula') {
        return (
            <Ionicons
                size={size} color={color}
                name={focused ? 'flash' : 'flash-outline'}
                
            />
        )
    }
}

const HomeTabs = (props) => {
    const {rooms} = useSelector((state)=> state.chatRoomReducer);
    const dispatch = useDispatch();

    React.useEffect(() => {
    }, [])

    return (
        <Tab.Navigator
            screenOptions={({ route }) => ({
                tabBarIcon: ({ focused, color, size }) => {
                    return TabBarIcon(route.name, focused,size,color, rooms)
                },
            })}
        >
            <Tab.Screen name="Watch"  component={WatchScreen} />
            <Tab.Screen name="ChatRoom"  component={ChatRoomScreen} />
            <Tab.Screen name="Simula" component={SimulaScreen} />
        </Tab.Navigator>
    )
}

const styles = {
    badgeCycle: {
        position: 'absolute',
        right: -8,
        top: -8,
        backgroundColor: 'red',
        borderRadius: 6,
        width: 12,
        height: 13,
        justifyContent: 'center',
        alignItems: 'center',
    },
    badgeText: {
        color: 'white',
        fontSize: 10,
        fontWeight: 'bold',
    }
}

export default HomeTabs
