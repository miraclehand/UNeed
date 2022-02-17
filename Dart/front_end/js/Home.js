import React, { useState, useRef } from 'react';
import { AppState, Vibration, Text, Button } from 'react-native';
import { useDispatch, useSelector } from 'react-redux'
import * as Updates from 'expo-updates';
import * as Notifications from 'expo-notifications';
import AppNavigator from './navigation/AppNavigator';
import LoginScreen from './screens/LoginScreen';
import { requestChatCatchup, requestPutChatCheck, upsertChat } from './actions/ChatAction';
import { upsertChatRoom, updateBadge } from './actions/ChatRoomAction';
//import { receiveMessage } from './actions/MessageAction';
import { upsert_chat_room, insert_chat } from './device/db';
import { requestBalance } from './actions/HTSAction';
import { Alert } from "react-native";

Notifications.setNotificationHandler({
    handleNotification: async () => ({
        shouldShowAlert: true,
        shouldPlaySound: false,
        shouldSetBadge: false,
    }),
});

export default function Home (props) {
    //const [appState, setAppState] = useState(AppState.currentState);
    const appState = useRef(AppState.currentState);
    const [appStateVisible, setAppStateVisible] = useState(appState.current);
    const { email, token } = useSelector((state)=> state.userReducer);
    const { navigation, os, cntry } = useSelector((state)=> state.baseReducer);
    const { db, chat_id } = useSelector((state)=> state.dbReducer);
    const { metadata } = useSelector((state)=> state.dbReducer);
    const { rooms } = useSelector((state)=> state.chatRoomReducer); 
    const chat_id_ref = React.useRef(chat_id)
    const metadata_ref = React.useRef(metadata)

    const navigation_ref = React.useRef(navigation)

    const dispatch = useDispatch();

    React.useEffect(() => {
        let noti, resp
        AppState.addEventListener("change", handleAppStateChange);

        // NOTE IOS에서는 add,remove,add 순으로 해야지 1번만 리스너가 동작한다.
        noti =Notifications.addNotificationReceivedListener(handleNotification);
        resp =Notifications.addNotificationResponseReceivedListener(handleResponse);
        Notifications.removeNotificationSubscription(noti);
        Notifications.removeNotificationSubscription(resp);
        noti =Notifications.addNotificationReceivedListener(handleNotification);
        resp =Notifications.addNotificationResponseReceivedListener(handleResponse);
        dispatch(requestBalance(email, token))
        return () => {
            AppState.removeEventListener("change", handleAppStateChange);
            Notifications.removeNotificationSubscription(noti);
            Notifications.removeNotificationSubscription(resp);
        };
    }, [])

    React.useEffect(() => {
        chat_id_ref.current = chat_id
    }, [chat_id])

    React.useEffect(() => {
        metadata_ref.current = metadata
    }, [metadata])

    React.useEffect(() => {
        if (navigation) {
            navigation_ref.current = navigation.current
        }
    }, [navigation])

    React.useEffect(() => {
        if (email && os !== 'web') {
            handleAppUpdate()
            dispatch(requestChatCatchup(os, db, email, token, cntry, metadata_ref.current.last_chat_id))
        }
    }, [email])

    const handleAppUpdate = async () => {
        try {
            const update = await Updates.checkForUpdateAsync();
            if (update.isAvailable) {
                Alert.alert(
                    '알림!',
                    '새로운 버전이 있습니다. 업데이트 하시겠습니까?',
                    [
                        {
                            text: 'Cancel',
                            onPress: () => console.log('Cancel Pressed'),
                            style: 'cancel',
                        },
                        {text: 'OK', onPress: () => runUpdate()},
                    ],
                    {cancelable: false},
                );
            }
        } catch (e) {
            alert(e)
            console.log(e)
            // handle or log error
        }
    }

    const runUpdate = async () => {
        await Updates.fetchUpdateAsync();
        alert('업데이트 진행중입다...')
        await Updates.reloadAsync();
    }

    const handleAppStateChange = (nextAppState) => {
        if (appState.current.match(/inactive|background/) &&
            nextAppState === "active" &&
            email && os !== 'web') 
        {
            dispatch(requestChatCatchup(os, db, email, token, cntry, metadata_ref.current.last_chat_id))
            //handleAppUpdate() TODO
        }
        appState.current = nextAppState;
    };

    const getCurrentRouteName = () => {
        if (navigation_ref && navigation_ref.current) {
            return navigation_ref.current?.getCurrentRoute().name
        }
        return 'nonamed'
    }

    const handleResponse = (notification) => {
        const content = notification.notification.request.content
        const data    = content.data
        const chat    = data.chat

        if (getCurrentRouteName() !== 'Chat' && navigation_ref.current) {
            navigation_ref.current.navigate('Chat', { 'watch_id': data.watch_id })
        }
        dispatch(updateBadge(os, db, data.watch_id, 0))
    }

    const handleNotification = (notification) => {
        const content = notification.request.content
        const title   = content.title
        const body    = content.body
        const data    = content.data
        const data_type = data.data_type
        const chat      = data.chat
        const watch_id   = data.watch_id
        const watch_name = data.watch_name

        if (data_type !== 1) {
            return
        }

        let badge = 0
        if (getCurrentRouteName() !== 'Chat') {
            badge = 1
        }
        upsert_chat_room(db, watch_id, chat.label)
        insert_chat(db, chat)

        dispatch(upsertChatRoom(watch_id, watch_name, chat.label, badge))
        dispatch(upsertChat(chat))
        dispatch(requestPutChatCheck(os, db, email, token, cntry, chat._id))
    }

    return (
        <>
            {!email ? <LoginScreen /> : <AppNavigator />}
        </>
    )
}

