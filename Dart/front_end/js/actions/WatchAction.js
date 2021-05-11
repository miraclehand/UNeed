import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { getHeaderAuth } from './FetchOptions';
import { exec_query, select_query } from '../util/dbUtil';

export function initWatch() {
    return dispatch => {
        dispatch({type: ACTION_TYPE.INIT_WATCH});
    }
}

/*
export function changeWatchName(name) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.CHANGE_WATCH_NAME, name});
    }
}

export function changeWatchStocks(stocks) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.CHANGE_WATCH_STOCKS, stocks});
    }
}

export function changeWatchStdDisc(std_disc) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.CHANGE_WATCH_STD_DISC, std_disc});
    }
}

export function changeWatchDetail(detail) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.CHANGE_WATCH_DETAIL, detail});
    }
}
*/

export function requestWatch(os, db, email, token, cntry) {
    if (os === 'web') {
        return requestWatchWeb(email, token, cntry);
    } else {
        return requestWatchMobile(db);
    }
}

function requestWatchWeb(email, token, cntry) {
    const options = {
        method: 'GET',
        headers: getHeaderAuth(email, token),
    }

    return dispatch => {
        fetch(URL.WATCHS + '/' + cntry + '/' + email, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_WATCHS,
                                    watchs:json.watchs}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

function requestWatchMobile(db) {
    const sql = 'select a.watch_id id, a.name, a.label, a.stock_codes, a.stock_names, b.std_disc_id, b.report_nm std_disc_report_nm, b.report_dnm std_disc_report_dnm from watch a, std_disc b where a.std_disc_id = b.std_disc_id order by a.watch_id;'
    return dispatch => {
        select_query(db, sql)
            .then(watchs => {
                dispatch({type: ACTION_TYPE.RECEIVE_WATCHS, watchs})
            })
    }
}

export function requestPostWatch(os, db, email, token, cntry, newWatch) {
    const options = {
        method: 'POST',
        headers: getHeaderAuth(email, token),
        body: JSON.stringify({unit:newWatch}),
    }

    if (os === 'web') {
        return requestPostWatchWeb(email, cntry, newWatch, options);
    } else {
        fetch(URL.WATCHS + '/' + cntry + '/' + email, options)
        return requestPostWatchMobile(db, newWatch);
    }
}

function requestPostWatchWeb(email, cntry, newWatch, options) {
    return dispatch => {
        fetch(URL.WATCHS + '/' + cntry + '/' + email, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.PUSH_WATCH, newWatch}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

function requestPostWatchMobile(db, newWatch) {
    const { id, name, stocks, std_disc, stock_codes, stock_names } = newWatch
    let sql

    sql = 'insert into watch(watch_id, name, label, stock_codes, stock_names, std_disc_id) values(?,?,?,?,?,?);',
    exec_query(db, sql, [id, name, stock_names, stock_codes, stock_names, std_disc.std_disc_id])

    sql = 'update metadata set last_watch_id = ?;',
    exec_query(db, sql, [id])

    stocks.map( stock => {
        sql = 'insert into watch_stock(watch_id, stock_code) values(?,?);',
        exec_query(db, sql, [id, stock.code])
    })
    return dispatch => {
        dispatch({type: ACTION_TYPE.SET_LAST_WATCH_ID, id})
        dispatch({type: ACTION_TYPE.PUSH_WATCH, newWatch})
    }
        /*
        .then( (watch_id) => {
            newWatch.id = watch_id
            const options = {
                method: 'POST',
                headers: getHeaderAuth('android@gmail.com', 'token'),
                body: JSON.stringify({unit:newWatch}),
            }
            fetch(URL.WATCHS + '/' + cntry + '/' + email, options)
            return dispatch => {
                dispatch({type: ACTION_TYPE.PUSH_WATCH, newWatch})
            }
        })
        */


/*
    return dispatch => {
        newWatch.stocks.map( stock => {
            sql = 'insert into watch_stock(id, stock_code) values(?,?);',
            exec_query(db, sql, [watch_stock_id, stock.code])
        })
    }

    return dispatch => {
        sql = 'select max(id) from watch_stock;'
        select_query(db, sql)
            .then(watch_stock_id => {
                aaa = 
                watch_stock_id.length > 0
                newWatch.stocks.map( stock => {
                    sql = 'insert into watch_stock(id, stock_code) values(?,?);',
                    exec_query(db, sql, [watch_stock_id, stock.code])
                })
                return watch_stock_id
            })
            .then( (watch_stock_id) => {
                sql = 'insert into watch(name, label, stock_codes, stock_names, watch_stock_id, std_disc_id) values(?,?,?,?,?,?);',
                exec_query(db, sql, [name, label, stock_codes, stock_names, watch_stock_id, std_disc_id])
            })
            .then( () => {
                dispatch({type: ACTION_TYPE.PUSH_WATCH, newWatch})
            })
        }
        */
}

export function requestDeleteWatch(os, db, email, token, cntry, delWatch) {
    const options = {
        method: 'DELETE',
        headers: getHeaderAuth(email, token),
        body: JSON.stringify({unit:delWatch}),
    }

    if (os === 'web') {
        return requestDeleteWatchWeb(email, cntry, delWatch, options);
    } else {
        fetch(URL.WATCHS + '/' + cntry + '/' + email, options)
        return requestDeleteWatchMobile(db, delWatch);
    }
}

function requestDeleteWatchWeb(email, cntry, delWatch, options) {
    return dispatch => {
        fetch(URL.WATCHS + '/' + cntry + '/' + email, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.POP_WATCH,delWatch}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

function requestDeleteWatchMobile(db, delWatch) {
    let sql

    return dispatch => {
        sql = 'delete from watch where watch_id = ?;'
        exec_query(db, sql, [delWatch.id])

        sql = 'delete from watch_stock where watch_id = ?;'
        exec_query(db, sql, [delWatch.id])

        dispatch({type: ACTION_TYPE.POP_WATCH,delWatch})
    }
}
