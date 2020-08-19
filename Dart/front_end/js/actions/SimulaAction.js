import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { getHeaderAuth } from './FetchOptions';

export function initSimula() {
    return dispatch => {
        dispatch({type: ACTION_TYPE.INIT_SIMULA});
    }
}

export function requestSimula(os, db, email, token, cntry) {
    const options = {
        method: 'GET',
        headers: getHeaderAuth(email, token),
    }

    return dispatch => {
        fetch(URL.SIMULA + '/' + cntry + '/' + email, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_SIMULA,
                                    simulas:json.simulas}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

export function requestPostSimula(os, db, email, token, cntry, newSimula) {
    const options = {
        method: 'POST',
        headers: getHeaderAuth(email, token),
        body: JSON.stringify({unit:newSimula}),
    }

    return dispatch => {
        fetch(URL.SIMULA + '/' + cntry + '/' + email, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.PUSH_SIMULA,
                                    newSimula:json.simula}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

export function setSimula(index, simula) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.SET_SIMULA, index, simula});
    }
}
