import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { getHeaderAuth } from './FetchOptions';
import { exec_query, select_query } from '../util/dbUtil';
import { upsert_chat_room } from '../device/db';

export function requestChatRoom(os, db, email, token, cntry) {
    if (os === 'web') {
        return requestChatRoomWeb(email, token, cntry);
    } else {
        return requestChatRoomMobile(db);
    }
}

export function requestChatRoomWeb(email, token, cntry) {
    const options = {
        method: 'GET',
        headers: getHeaderAuth(email, token),
    }

    return dispatch => {
        fetch(URL.CHAT_ROOM + '/' + cntry + '/' + email, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_CHAT_ROOM,
                                    rooms:json.rooms}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

function requestChatRoomMobile(db) {
    const sql = 'select a.*, b.name watch_name ' +
                '  from chat_room a' +
                '      ,watch b' +
                ' where a.watch_id = b.watch_id' +
                ' order by a.update_time desc;'

    return dispatch => {
        select_query(db, sql)
            .then(rooms => {
                dispatch({type: ACTION_TYPE.RECEIVE_CHAT_ROOM,
                          rooms:rooms})
            })
    }
}

export function upsertChatRoom(watch_id, watch_name, last_label, badge) {
    return dispatch => {
        const room = { watch_id, watch_name, last_label, 'badge':badge }
        dispatch({type: ACTION_TYPE.UPSERT_CHAT_ROOM, room})
    }
}

export function updateBadge(os, db, watch_id, badge) {
    if (os !== 'web') {
        const sql = 'update chat_room set badge = 0 where watch_id = ?'
        exec_query(db, sql, [watch_id])
    }
    return dispatch => {
        dispatch({type: ACTION_TYPE.UPDATE_BADGE, watch_id})
    }
}

export function requestDeleteChatRoom(os, db, email, token, cntry, delRoom) {
    const options = {
        method: 'DELETE',
        headers: getHeaderAuth(email, token),
        body: JSON.stringify({watch_id:delRoom.watch_id}),
    }

    if (os === 'web') {
        return requestDeleteChatRoomWeb(email, cntry, delRoom, options);
    } else {
        fetch(URL.CHAT_ROOM + '/' + cntry + '/' + email, options)
        return requestDeleteChatRoomMobile(db, delRoom);
    }
}

function requestDeleteChatRoomWeb(email, cntry, delRoom, options) {
    return dispatch => {
        fetch(URL.CHAT_ROOM + '/' + cntry + '/' + email, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.POP_CHAT_ROOM, delRoom}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

function requestDeleteChatRoomMobile(db, delWatch) {
    let sql

    return dispatch => {
        sql = 'delete from watch where watch_id = ?;'
        exec_query(db, sql, [delWatch.id])

        sql = 'delete from watch_stock where watch_id = ?;'
        exec_query(db, sql, [delWatch.id])

        dispatch({type: ACTION_TYPE.POP_CHAT_ROOM, delRoom})
    }
}


