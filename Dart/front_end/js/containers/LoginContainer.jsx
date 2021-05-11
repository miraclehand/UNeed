import React, { useState } from 'react';
import * as WebBrowser from 'expo-web-browser';
import { Text, TextInput, Button } from 'react-native';
import * as Google from 'expo-auth-session/providers/google';
import { useDispatch, useSelector } from 'react-redux'
import { requestPostUser, setPushToken, setAuthState } from '../actions/UserAction';
import { saveAuthState } from '../device/user';
import LoginComponent from '../components/LoginComponent';
import { registerForPushNotificationsAsync } from '../device/user';

WebBrowser.maybeCompleteAuthSession();

const LoginContainer = (props) => {
    const [userInfo, setUserInfo] = useState(false);
    const [token, setToken] = useState('');

    const dispatch = useDispatch();
    const [request, response, promptAsync] = Google.useAuthRequest({
        expoClientId: '536908281748-teiiu4iu80p3romorrcj90pivgkbvkev.apps.googleusercontent.com',
        iosClientId: '536908281748-n5190ntbccf3gklu3f7h4im226edbjpc.apps.googleusercontent.com',
        androidClientId: '536908281748-jjtno1de0mpknm2nohh594o7q2oiasa5.apps.googleusercontent.com',
        webClientId: '536908281748-iut4mcukcfn8agn19iu2ioiqpfu2gces.apps.googleusercontent.com'
    });

    const handleSignIn = () => {
        promptAsync();
    }

    React.useEffect(() => {
        registerForPushNotificationsAsync().then(token => {
            setToken(token)
        })
        /*
        const fetchPushToken = async () => {
            dispatch(setPushToken(await registerForPushNotificationsAsync()))
        }
        fetchPushToken()
        */
    }, [])

    const fetchUserInfo = async (token) => {
        const sql = 'https://openidconnect.googleapis.com/v1/userinfo'
        const options = { headers: { Authorization: `Bearer ${token}` } }

        fetch(sql, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('request user fail');
            }).then(json => {
                setUserInfo(json)
            })
            .catch(error => {
                alert('error getAuthState:' + error)
            })
    };

    React.useEffect(() => {
        if (response?.type === 'success') {
            const { authentication } = response;
            fetchUserInfo(authentication.accessToken)
        }
    }, [response]);

    React.useEffect(() => {
        if (userInfo) {
            dispatch(setPushToken(token))
            dispatch(setAuthState(userInfo))
            dispatch(requestPostUser(userInfo, token))
        }
    }, [userInfo]);

    return (
        <LoginComponent
            request      = {request}
            handleSignIn = {handleSignIn}
            handleSignOut= {handleSignIn}
        />
    )
}
export default LoginContainer;

