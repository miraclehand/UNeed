import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { getDisassembled } from '../util/textUtil';
import { reset_stock, reset_std_disc, db_update_version } from '../device/db';

export function requestStocks(os, db, cntry) {
    return dispatch => {
        fetch(URL.STOCKS + '/' + cntry)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => {
                const stocks = [{code:'000000',name:'전체', dname:getDisassembled('>전체') }, ...json.stocks]

                if (os !== 'web') {
                    reset_stock(db, stocks)
                }
                dispatch({type: ACTION_TYPE.SET_STOCKS, stocks})
            })
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

export function requestStdDiscs(os, db, cntry) {
    return dispatch => {
        fetch(URL.STD_DISCS + '/' + cntry)
            .then(res => {
                if (res.ok) return res.json();
                else throw new Error('unauthorized user');
            })
            .then(json => {
                if (os !== 'web') {
                    reset_std_disc(db, json.std_discs)
                }
                dispatch({type: ACTION_TYPE.SET_STD_DISCS,
                                std_discs:json.std_discs})
            })
            .catch(error => {
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

export function requestVersion(os, db, cntry, metadata) {
    let d1, d2

    return dispatch => {
        fetch(URL.VERSION)
            .then(res => {
                return res.json();
            })
            .then(json => {
                const server_version = json.version
                if (os === 'web') {
                    requestStocks(os, db, cntry)
                    requestStdDiscs(os, db, cntry)
                } else {
                    d1 = Date.parse(metadata.stock_ver)
                    d2 = Date.parse(server_version.stock_ver)
                    if (isNaN(d1) && d1 < d2) {
                        requestStocks(os, db, cntry)
                    }

                    d1 = Date.parse(metadata.std_disc_ver)
                    d2 = Date.parse(server_version.std_disc_ver)
                    if (isNaN(d1) && d1 < d2) {
                        requestStdDiscs(os, db, cntry)
                    }
                    db_update_version(db, server_version)
                }
                return dispatch({type: ACTION_TYPE.SET_VERSION,
                                 version:server_version})
            })
    }
}
