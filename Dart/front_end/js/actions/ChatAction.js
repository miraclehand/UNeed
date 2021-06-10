import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { getHeaderAuth } from './FetchOptions';
import { exec_query, select_query } from '../util/dbUtil';
import { upsert_chat_room, insert_chat } from '../device/db';

export function upsertChat(chat) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.UPSERT_CHAT, chat})
    }
}

export function requestChat(os, db, email, token, cntry, watch_id) {
    if (os === 'web') {
        return requestChatWeb(email, token, cntry, watch_id);
    } else {
        return requestChatMobile(db, watch_id);
    }
}

export function requestChatWeb(email, token, cntry, watch_id) {
    const options = {
        method: 'GET',
        headers: getHeaderAuth(email, token),
    }

    console.log(URL.CHAT + '/' + cntry + '/' + email + '/' + watch_id)
    return dispatch => {
        fetch(URL.CHAT + '/' + cntry + '/' + email + '/' + watch_id, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_CHAT,
                                    chats:json.chats}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

function requestChatMobile(db, watch_id) {
    const sql = 'select * ' +
                '  from chat a' +
                ' where a.watch_id = ?;'

    return dispatch => {
        select_query(db, sql, [watch_id])
            .then(chats => {
                dispatch({type: ACTION_TYPE.RECEIVE_CHAT, chats})
            })
    }
}

export function requestChatCheck_not_use(db, email, token, cntry, chat_id) {
    const options = {
        method: 'GET',
        headers: getHeaderAuth(email, token),
    }

    return dispatch => {
        fetch(URL.CHAT_CHECK + '/' + cntry + '/' + email + '/'+chat_id, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => {
                if (json.rooms) {
                    json.rooms.map( room => {
                        upsert_chat_room(db, room.watch_id, room.last_label)
                        dispatch({type: ACTION_TYPE.UPSERT_CHAT_ROOM, room})
                    })
                }
            })
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

export function requestChatCatchup(os, db, email, token, cntry, chat_id) {
    const options = {
        method: 'GET',
        headers: getHeaderAuth(email, token),
    }

    return dispatch => {
        fetch(URL.CHAT_CATCHUP+'/'+cntry+'/'+email+'/'+chat_id, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => {
                if (json.exec_query !== '') {
                    json.exec_query.split(';').map( (query) => {
                        exec_query(db, query)
                            .catch(error => {
                                console.log('error', error)
                                dispatch({type: ACTION_TYPE.SIGN_OUT})
                            })
                        })
                    dispatch({type: ACTION_TYPE.SIGN_OUT})
                }

                json.rooms.map( room => {
                    upsert_chat_room(db, room.watch_id, room.last_label)
                    dispatch({type: ACTION_TYPE.UPSERT_CHAT_ROOM, room})
                })
                json.chats.map( chat => {
                    insert_chat(db, chat)
                    dispatch({type: ACTION_TYPE.UPSERT_CHAT, chat})
                })
                if (json.chats.length > 0) {
                    //requestPutChatCheck(os, db, email, token, cntry, json.last_chat_id)
                    const sql = 'update metadata set last_chat_id = ?;'
                    exec_query(db, sql, [json.last_chat_id])
                    dispatch({type: ACTION_TYPE.SET_CHAT_ID, chat_id:json.last_chat_id})
                }
            })
            .catch(error => {
                console.log('error', error)
                //서버 재부팅할때 접속하는 경우가 있을 수 있다.
                //dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

export function requestPutChatCheck(os, db, email, token, cntry, chat_id) {
    const options = {
        method: 'PUT',
        headers: getHeaderAuth(email, token),
    }

    if (os === 'web') {
        return requestPutChatCheckWeb(email, token, cntry, chat_id, options)
    } else {
        fetch(URL.CHAT_CHECK + '/' + cntry+ ' /' + email+'/'+chat_id, options)
        return requestPutChatCheckMobile(db, chat_id)
    }
}

function requestPutChatCheckWeb(os, db, email, token, cntry, chat_id, options) {
    return dispatch => {
        fetch(URL.CHAT_CHECK + '/' + cntry + '/' + email + '/'+chat_id, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

function requestPutChatCheckMobile(db, chat_id) {
    const sql = 'update metadata set last_chat_id = ?;'
    exec_query(db, sql, [chat_id])
    return dispatch => {
        dispatch({type: ACTION_TYPE.SET_CHAT_ID, chat_id})
    }
}


