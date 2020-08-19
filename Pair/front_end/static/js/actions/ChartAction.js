import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import signout from './AuthAction';
import { getHeaderAuth } from './FetchOptions';

export function requestChart(username, token, cntry, date1, date2, code1, code2){
    const params = '?code1=' + encodeURIComponent(code1)
                 + '&code2=' + encodeURIComponent(code2)
                 + '&date1=' + encodeURIComponent(date1)
                 + '&date2=' + encodeURIComponent(date2)

    const options = {
        method: 'GET',
        headers: getHeaderAuth(username, token)
    }

    return dispatch => {
        fetch(URL.COMPANY + '/' + cntry + '/' + code1, options)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_COMPANY,
                                    index:0,
                                    company:json.company}))
        fetch(URL.COMPANY + '/' + cntry + '/' + code2, options)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_COMPANY,
                                    index:1,
                                    company:json.company}));

        fetch(URL.NORM_CHART + '/' + cntry + params, options)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_NORM_CHART,
                                    index: 0,
                                    img_src:json.img_src}));
        fetch(URL.LOG_CHART + '/' + cntry + params, options)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_LOG_CHART,
                                    index: 1,
                                    img_src:json.img_src}));
        fetch(URL.HIST_CHART + '/' + cntry + params, options)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_HIST_CHART,
                                    index: 2,
                                    img_src:json.img_src}));
        fetch(URL.VOL_CHART + '/' + cntry + params, options)
            .then(res => res.json())
            .then(json => dispatch({type: ACTION_TYPE.RECEIVE_VOL_CHART,
                                    index: 3,
                                    img_src:json.img_src}));
    }
}

export function clearChart() {
    return dispatch => {
        dispatch({type: ACTION_TYPE.CLEAR_CHART});
    }
}
