import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';

export function cacheMetadata(metadata) {
    return dispatch => {
        return dispatch({type:ACTION_TYPE.SET_META_DATA, metadata})
    }
}
/*
FIXME
export function cacheVersion(version) {
    return dispatch => {
        return dispatch({type:ACTION_TYPE.SET_VERSION, version})
    }
}

export function cacheChatId(chat_id) {
    return dispatch => {
        return dispatch({type:ACTION_TYPE.SET_CHAT_ID, chat_id})
    }
}
*/

export function cacheStocks(stocks) {
    return dispatch => {
        return dispatch({type:ACTION_TYPE.SET_STOCKS, stocks})
    }
}

export function cacheStdDiscs(std_discs) {
    return dispatch => {
        return dispatch({type:ACTION_TYPE.SET_STD_DISCS, std_discs})
    }
}

export function cacheChatRooms(rooms) {
    return dispatch => {
        return dispatch({type:ACTION_TYPE.RECEIVE_CHAT_ROOM, rooms})
    }
}
