import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { getHeaderAuth } from './FetchOptions';

export function initUnit() {
    return dispatch => {
        dispatch({type: ACTION_TYPE.INIT_UNIT});
    }
}

export function setUnitName(name) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.SET_UNIT_NAME, name});
    }
}

export function setUnitSDate(s_date) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.SET_UNIT_SDATE, s_date});
    }
}

export function setUnitEDate(e_date) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.SET_UNIT_EDATE, e_date});
    }
}

export function setUnitStocks(stocks) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.SET_UNIT_STOCKS, stocks});
    }
}

export function setUnitStdDisc(std_disc) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.SET_UNIT_STD_DISC, std_disc});
    }
}

export function setUnitDetail(detail) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.SET_UNIT_DETAIL, detail});
    }
}
