import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { getHeaderAuth } from './FetchOptions';

export function requestAlert(os, db, email, token, cntry) {
    if (os === 'web') {
        return requestAlertWeb(email, token, cntry);
    } else {
        return requestAlertMobile(db);
    }
}

export function requestAlertWeb(email, token, cntry) {
    const options = {
        method: 'GET',
        headers: getHeaderAuth(email, token),
    }

    return dispatch => {
        fetch(URL.ALERT + '/' + cntry + '/' + email, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_ALERT,
                                    rooms:json.rooms}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

function requestAlertMobile(db) {
    const sql = 'select a.watch_id, b.name watch_name, a.room_id, a.last_disc_label, a.badge_count' +
                '  from alert a' +
                '      ,watch b' +
                ' where a.watch_id = b.id' +
                ' order by a.update_time desc;'

    return dispatch => {
        select_query(db, sql)
            .then(rooms => {
                dispatch({type: ACTION_TYPE.RECEIVE_ALERT,
                          rooms:rooms})
            })
    }
}

export function upsertAlert(email, token, cntry) {
}
