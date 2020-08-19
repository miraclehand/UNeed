import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { getHeaderAuth } from './FetchOptions';

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
        return requestWatchMobile(db, email, token, cntry);
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

export function requestPostWatch(os, db, email, token, cntry, newWatch) {
    if (os === 'web') {
        return requestPostWatchWeb(email, token, cntry, newWatch);
    } else {
        return requestPostWatchMobile(db, email, token, cntry, newWatch);
    }
}

function requestPostWatchWeb(email, token, cntry, newWatch) {
    const options = {
        method: 'POST',
        headers: getHeaderAuth(email, token),
        body: JSON.stringify({unit:newWatch}),
    }

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

export function requestDeleteWatch(os, db, email, token, cntry, delWatch) {
    if (os === 'web') {
        return requestDeleteWatchWeb(email, token, cntry, delWatch);
    } else {
        return requestDeleteWatchMobile(db, email, token, cntry, delWatch);
    }
}

function requestDeleteWatchWeb(email, token, cntry, delWatch) {
    const options = {
        method: 'DELETE',
        headers: getHeaderAuth(email, token),
        body: JSON.stringify({unit:delWatch}),
    }

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
