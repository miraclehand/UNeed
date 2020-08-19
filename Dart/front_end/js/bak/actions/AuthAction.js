import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';

export function loadAuth() {
    return dispatch => {
        dispatch({type: ACTION_TYPE.LOAD_AUTH});
    }
}

export function requestFreePass() {
    return dispatch => {
        fetch(URL.FREE_PASS)
        .then(res => {
            if (res.ok) return res.json();
            else throw new Error('freepass fail');
        })
        .then(json => {
            dispatch({type: ACTION_TYPE.SUCCESS_FREE_PASS,
                username:json.username,
                token:json.token,
                level:json.level,
            });
        })
        .catch(error => {
            dispatch({type: ACTION_TYPE.FAIL_FREE_PASS});
        })
    }
}

export function requestSignIn(username, password) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username:encodeURIComponent(username),
                               password:encodeURIComponent(password)})
    }

    return dispatch => {
        fetch(URL.SIGN_IN, requestOptions)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('login fail');
            })
            .then(json => {
                dispatch({type: ACTION_TYPE.SUCCESS_SIGN_IN,
                    username:json.username,
                    token:json.token,
                    level:json.level,
                });
            })
            .catch(error => {
                dispatch({type: ACTION_TYPE.FAIL_SIGN_IN});
            })
    }
}

export function requestSignOn(username, password) {
    return dispatch => {
        fetch(URL.SIGN_ON, {
                method: 'POST',
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                    Accept: 'application/json',
                },
                body: JSON.stringify({
                    username: encodeURIComponent(username),
                    password: encodeURIComponent(password),
                }),
            }
        )
        .then(res => res.json())
        .then(json => dispatch({type: ACTION_TYPE.SUCCESS_SIGN_ON,
            username:json.username,
            token:json.token,
            level:json.level,
        }))
    }
}

export function signout() {
    return dispatch => {
        dispatch({type: ACTION_TYPE.SIGN_OUT});
    }
}
