import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { getHeaderAuth } from './FetchOptions';
import { exec_query, select_query } from '../util/dbUtil';

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

export function receiveAlertRoom(db, watch_id, disc) {
    let sql
    const last_disc_label = disc['corp_name']
    //alert(disc['corp_name'])

    return dispatch => {
        sql = 'select watch_id from alert where watch_id = ?'
        select_query(db, sql, [watch_id])
            .then(rst => {
                if (rst.length === 0) { sql = 'insert into alert(watch_id, last_disc_label, update_time) values(?, ?, datetime(\'now\'))'
                    exec_query(db, sql, [watch_id, last_disc_label])
                } else {
                    sql = 'update alert set last_disc_label = ?, update_time = datetime(\'now\') where watch_id = ?'
                    exec_query(db, sql, [last_disc_label, watch_id])
                }
                sql = 'insert into disc(rcept_dt, reg_time, corp_cls, corp_code, corp_name, stock_code, rcept_no, report_nm, flr_nm, rm, tick, content, url ) values(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                exec_query(db, sql, [disc['rcept_dt'], disc['reg_time'], disc['corp_cls'], disc['corp_code'], disc['corp_name'], disc['stock_code'], disc['rcept_no'], disc['report_nm'], disc['flr_nm'], disc['rm'], disc['tick'], disc['content'], disc['url']])
                return dispatch({type: ACTION_TYPE.PUSH_DISC,
                                 new_disc:disc})
            })
    }
}

export function upsertAlertRoom(db, watch_id, disc) {
    const sql = 'insert into disc(watch_id, rcept_dt, reg_time, corp_cls, corp_code, corp_name, stock_code, rcept_no, report_nm, flr_nm, rm, tick, content, url ) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'

    //exec_query(db, sql, [watch_id, disc['rcept_dt'], disc['reg_time'], disc['corp_cls'], disc['corp_code'], disc['corp_name'], disc['stock_code'], disc['rcept_no'], disc['report_nm'], disc['flr_nm'], disc['rm'], disc['tick'], disc['content'], disc['url']])
    return dispatch({type: ACTION_TYPE.PUSH_DISC,
                     new_disc:disc})
}
export function receiveNotification(db, watch_id, disc) {
    let sql
    const last_disc_label = disc['corp_name']
    //alert(disc['corp_name'])

    return dispatch => {
        sql = 'select watch_id from alert where watch_id = ?'
        select_query(db, sql, [watch_id])
            .then(rst => {
                if (rst.length === 0) { sql = 'insert into alert(watch_id, last_disc_label, update_time) values(?, ?, datetime(\'now\'))'
                    exec_query(db, sql, [watch_id, last_disc_label])
                } else {
                    sql = 'update alert set last_disc_label = ?, update_time = datetime(\'now\') where watch_id = ?'
                    exec_query(db, sql, [last_disc_label, watch_id])
                }
                sql = 'insert into disc(rcept_dt, reg_time, corp_cls, corp_code, corp_name, stock_code, rcept_no, report_nm, flr_nm, rm, tick, content, url ) values(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                exec_query(db, sql, [disc['rcept_dt'], disc['reg_time'], disc['corp_cls'], disc['corp_code'], disc['corp_name'], disc['stock_code'], disc['rcept_no'], disc['report_nm'], disc['flr_nm'], disc['rm'], disc['tick'], disc['content'], disc['url']])
                return dispatch({type: ACTION_TYPE.PUSH_DISC,
                                 new_disc:disc})
            })
    }
}
