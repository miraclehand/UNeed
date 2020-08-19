import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { getHeaderAuth } from './FetchOptions';

export function requestMessages(email, token, cntry, date1, date2) {
    const options = {
        method: 'GET',
        headers: getHeaderAuth(email, token),
    }

    const params = '?date1=' + encodeURIComponent(date1)
                 + '&date2=' + encodeURIComponent(date2)

    return dispatch => {
        fetch(URL.DISCS + '/' + cntry + params, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_MESSAGES,
                                    discs:json.discs}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

export function requestMessages1(email, token, cntry, code, date1, date2) {
    const options = {
        method: 'GET',
        headers: getHeaderAuth(email, token),
    }

    const params = '?code='  + code
                 + '&date1=' + encodeURIComponent(date1)
                 + '&date2=' + encodeURIComponent(date2)

    return dispatch => {
        fetch(URL.DISC + '/' + cntry + params, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_MESSAGES,
                                    discs:json.discs}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

export function requestMessage(email, token, cntry, date1, date2) {
    const options = {
        method: 'GET',
        headers: getHeaderAuth(email, token),
    }

    const params = '?code='  + code
                 + '&date1=' + encodeURIComponent(date1)
                 + '&date2=' + encodeURIComponent(date2)

    return dispatch => {
        fetch(URL.DISC + '/' + cntry + params, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_MESSAGES,
                                    discs:json.discs}))
            .catch(error => {
                console.log('error', error)
            })
    }
}
