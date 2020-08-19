import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import signout from './AuthAction';
import { getHeaderAuth } from './FetchOptions';

export function requestProgress(username, token, cntry) {
    const options = {
        method: 'GET',
        headers: getHeaderAuth(username, token),
    }

    return dispatch => {
        fetch(URL.PROGRESS + '/' + cntry + '/' + username, options)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_PROGRESS,
                                    username: json.username,
                                    seconds:  json.seconds,
                                    progress: json.progress}));
    }
}

export function requestStopProgress(username, token, cntry) {
    const options = {
        method: 'DELETE',
        headers: getHeaderAuth(username, token),
    }

    return (dispatch, getState, api) => {
        fetch(URL.PROGRESS + '/' + cntry + '/' + username, options)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_PROGRESS,
                                    username:json.username,
                                    seconds:  json.seconds,
                                    progress: json.progress}));
    }
}

