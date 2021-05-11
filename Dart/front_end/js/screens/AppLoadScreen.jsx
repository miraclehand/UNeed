import React, { useEffect, useState } from 'react';
import { View ,Image, Text, Platform } from 'react-native';
import { useDispatch, useSelector } from 'react-redux'
import Constants from 'expo-constants'
import * as SplashScreen from 'expo-splash-screen';
import { Asset } from 'expo-asset';
import { setAuthState, requestPostUser } from '../actions/UserAction';
import { db_create_table, db_drop_table, db_select_table, db_insert_metadata } from '../device/db';
import { cacheAuthState } from '../device/user';

import { cacheMetadata, cacheStocks, cacheStdDiscs, cacheChatRooms } from '../actions/DeviceAction';
import { requestStocks, requestStdDiscs, requestVersion } from '../actions/ServerPoolAction';

const AppLoadScreen = ({setReady}) => {
    const { os, cntry } = useSelector((state)=> state.baseReducer);
    const { db } = useSelector((state)=> state.dbReducer);
    const dispatch = useDispatch();

    useEffect( () => {
        SplashScreen.preventAutoHideAsync();
    }, []);

    const loadResourcesAsync = async() => {
        let authState
        const init_metadata = {'stock_ver':'2000-01-01', 'std_disc_ver':'2000-01-01', 'last_chat_id':'000000000000000000000000', 'last_watch_id':100, 'last_simula_id':100}

        SplashScreen.hideAsync();

        try {
            if (os === 'web') {
                authState = {name:'web', email:'web', level:0}
                dispatch(requestPostUser(authState, 'token'))
                dispatch(setAuthState(authState))
                dispatch(requestStocks(os, db, cntry))
                dispatch(requestVersion(os, db, cntry, {}))
                dispatch(cacheMetadata(init_metadata))
            } else {
                //tables = db_drop_table(db)
                //Promise.all(tables)
                tables = db_create_table(db)
                values = db_select_table(db)
                Promise.all(tables)
                await Promise.all(values).then( (results) => {
                    let   metadata
                    const _metadata = results[0]
                    const stocks    = results[1]
                    const std_discs = results[2]
                    const chat_room = results[3]

                    if (_metadata.length > 0) {
                        metadata = _metadata[0]
                    } else {
                        metadata = init_metadata
                        db_insert_metadata(db, metadata)
                    }
                    dispatch(cacheMetadata(metadata))
                    /*
                    if (version.length > 0) {
                        dispatch(cacheVersion(version[0]))
                    }
                    if (chatcheck.length > 0) {
                        dispatch(cacheChatId(chatcheck[0].chat_id))
                    } else {
                        insert_chat_id(db, init_chat_id)
                        dispatch(cacheChatId(init_chat_id))
                    }
                    */
                    if (stocks.length > 0) {
                        dispatch(cacheStocks(stocks))
                    } else {
                        dispatch(requestStocks(os, db, cntry))
                    }
                    if (std_discs.length > 0) {
                        dispatch(cacheStdDiscs(std_discs))
                    } else {
                        dispatch(requestStdDiscs(os, db, cntry))
                    }
                    if (chat_room.length > 0) {
                        dispatch(cacheChatRooms(chat_room))
                    }
                    dispatch(requestVersion(os, db, cntry, metadata))
                })
                if (Constants.isDevice) {
                    authState = await cacheAuthState();
                }
                else {
                    authState = {name:'android', email:'android@gmail.com', level:0}
                    dispatch(requestPostUser(authState, 'token'))
                }
                await dispatch(setAuthState(authState))
            }
        } catch (e) {
            alert(e)
            console.warn(e)
        } finally {
            setReady(true)
        }
    }
    return (
        <Image
            source={require('../../assets/icon.png')}
            style = {{ width : 200, height : 200 }}
            onLoad={loadResourcesAsync}
        />
    )
}

export default AppLoadScreen
