import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';

function regex1(text) {
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

function get_value(key, text) {
    let s_idx, e_idx, value

    s_idx = text.search(key) + key.length;
    e_idx = s_idx + text.substring(s_idx,s_idx+50).search(',')
    value = text.substring(s_idx, e_idx).replaceAll('"','').trim()
    return unescape(value.replaceAll('\\','%'))
}

function regex(text) {
    let value, it

    let candle = {}

    candle['code'] = get_value('"code":', text)
    candle['name'] = get_value('"name":', text)

    console.log(candle)

    return text.split('{').filter(line => line.includes('date'))
        .reduce( (acc, line) => {
            line = line.replace(/"/g,'')
            value = line.trim().split(',')
            console.log(line)
            console.log(value)
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
    */
}

export function requestCandle(email, token, cntry, code, date1, date2) {
    console.log(URL.CANDLE)
        /* 'Access-Control-Allow-Origin':'*' */
    return dispatch => {
        fetch(URL.CANDLE)
        /*
        fetch(URL.CANDLE, {method:'GET', mode:'cors', 
        cache: 'no-cache',
        credentials: 'same-origin',
         redirect: 'follow', 
         referrer: 'no-referrer',
          'Content-Type': 'application/json',
           Accept: 'application/json',
        headers: {'origin':'http://125.183.209.195:19006'  ,
        }})
        */
            .then(res => {
                console.log('rrres1', res)
                if (res.ok) return res.text();
                else throw new Error('unauthorized user');
            })
            .then(text => {
                const ohlcvs = text
                //const ohlcvs = regex(text)
                //a[code] = regex(text)
                const candle = regex(text)
                console.log(candle)
                dispatch({type: ACTION_TYPE.RECEIVE_OHLCV,
                            code,
                            code,
                            date1,
                            date2,
                            ohlcvs})
            })
            .catch(error => {
                alert(error)
                console.log('error', error)
                dispatch({type: ACTION_TYPE.SIGN_OUT})
                dispatch({type: ACTION_TYPE.RECEIVE_OHLCV,
                            code,
                            code,
                            date1,
                            date2,
                            ohlcvs: 'errorrrrr'})
            })
    }
}

