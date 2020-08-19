import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { Text, View, Button, Vibration, Platform } from 'react-native';
import { AppLoading, Notifications } from 'expo'
import * as Permissions from 'expo-permissions';
import Constants from 'expo-constants';

import { getCachedUserAsync, getCachedAuthAsync, cacheAuthAsync } from './init/InitUser';
import { registerForPushNotificationsAsync } from './init/InitPush';
import { initDB } from './init/InitDB';

import { setUser, requestPostUser } from './actions/UserAction';
import { receiveNotification } from './actions/AlertRoomAction';
import { changeOS } from './actions/BaseAction';

import { finishLoading } from './actions/InitAction';
import AppNavigator from './navigation/AppNavigator';

import LoginScreen from './screens/LoginScreen';

import { Avatar, Badge, Icon, withBadge } from 'react-native-elements'


//import * as SQLite from 'expo-sqlite';

/*
import firebase from 'firebase';
const firebaseConfig = {
    apiKey: "AIzaSyAtHXv14VCnmSK7cjMmlNWQkRC-seQzIv4",
    authDomain: "dartuneed.firebaseapp.com",
    databaseURL: "https://dartuneed.firebaseio.com",
    projectId: "dartuneed",
    storageBucket: "dartuneed.appspot.com",
    messagingSenderId: "536908281748",
    appId: "1:536908281748:web:2efc7f414c8d0b4b38c181",
    measurementId: "G-B9FWV0FXYR"
}
firebase.initializeApp(firebaseConfig);
*/

export class Connected extends React.Component {
    constructor(props) {
        super(props)

        this.loadResourcesAsync = this.loadResourcesAsync.bind(this)
        this.handleLoadingError = this.handleLoadingError.bind(this)
        this.handleNotification = this.handleNotification.bind(this)
        this.sendPushNotification = this.sendPushNotification.bind(this)
        
        //const token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImMxNzcxODE0YmE2YTcwNjkzZmI5NDEyZGEzYzZlOTBjMmJmNWI5MjciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI1MzY5MDgyODE3NDgtOHA5dHA4ZmgzNmIycW0xNXQxbjk0dWtrNHZmaWczZTQuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI1MzY5MDgyODE3NDgtOHA5dHA4ZmgzNmIycW0xNXQxbjk0dWtrNHZmaWczZTQuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTU3MDk5MDE0OTM5OTQzMDAwNTgiLCJlbWFpbCI6Im1pcmFjbGVoYW5kQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiekJ1S0ZYczZaZXY4UkROVTNNLTY4ZyIsIm5hbWUiOiJ5b25nIGV1biBwYXJrIiwicGljdHVyZSI6Imh0dHBzOi8vbGg2Lmdvb2dsZXVzZXJjb250ZW50LmNvbS8taXU1UW1qbnl5STQvQUFBQUFBQUFBQUkvQUFBQUFBQUFBQUEvQU1adXVjbUhFUGR3WmxEcGw3a1JvVl9OVmhZbnNRd0ZfQS9zOTYtYy9waG90by5qcGciLCJnaXZlbl9uYW1lIjoieW9uZyBldW4iLCJmYW1pbHlfbmFtZSI6InBhcmsiLCJsb2NhbGUiOiJrbyIsImlhdCI6MTU4OTcyNDQyNywiZXhwIjoxNTg5NzI4MDI3fQ'
        //const token = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZG1pbkB0LW1vbmV0LmNvbSIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwidXNlcklkIjoiODNiYmEzNDAtMDI3ZC0xMWU4LWI4ZmEtYWY1YjU0OTEyMDA0IiwiZmlyc3ROYW1lIjoi7ISx64Ko7IucIiwibGFzdE5hbWUiOiLqtIDrpqzsnpAiLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiMzkwMTNjNzAtMDI3ZC0xMWU4LWI4ZmEtYWY1YjU0OTEyMDA0IiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCIsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNTM1OTU1NDE2LCJleHAiOjM2NzU5NTU0MTZ9.N1Ms0LA7WtOel1pg6lTMRNDJosY3qfR6Q4SVuAUwmDPmTj4uYnKU0B-9Wdlqmg4HQRUXa23edOTU-TnAxfBoyg'

        //console.log(Buffer.from(token, 'base64').toString('binary'))
        //const jwt_decode = require('jwt-decode')
        //const decoded = jwtDecoder(token)
        //console.log(decoded)
        //console.log(decoded['email'])
    }

    loadResourcesAsync() {
        (async () => {
            let cachedUser

            Notifications.addListener(this.handleNotification);

            /* cache user */
            const os = Platform.select({web:'web',android:'android',ios:'ios'})

            this.props.changeOS(os)
            if (os === 'web') {
                cachedUser = {name:'web', email:'web', pushToken:'web', level:0}
                this.props.requestPostUser(cachedUser)
                //this.props.setUser(cachedUser)
            } else {
                /* 둘중에 하나에서 에러가 발생 */
                cachedUser = await getCachedUserAsync();
                this.props.setUser(cachedUser)
                initDB(this.props.db); /* init db */
            }
        })()
    }

    handleLoadingError(error) {
        // In this case, you might want to report the error to your error
        // reporting service, for example Sentry
        console.warn(error)
    }

    handleNotification(notification) {
        alert('ddddddddddddddddd')
        Vibration.vibrate();
        console.log('receive notification', notification);
        alert('notification[' + JSON.stringify(notification) + ']')
        this.props.receiveNotification(notification)
    };

    sendPushNotification = async () => {
        const message = {
          to: this.state.expoPushToken,
          sound: 'default',
          title: this.state.title,
          body: this.state.body,
          data: { data: this.state.data },
          _displayInForeground: true,
        };
        /*
        const response = await fetch('http://182.228.22.202:8200/api/user/yepark', {
        */
        const response = await fetch('https://exp.host/--/api/v2/push/send', {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Accept-encoding': 'gzip, deflate',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(message),
        });
    };

    render () {
        if (!this.props.isLoadingComplete && !this.props.skipLoadingScreen) {
            return (
                <AppLoading
                    startAsync={this.loadResourcesAsync}
                    onError={this.handleLoadingError}
                    onFinish={this.props.finishLoading}
                />
            )
        }
        if (!this.props.email) return (<LoginScreen />)
        return (<AppNavigator />)
    }
}
/*
        const BadgedIcon = withBadge(1)(Icon)
        return <View>
                <Badge value={3} status="success" />
                <Badge value={3} status="error" containerStyle={{position:'absolute', top:50, right:50}} />
                <Badge value={<Text>My Custom Badge</Text>} />
                <Badge status="warning" />
                <Badge
                    status="success"
                    containerStyle={{ position: 'absolute', top: -4, right: -4 }}
                />
                <BadgedIcon type="ionicon" name="ios-chatbubbles" />
               </View>
        return (<Badge size={40}> 3</Badge>)
        return <LoginScreen />
        */

function mapStateToProps (state) {
    return {
        email: state.userReducer.email,
        isLoadingComplete: state.initReducer.isLoadingComplete,
        db: state.dbReducer.db,
        os: state.baseReducer.os,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        changeOS       : bindActionCreators(changeOS, dispatch),
        requestPostUser: bindActionCreators(requestPostUser, dispatch),
        setUser        : bindActionCreators(setUser, dispatch),
        finishLoading  : bindActionCreators(finishLoading, dispatch),
        receiveNotification : bindActionCreators(receiveNotification, dispatch),
    };
}

const Home = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default Home
