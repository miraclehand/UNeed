import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { getHeaderAuth } from './FetchOptions';
import { exec_query, select_query } from '../util/dbUtil';

export function requestBalance(email, token) {
    const options = {
        method: 'GET',
        headers: getHeaderAuth(email, token),
    }

    return dispatch => {
        fetch(URL.HTS_BALANCE + '/0', options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_HTS_BALANCE,
                                    balance:JSON.parse(json.balance)}))
            .catch(error => {
                console.log('error', error)
            })
    }
}

export function requestOrders(email, token, chegb) {
    const options = {
        method: 'GET',
        headers: Object.assign({}, getHeaderAuth(email, token), {'chegb':chegb})
    }
    return dispatch => {
        fetch(URL.HTS_ORDER, options)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('login fail');
            })
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_HTS_ORDERS,
                                    orders:JSON.parse(json.orders)}))
            .catch(error => {
                console.log('error', error)
            })
    }
}

function requestPostOrder(order_type, code, qty, price) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order_type : order_type,
                               code       : code,
                               qty        : qty.replace(',',''),
                               price      : price.replace(',',''),
        })
    }
    return dispatch => {
        fetch(URL.HTS_ORDER, requestOptions)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('login fail');
            })
            .then(json => {
                console.log(json)
                alert(json.message)
            })
            .catch(error => {
                console.log('error', error)
            })
    }
}

function requestPutOrder(order_type, code, qty, price, ordno) {
    const requestOptions = {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order_type : order_type,
                               code       : code,
                               qty        : qty.replace(',',''),
                               price      : price.replace(',',''),
                               ordno      : ordno.replace(',',''),
        })
    }
    return dispatch => {
        fetch(URL.HTS_ORDER, requestOptions)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('login fail');
            })
            .then(json => {
                console.log(json)
                alert(json.message)
            })
            .catch(error => {
                console.log('error', error)
            })
    }
}

function requestDeleteOrder(order_type, code, qty, ordno) {
    const requestOptions = {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order_type : order_type,
                               code       : code,
                               qty        : qty.replace(',',''),
                               ordno      : ordno.replace(',',''),
        })
    }
    return dispatch => {
        fetch(URL.HTS_ORDER, requestOptions)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('login fail');
            })
            .then(json => {
                console.log(json)
                alert(json.message)
            })
            .catch(error => {
                console.log('error', error)
            })
    }
}

export function requestBuy(code, qty, price) {
    return requestPostOrder('2', code, qty, price)
}

export function requestSell(code, qty, price) {
    return requestPostOrder('1', code, qty, price)
}

export function requestModify(code, qty, price, ordno) {
    return requestPutOrder('3', code, qty, price, ordno)
}

export function requestCancel(code, qty, ordno) {
    return requestDeleteOrder('0', code, qty, ordno)
}
