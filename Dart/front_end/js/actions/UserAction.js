import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';

export function setUser(user) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.SET_USER,
                  name      : user ? user['name']      : null,
                  email     : user ? user['email']     : null,
                  pushToken : user ? user['pushToken'] : null,
                  level     : user ? user['level']     : null,
        });
    }
}

export function requestPostUser(user) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name      : user['name'],
                               email     : user['email'],
                               pushToken : user['pushToken'],
                               level     : user['level'],
        })
    }

    return dispatch => {
        fetch(URL.USER + '/' + user['name'], requestOptions)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('login fail');
            })
            .then(json => {
                dispatch({type: ACTION_TYPE.SET_USER,
                    name      : json.user.name,
                    email     : json.user.email,
                    pushToken : json.user.pushToken,
                    level     : json.user.level,
                });
            })
            .catch(error => {
                dispatch({type: ACTION_TYPE.FAIL_SIGN_IN});
            })
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
