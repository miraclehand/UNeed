import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import signout from './AuthAction';
import { getHeaderAuth } from './FetchOptions';

export function requestSimula(username, token, cntry) {
    const options = {
        method: 'GET',
        headers: getHeaderAuth(username, token),
    }
    return dispatch => {
        fetch(URL.SIMULA + '/' + cntry + '/' + username, options)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_SIMULA,
                                    username: json.username,
                                    simulas: json.simulas}));
    }
}

export function requestPostSimula(username, token, cntry, strainer) {
    const date1 = strainer['date1']
    const date2 = strainer['date2']

    const options = {
        method: 'POST',
        headers: getHeaderAuth(username, token),
        body: JSON.stringify({
            date1: date1,
            date2: date2,
            strainer:strainer,
        })
    }

    return (dispatch, getState, api) => {
        dispatch({type: ACTION_TYPE.REQUEST_SIMULA})
        fetch(URL.SIMULA + '/' + cntry + '/' + username, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error(res.statusText);
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_SIMULA,
                                    username: json.username,
                                    simulas:json.simulas}))
            .catch(error => {
                dispatch({type: ACTION_TYPE.POPUP_OPEN,
                          title: 'Run Simulation',
                          content: error.toString()})
            });
    }
}

