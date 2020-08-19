import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';

export function requestListStock(cntry) {
    return dispatch => {
        dispatch({type: ACTION_TYPE.REQUEST_LIST_STOCK});
        fetch(URL.LIST_STOCK + '/' + cntry)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_LIST_STOCK, stocks:json.stocks}));
    }
}

