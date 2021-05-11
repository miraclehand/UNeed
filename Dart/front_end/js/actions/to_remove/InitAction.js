import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { exec_query, select_query } from '../util/dbUtil';

export function finishLoading() {
    return dispatch => {
        dispatch({type: ACTION_TYPE.FINISH_LOADING});
    }
}

export function requestVersion() {
    return dispatch => {
        fetch(URL.VERSION)
            .then(res => {
                return res.json();
            })
            .then(json => {
                return dispatch({type: ACTION_TYPE.RECEIVE_SERVER_VERSION,
                                 version:json.version})
            })
    }
}

export function loadData(db) {
    let sql

    sql = 'select * from version;'
    select_query(db, sql)
        .then( version => {
            if (version.length === 0) {
                sql = 'insert into version(stock_ver,std_disc_ver) values(?,?);'
                exec_query(db, sql, ['2000-01-01', '2000-01-01'])
                ver = {'stock_ver':'2000-01-01', std_disc_ver:'2000-01-01'}
            } else {
                ver = version[0]
            }
            dispatch({type:ACTION_TYPE.SET_VERSION, version:ver})
        })

    sql = 'select * from stock;'
    select_query(db, sql)
        .then( stocks => {
            dispatch({type:ACTION_TYPE.RECEIVE_LIST_STOCK, list_stock: stocks})
        })

    sql = 'select * from std_disc;'
    select_query(db, sql)
        .then( std_disc => {
            dispatch({type:ACTION_TYPE.RECEIVE_LIST_STD_DISC, list_std_disc: std_disc})
        })
}

export function updateVersion(os, db, version) {
    let sql

    sql = 'select * from version'
    select_query(db, sql)
        .then(ver => {
            if (ver.length === 0) {
                sql = 'insert into version(stock_ver,std_disc_ver) values(?,?);'
            } else {
                sql = 'update version set stock_ver = ?, std_disc_ver = ?;'
            }
            exec_query(db, sql, [version.stock_ver, version.std_disc_ver])
         })
    return dispatch({type:ACTION_TYPE.SET_VERSION, version})
}
