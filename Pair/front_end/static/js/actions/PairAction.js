import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';

export function requestPickedPair(cntry) {
    return dispatch => {
        fetch(URL.PICKED_PAIR + '/' + cntry)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_PICKED_PAIR,
                                    cntry: cntry,
                                    picked_pairs:json.picked_pairs}));
    }
}
