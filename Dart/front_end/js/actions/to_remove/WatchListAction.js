import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { getHeaderAuth } from './FetchOptions';

function requestWatchListWeb(email, token, cntry) {
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

function requestWatchListMobile(db, email, token, cntry) {
    return dispatch => {
        return db.transaction(tx => {
            tx.executeSql("select * from watch_list order by keyword;",
                [],
                (_, {rows:{_array}}) => {
                    return dispatch({type: ACTION_TYPE.RECEIVE_WATCHS,
                                     watchs:_array})
                },
                /*(t, error) => {*/
                (_, error) => {
                    alert('error select watch_list=>' + error)
                }
            );
        })
    }
}
/*
export function fetchGroupMeta() {
    return (dispatch) => {
            return db.transaction(txn => {
                txn.executeSql(
                    'SELECT * FROM group_meta',
                    [],
                    (_, result) => {
                        console.log('Result', result);
                        return dispatch(getGroupMetaSuccess(['fake', 'data']));
                    },
                    (_, error) => {
                        console.log('Error', error);
                        return dispatch(getGroupMetaFailure(error));
                    }
                );
            });
    };
}
*/

export function requestWatchList(os, db, email, token, cntry) {
    if (os === 'web') {
        return requestWatchListWeb(email, token, cntry);
    } else {
        return requestWatchListMobile(db, email, token, cntry);
    }
}

function requestPostWatchListWeb(email, token, cntry, keyword) {
    const stock_code = 'stock_code'
    const stock_name = 'stock_name'

    const options = {
        method: 'POST',
        headers: getHeaderAuth(email, token),
        body: JSON.stringify({keyword:keyword}),
    }

    return dispatch => {
        fetch(URL.WATCHS + '/' + cntry + '/' + email, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.PUSH_WATCH,
                                    new_watchs:{stock_code,stock_name,keyword}}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

function requestPostWatchListMobile(db, email, token, cntry, keyword) {
    const stock_code = 'stock_code'
    const stock_name = 'stock_name'

    const options = {
        method: 'POST',
        headers: getHeaderAuth(email, token),
        body: JSON.stringify({keyword:keyword}),
    }

    return dispatch => {
        fetch(URL.WATCHS + '/' + cntry + '/' + email, options)
        return db.transaction( tx => {
            tx.executeSql(
                "insert into watch_list(stock_code, stock_name, keyword) " + 
                "values(?, ?, ?);",
                [stock_code, stock_name, keyword],
                (_, {rows}) => {
                },
                (_, error) => {
                    alert('error insert watch_list=>' + error)
                });
            return dispatch({type: ACTION_TYPE.PUSH_WATCH,
                             new_watchs:{stock_code,stock_name,keyword}})
        });
    }
}

export function requestPostWatchList(os, db, email, token, cntry, keyword) {
    if (os === 'web') {
        return requestPostWatchListWeb(email, token, cntry, keyword);
    } else {
        return requestPostWatchListMobile(db, email, token, cntry, keyword);
    }
}

function requestDeleteWatchListWeb(email, token, cntry, index, keyword) {
    const stock_code = 'stock_code'
    const stock_name = 'stock_name'

    const options = {
        method: 'DELETE',
        headers: getHeaderAuth(email, token),
        body: JSON.stringify({keyword:keyword}),
    }

    return dispatch => {
        fetch(URL.WATCHS + '/' + cntry + '/' + email, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.POP_WATCH,
                                    index:index}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

function requestDeleteWatchListMobile(db, email, token, cntry, index, keyword) {
    const stock_code = 'stock_code'
    const stock_name = 'stock_name'

    const options = {
        method: 'DELETE',
        headers: getHeaderAuth(email, token),
        body: JSON.stringify({keyword:keyword}),
    }

    return dispatch => {
        fetch(URL.WATCHS + '/' + cntry + '/' + email, options)
        return db.transaction( tx => {
            tx.executeSql(
                "delete from watch_list where stock_code = ? and stock_name = ? and keyword = ?);" + 
                [stock_code, stock_name, keyword],
                (_, {rows}) => {
                },
                (_, error) => {
                    alert('error delete watch_list=>' + error)
                });
            return dispatch({type: ACTION_TYPE.POP_WATCH,
                             index:index})
        });
    }
}

export function requestDeleteWatchList(os, db, email, token, cntry, index, keyword) {
    if (os === 'web') {
        return requestDeleteWatchListWeb(email, token, cntry, index, keyword);
    } else {
        return requestDeleteWatchListMobile(db, email, token, cntry, index, keyword);
    }
}
