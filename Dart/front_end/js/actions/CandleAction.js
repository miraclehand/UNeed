import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';

function regex(text) {
    let value, it

    return text.split('\n').filter(line => line.includes('<item data='))
        .reduce( (acc, line) => {
            line = line.replace('<item data=','')
                       .replace('/>','')
                       .replace(/"/g,'')
            value = line.trim().split('|')
            if (value.length === 6) {
                it = {'date' :value[0],
                      'open' :value[1],
                      'high' :value[2],
                      'low'  :value[3],
                      'close':value[4],
                      'value':value[5],
                      'log'  :Math.log(value[4]),
                }
                return {...acc, [it.date]:it }
            }
        },{})
/*
    return text.split('\n').filter(line => line.includes('<item data='))
        .map(line => {
            line = line.replace('<item data=','')
                       .replace('/>','')
                       .replace(/"/g,'')
            value = line.trim().split('|')
            if (value.length === 6) {
                return {'date' :value[0],
                        'open' :value[1],
                        'high' :value[2],
                        'low'  :value[3],
                        'close':value[4],
                        'value':value[5],
                        'log'  :Math.log(value[4]),
                }
            }
        })
        */
}

export function requestCandle(code) {
    return dispatch => {
        fetch(URL.CANDLE + '&symbol=' + code + '&count=' + 300)
            .then(res => {
                if (res.ok) return res.text();
                else throw new Error('unauthorized user');
            })
            .then(text => {
                const ohlcvs = regex(text)
                //a[code] = regex(text)
                dispatch({type: ACTION_TYPE.RECEIVE_OHLCV,
                            code,
                            ohlcvs})
            })
            .catch(error => {
                alert(error)
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
            })
    }
}

