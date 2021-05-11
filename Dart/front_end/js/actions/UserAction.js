import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { saveAuthState } from '../device/user';

export function requestUser(token, pushToken) {
    const sql = 'https://openidconnect.googleapis.com/v1/userinfo'
    const options = {
        headers: { Authorization: `Bearer ${token}` }
    }
    return dispatch => {
        fetch(sql, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('request user fail');
            })
            .then(json => {
                //alert(JSON.stringify(json))
                //saveAuthState(json)
                //setAuthState(json)
                //dispatch({type: ACTION_TYPE.SET_AUTH_STATE, json });
                /*
                dispatch({type: ACTION_TYPE.SET_AUTH_STATE,
                          name:  json['name'],
                          email: json['email'],
                          level: 0,
                });
                */
                alert('PostUser1')
                requestPostUser(json, pushToken)
            })
            .catch(error => {
                alert('error requestUser:' + error)
            })
    }
}

export function setAuthState(authState) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.SET_AUTH_STATE,
                  name:  authState['name'],
                  email: authState['email'],
                  level: 0,
        });
    }
}

export function setPushToken(pushToken) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.SET_PUSH_TOKEN, pushToken});
    }
}

export function requestPostUser(user, pushToken) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name      : user['name'],
                               email     : user['email'],
                               pushToken : pushToken,
                               level     : 0,
        })
    }

    return dispatch => {
        fetch(URL.USER + '/' + user['name'], requestOptions)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('login fail');
            })
            .then(json => {
                if (user['name'] !== 'web') {
                    saveAuthState(user)
                }
            })
            .catch(error => {
                dispatch({type: ACTION_TYPE.FAIL_SIGN_IN});
            })
    }
}

export function signOut() {
    return dispatch => {
        dispatch({type: ACTION_TYPE.SIGN_OUT});
    }
}

/*
export function requestFreePass() {
    return dispatch => {
        fetch(URL.FREE_PASS)
        .then(res => {
            if (res.ok) return res.json();
            else throw new Error('freepass fail');
        })
        .then(json => {
            dispatch({type: ACTION_TYPE.SUCCESS_FREE_PASS,
                email:json.email,
                token:json.token,
                level:json.level,
            });
        })
        .catch(error => {
            dispatch({type: ACTION_TYPE.FAIL_FREE_PASS});
        })
    }
}

export function requestSignIn(email, password) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email:encodeURIComponent(email),
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
                    email:json.email,
                    token:json.token,
                    level:json.level,
                });
            })
            .catch(error => {
                dispatch({type: ACTION_TYPE.FAIL_SIGN_IN});
            })
    }
}

export function requestSignOn(email, password) {
    return dispatch => {
        fetch(URL.SIGN_ON, {
                method: 'POST',
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                    Accept: 'application/json',
                },
                body: JSON.stringify({
                    email: encodeURIComponent(email),
                    password: encodeURIComponent(password),
                }),
            }
        )
        .then(res => res.json())
        .then(json => dispatch({type: ACTION_TYPE.SUCCESS_SIGN_ON,
            email:json.email,
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
*/
