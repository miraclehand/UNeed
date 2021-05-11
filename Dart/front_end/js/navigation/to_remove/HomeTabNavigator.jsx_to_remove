import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
//import { WatchStackScreen, AlertStackScreen, SimulaStackScreen } from './StackNavigator'

import { View, Text, Button, TouchableOpacity } from 'react-native';
import { Avatar, Badge, Icon, withBadge } from 'react-native-elements'
import { Ionicons } from '@expo/vector-icons';

// https://reactnavigation.org/docs/tab-based-navigation/
import WatchScreen from '../screens/WatchScreen'
import AlertScreen from '../screens/AlertScreen'
import SimulaScreen from '../screens/SimulaScreen'

const Tab = createBottomTabNavigator();
/*
https://snack.expo.io/?platform=android&name=Screen%20options%20resolution%20%7C%20React%20Navigation&dependencies=%40react-native-community%2Fmasked-view%40%5E0.1.1%2C%40react-navigation%2Fnative%40%5E5.0.5%2C%40react-navigation%2Fbottom-tabs%40%5E5.0.5%2C%40react-navigation%2Fdrawer%40%5E5.0.5%2C%40react-navigation%2Fmaterial-bottom-tabs%40%5E5.0.5%2C%40react-navigation%2Fmaterial-top-tabs%40%5E5.0.5%2C%40react-navigation%2Fstack%40%5E5.0.5%2Creact-native-gesture-handler%401.5.2%2Creact-native-reanimated%401.4.0%2Creact-native-safe-area-context%400.6.0%2Creact-native-screens%402.0.0-alpha.12&sourceUrl=https%3A%2F%2Freactnavigation.org%2Fexamples%2F5.x%2Ftab-based-navigation-badges.js
*/

function IconWithBadge({ name, badgeCount, color, size }) {
  return (
    <View style={{ width: 24, height: 24, margin: 5 }}>
      <Ionicons name={name} size={size} color={color} />
      {badgeCount > 0 && (
        <View
          style={{
            // On React Native < 0.57 overflow outside of parent will not work on Android, see https://git.io/fhLJ8
            position: 'absolute',
            right: -6,
            top: -3,
            backgroundColor: 'red',
            borderRadius: 6,
            width: 12,
            height: 12,
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          <Text style={{ color: 'white', fontSize: 10, fontWeight: 'bold' }}>
            {badgeCount}
          </Text>
        </View>
      )}
    </View>
  );
}
function AlertIconWithBadge(props) {
      // You should pass down the badgeCount in some other ways like React Context API, Redux, MobX or event emitters.
      return <IconWithBadge {...props} badgeCount={5} />;
}
class HomeTabs extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <Tab.Navigator
                screenOptions={({ route }) => ({
                    tabBarIcon: ({ focused, color, size }) => {
                        if (route.name === 'Alert') {
                            return (
                                <AlertIconWithBadge
                                    name={
                                        focused
                                            ? 'ios-information-circle'
                                            : 'ios-information-circle-outline'
                                    }
                                    size={size}
                                    color={color}
                                />
                            )
                        } else if (route.name === 'Watch') {
                            return (
                                <Ionicons
                                    name={focused ? 'ios-list-box' : 'ios-list'}
                                    size={size}
                                    color={color}
                                />
                            )
                        } else if (route.name === 'Simula') {
                            return (
                                <Ionicons
                                    name={focused ? 'ios-list-box' : 'ios-list'}
                                    size={size}
                                    color={color}
                                />
                            )
                        }
                    }
                })}
            >
                <Tab.Screen name="Watch"  component={WatchScreen}  />
                <Tab.Screen name="Alert"  component={AlertScreen}  />
                <Tab.Screen name="Simula" component={SimulaScreen} />
            </Tab.Navigator>
        )
        /*
                <Tab.Screen name="Watch"  component={WatchStackScreen}  />
                <Tab.Screen name="Alert"  component={AlertStackScreen}  />
                <Tab.Screen name="Simula" component={SimulaStackScreen} />
                */
    }
}

export default HomeTabs
