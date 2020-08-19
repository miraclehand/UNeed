import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';

export function popup_close() {
    return dispatch => {
        dispatch({type: ACTION_TYPE.POPUP_CLOSE});
    }
}

