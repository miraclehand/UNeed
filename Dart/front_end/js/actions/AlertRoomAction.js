import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { getHeaderAuth } from './FetchOptions';

function requestAlertRoomWeb(email, token, cntry, watch_id) {
    const options = {
        method: 'GET',
        headers: getHeaderAuth(email, token),
    }

    return dispatch => {
        fetch(URL.ALERT_ROOM + '/' + cntry + '/' + email + '/' + watch_id, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_ALERT_ROOM,
                                    discs:json.discs}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

function requestAlertRoomMobile(db, email, token, cntry, watch_id) {
    return dispatch => {
        return db.transaction(tx => {
            tx.executeSql("select * from disc where watch_id = ? order by _id;",
                [watch_id],
                (_, {rows:{_array}}) => {
                    return dispatch({type: ACTION_TYPE.RECEIVE_ALERT_ROOM,
                                     discs:_array})
                }, (t, error) => {
                    alert('error select disc=>' + error)
                }
            );
        })
    }
}

export function requestAlertRoom(os, db, email, token, cntry, watch_id) {
    if (os === 'web') {
        return requestAlertRoomWeb(email, token, cntry, watch_id);
    } else {
        return requestAlertRoomMobile(db, email, token, cntry, watch_id);
    }
}


export function receiveNotification(disc) {
    return dispatch => {
        return db.transaction( tx => {
            tx.executeSql(
                "insert into disc(rcept_dt, reg_time, corp_cls, corp_code, corp_name, stock_code, rcept_no, report_nm, flr_nm, rm, tick, content, url ) " +
                "values(?, ?, ?);",
                [disc['rcept_dt'], disc['reg_time'], disc['corp_cls'], disc['corp_code'], disc['corp_name'], disc['stock_code'], disc['rcept_no'], disc['report_nm'], disc['flr_nm'], disc['rm'], disc['tick'], disc['content'], disc['url']],
                (_, {rows}) => {
                }, (t, error) => {
                    alert('error insert disc =>' + error)
                });
                return dispatch({type: ACTION_TYPE.PUSH_DISC,
                                 new_disc:disc})
        });
    }
}
