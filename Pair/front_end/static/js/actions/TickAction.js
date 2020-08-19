import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';

export function requestTick(cntry, code) {
    return dispatch => {
        fetch(URL.TICK + '/' + cntry + '/' + encodeURIComponent(code))
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_TICK,
                                    tick: json.tick}));
    }
}
