import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
//import { saveAuthState } from '../device/db';

export function incBadge(watch_id) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.INC_BADGE, watch_id: watch_id });
    }
}

export function clrBadge(watch_id) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.CLR_BADGE, watch_id: watch_id });
    }
}
