import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { getHeaderAuth } from './FetchOptions';

export function requestStrainer(username, token, cntry) {
    const options = {
        method: 'GET',
        headers: getHeaderAuth(username, token),
    }

    return dispatch => {
        fetch(URL.STRAINER + '/' + cntry + '/' + username, options)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_STRAINER,
                                    username: json.username,
                                    strainers: json.strainers}));
    }
}

export function requestPostStrainer(username, token, cntry, strainer) {
    const options = {
        method: 'POST',
        headers: getHeaderAuth(username, token),
        body: JSON.stringify({strainer:strainer, })
    }

    return (dispatch, getState, api) => {
        dispatch({type: ACTION_TYPE.REQUEST_STRAINER})
        fetch(URL.STRAINER + '/' + cntry + '/' + username, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error(res.statusText);
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_STRAINER,
                                    username: json.username,
                                    strainers: json.strainers}))
            .catch(error => {
                 dispatch({type: ACTION_TYPE.POPUP_OPEN,
                           title: 'Save Strainer',
                           content: error.toString()})
            });
    }
}

export function requestDeleteStrainer(username, token, cntry, strainer) {
    const options = {
        method: 'DELETE',
        headers: getHeaderAuth(username, token),
        body: JSON.stringify({strainer:strainer, })
    }

    return (dispatch, getState, api) => {
        dispatch({type: ACTION_TYPE.REQUEST_STRAINER})
        fetch(URL.STRAINER + '/' + cntry + '/' + username, options)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_STRAINER,
                                    username: json.username,
                                    strainers: json.strainers}));
    }
}
