import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { View, Text, Button, TouchableOpacity } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { MaterialCommunityIcons } from 'react-native-vector-icons';
import { initWatch, requestPostWatchList } from '../actions/WatchAction';

/*
import { Updates, Constants } from 'expo';
*/

import MainTabs from './MainTabNavigator';
import SimulaScreen from '../screens/SimulaScreen'
import CreateWatchScreen from '../screens/CreateWatchScreen'
import SetupWatchScreen from '../screens/SetupWatchScreen'
import AlertRoomScreen from '../screens/AlertRoomScreen'

const Stack = createStackNavigator();

class Connected extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            showUpdate: false
        }

        this.getHeaderTitle = this.getHeaderTitle.bind(this)
        this.getHeaderRight = this.getHeaderRight.bind(this)
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

    getHeaderTitle(route) {
        const title = route.state ? route.state.routes[route.state.index].name : route.name;
        return <Text style={{fontWeight:'bold'}}> { title } </Text>
    }

    AddWatchNextStep(navigation, route_name) {
        if (route_name === 'WatchList') {
            this.props.initWatch() 
            navigation.navigate('CreateWatch')
            return;
        }
        if (route_name === 'CreateWatch') {
            if (!this.props.watchName) {
                alert('관심 이름을 입력하세요.');
                return
            }
            if (this.props.watchStocks.length === 0) {
                alert('종목을 선택하세요.');
                return
            }
            navigation.navigate('SetupWatch')
            return
        }
        if (route_name === 'SetupWatch') {
            if (!this.props.watchStdDisc) {
                alert('공시를 선택 입력하세요.');
                return
            }
            const { os, db, email, token, cntry, watchState } = this.props

            this.props.requestPostWatchList(os, db, email, token, cntry, watchState)
            navigation.navigate('WatchList')
            return
        }
        if (route_name === 'Simula') {
        }
    }

    getAddWatchFontWeight(route_name) {
        if (route_name === 'CreateWatch') {
            if (!this.props.watchName) {
                return 'normal'
            }
            if (this.props.watchStocks.length === 0) {
                return 'normal'
            }
            return 'bold'
        }
        if (route_name === 'SetupWatch') {
            if (!this.props.watchStdDisc) {
                return 'normal'
            }
            return 'bold'
        }
    }

    getHeaderRight(route, navigation) {
        let buttons = []

        console.log('getHeaderRight', route )
        console.log('getHeaderRight', navigation )
        if (route.name === 'WatchList') {
            buttons = [
                { icon: <MaterialCommunityIcons name='magnify' size={30} />,
                  onPress: () => alert('this this'),
                },
                { icon: <MaterialCommunityIcons name='account-plus' size={30}/>,
                  onPress: () => this.AddWatchNextStep(navigation, route.name),
                },
            ]
        } else if (route.name === 'CreateWatch') {
            const fontWeight = this.getAddWatchFontWeight(route.name)

            buttons = [
                { icon: <Text style = {{ fontWeight:fontWeight }}>Next</Text>,
                  onPress: () => this.AddWatchNextStep(navigation, route.name),
                },
            ]
        } else if (route.name === 'SetupWatch') {
            const fontWeight = this.getAddWatchFontWeight(route.name)

            buttons = [
                { icon: <Text style = {{ fontWeight:fontWeight }}>Create</Text>,
                  onPress: () => this.AddWatchNextStep(navigation, route.name),
                },
            ]
        } else if (route.name === 'Simula') {
            buttons = [
                { icon: <MaterialCommunityIcons name='magnify' size={30} />,
                  onPress: () => alert('this this'),
                },
                { icon: <MaterialCommunityIcons name='eye-plus' size={30}/>,
                  onPress: () => this.AddWatchNextStep(navigation, route.name),
                },
            ]
        }

        return (
            <View style = {{
                flexDirection:'row',
                justifyContent:'flex-end',
                alignItems:'center'
            }}>
                {buttons && buttons.map((b, i) => {
                    return (
                        <TouchableOpacity onPress={b.onPress} key={i} >
                            {b.icon}
                        </TouchableOpacity>
                    )
                })}
            </View>
        )
    }

    render() {
        const { getHeaderTitle, getHeaderRight } = this 
        return (
            <NavigationContainer>
                <Stack.Navigator>
                    <Stack.Screen name='WatchList'
                        component={MainTabs} 
                        options = {({ route, navigation }) => ({
                            headerTitle: getHeaderTitle(route),
                            headerRight: () => getHeaderRight(route,navigation),
                        })}
                    />
                    <Stack.Screen name='CreateWatch'
                        component={CreateWatchScreen} 
                        options = {({ route, navigation }) => ({
                            headerTitle: getHeaderTitle(route),
                            headerRight: () => getHeaderRight(route,navigation),
                        })}
                    />
                    <Stack.Screen name='SetupWatch'
                        component={SetupWatchScreen} 
                        options = {({ route, navigation }) => ({
                            headerTitle: getHeaderTitle(route),
                            headerRight: () => getHeaderRight(route,navigation),
                        })}
                    />
                    <Stack.Screen name='AlertRoom'
                        component={AlertRoomScreen}
                    />
                    <Stack.Screen name='Simula'
                        component={SimulaScreen} 
                        options = {({ route, navigation }) => ({
                            headerTitle: getHeaderTitle(route),
                            headerRight: () => getHeaderRight(route,navigation),
                        })}
                    />
                </Stack.Navigator>
                {/* this.state.showUpdate ?
                    <>
                    <Text>A new update is available, click!</Text>
                    <Button onPress={this.doUpdate} title="Update Me" />
                    </>
                    : null
              */  }
            </NavigationContainer>
        )
    }
}

function mapStateToProps (state) {
    return {
        os: state.baseReducer.os,
        db: state.dbReducer.db,
        cntry: state.baseReducer.cntry,
        email: state.userReducer.email,
        watchName: state.watchReducer.name,
        watchStocks: state.watchReducer.stocks,
        watchStdDisc: state.watchReducer.std_disc,
        watchState: state.watchReducer,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        initWatch: bindActionCreators(initWatch, dispatch),
        requestPostWatchList: bindActionCreators(requestPostWatchList, dispatch),
    };
}

const AppNavigator = connect(mapStateToProps, mapDispatchToProps)(Connected);

export default AppNavigator
