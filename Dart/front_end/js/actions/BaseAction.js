import * as ACTION_TYPE from '../constants/action-types';

export function changeCntry(cntry) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.CHANGE_CNTRY, cntry});
    }
}

export function setNavigation(navigation) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.SET_NAVIGATION, navigation});
    }
}

