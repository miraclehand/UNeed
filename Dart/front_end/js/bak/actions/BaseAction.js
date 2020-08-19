import * as ACTION_TYPE from '../constants/action-types';

export function changeCntry(cntry) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.CHANGE_CNTRY, cntry:cntry});
    }
}
