import * as ACTION_TYPE from '../constants/action-types';

export function finishLoading() {
    return dispatch => {
        dispatch({type: ACTION_TYPE.FINISH_LOADING});
    }
}
