import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { getHeaderAuth } from './FetchOptions';

export function requestAsset(username, token) {
    const options = {
        method: 'GET',
        headers: getHeaderAuth(username, token)
    }

    return dispatch => {
        fetch(URL.ASSET + '/' + username, options)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_ASSET,
                                    username:json.username,
                                    budget:json.budget,
            }))
    }
}

export function requestPostAsset(username, token) {
    const options = {
        method: 'POST',
        headers: getHeaderAuth(username, token),
        body: JSON.stringify({budget:20000000})
    }

    return (dispatch, getState, api) => {
        fetch(URL.ASSET + '/' + username, options)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_ASSET,
                                    username:json.username,
                                    budget:json.budget,
            }))
    }
}

export function requestEntries(username, token, cntry) {
    const options = {
        method: 'GET',
        headers: getHeaderAuth(username, token)
    }

    return dispatch => {
        fetch(URL.TRADING + '/' + cntry + '/' + username, options)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_TRADING,
                                    username:json.username,
                                    entries:json.entries,
            }))
    }
}

export function requestOpenEntry(username, token, cntry, entry1, entry2) {
    const options = {
        method: 'POST',
        headers: getHeaderAuth(username, token),
        body: JSON.stringify({code1:entry1.code,
                              date1:entry1.date,
                              pos1: entry1.pos,
                              qty1: entry1.qty,
                              uv1:  entry1.uv,
                              code2:entry2.code,
                              date2:entry2.date,
                              pos2: entry2.pos,
                              qty2: entry2.qty,
                              uv2:  entry2.uv,
        })
    }

    return (dispatch, getState, api) => {
        fetch(URL.TRADING + '/' + cntry + '/' + username, options)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_TRADING,
                                    username:json.username,
                                    entries:json.entries,
            }))
    }
}

export function requestCloseEntry(username, token, cntry, entry_id) {
    const options = {
        method: 'DELETE',
        headers: getHeaderAuth(username, token),
        body: JSON.stringify({entry_id:entry_id,
        })
    }
    return (dispatch, getState, api) => {
        fetch(URL.TRADING + '/' + cntry + '/' + username, options)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_TRADING,
                                    username:json.username,
                                    entries:json.entries,
            }))
    }
}
