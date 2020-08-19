import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';

export function requestListStock(cntry) {
    return dispatch => {
        fetch(URL.LIST_STOCK + '/' + cntry)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_LIST_STOCK,
                                    list_stock:json.stocks}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

export function requestListStdDisc(cntry) {
    return dispatch => {
        fetch(URL.LIST_STD_DISC + '/' + cntry)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_LIST_STD_DISC,
                                    list_std_disc:json.list_std_disc}))
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}
