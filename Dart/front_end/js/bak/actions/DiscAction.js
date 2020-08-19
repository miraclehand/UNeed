import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import signout from './AuthAction';
import { getHeaderAuth } from './FetchOptions';

export function requestDiscs(username, token, cntry, date1, date2) {
    const params = '?date1=' + encodeURIComponent(date1)
                 + '&date2=' + encodeURIComponent(date2)

    const header = getHeaderAuth(username, token, 'GET')

    return dispatch => {
        fetch(URL.DISCS + '/' + cntry + params, header)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_DISC,
                                    discs:json.discs}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

export function requestDisc(username, token, cntry, code, date1, date2) {
    const params = '?code='  + code
                 + '&date1=' + encodeURIComponent(date1)
                 + '&date2=' + encodeURIComponent(date2)

    const options = {
        method: 'GET',
        headers: getHeaderAuth(username, token)
    }

    return dispatch => {
        fetch(URL.DISC + '/' + cntry + params, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_DISC,
                                    discs:json.discs}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

export function requestDiscDetail(username, token, cntry, date1, date2) {
    const params = '?code='  + code
                 + '&date1=' + encodeURIComponent(date1)
                 + '&date2=' + encodeURIComponent(date2)

    const options = {
        method: 'GET',
        headers: getHeaderAuth(username, token)
    }

    return dispatch => {
        fetch(URL.DISC + '/' + cntry + params, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_DISC,
                                    discs:json.discs}))
            .catch(error => {
                console.log('error', error)
            })
    }
}

