import { combineReducers } from 'redux';
import { Platform } from 'react-native'
import * as ACTION_TYPE from '../constants/action-types';
//import authReducer from './persistReducer';
import * as SQLite from 'expo-sqlite';
import { getDisassembled } from '../util/search';
import dayjs from 'dayjs';

const DB_NAME  = 'dart.db'
const VERSION  = '0.1'

const initialInitState = {
    isLoadingComplete: false,
};

/* kr:korea, us:united states */
const initialBaseState = {
    cntry: 'kr',
    os: '',
};

const initialUserState = {
    name     : null,
    email    : null,
    pushToken: null,
    level    : null,
};

const initialDBState = {
    dbName: DB_NAME,
    version: VERSION,
    db: Platform.select({web:'web',android:'android',ios:'ios' }) === 'web'
            ? ''
            : SQLite.openDatabase(DB_NAME, VERSION),
};

const initialAlertState = {
    rooms: [],
};

const initialAlertRoomState = {
    discs: [],
    last_disc: '',
    alert_cnt: 0,
};

const initialCorpState = {
    corps: [],
};

const initialUserMessagesState = {
    messages: [],
};

const initialListState = {
    list_stock   : [],
    list_std_disc: [],
};

const initialUnitState = {
    name : '',
    s_date : new Date(dayjs().add(-1,'year')),
    e_date : new Date(),
    stocks: [],
    stock_codes: '',
    stock_names: '',
    std_disc: '',
    detail: {},
}

const initialWatchState = {
    watch  : initialUnitState,
    watchs : [],
};

const initialCandleState = {
    ohlcvs: {},
};

const initialChartState = {
    options: {
        chart: {
            type: 'candlestick',
            height: 350
        },
        title: {
            text: 'CandleStick Chart',
            align: 'left'
        },
        xaxis: {
            type: 'datetime'
        },
        yaxis: {
            tooltip: {
                enabled: true
            }
        }
    },
    ohlcvs: [],
};

const initialSimulaState = {
    simula  : initialUnitState,
    simulas : [],
};

const initReducer = (state = initialInitState, action) => {
    switch (action.type) {
        case ACTION_TYPE.FINISH_LOADING:
            return Object.assign({}, state, {
                isLoadingComplete: true,
            });
        default:
            return state;
    }
}

const userReducer = (state = initialUserState, action) => {
    switch (action.type) {
        case ACTION_TYPE.SET_USER:
            return Object.assign({}, state, {
                name      : action.name,
                email     : action.email,
                pushToken : action.pushToken,
                level     : action.level,
            });
    default:
        return state;
    }
}

/*
const initialUserState = {
    username: '',
    expoPushToken: '',
    level: 0,
    authState: null,
};
const authReducer = (state = initialAuthState, action) => {
    switch (action.type) {
        case ACTION_TYPE.LOAD_EXPO_PUSH_TOKEN:
            return Object.assign({}, state, {
                expoPushToken: action.expoPushToken,
            });
        case ACTION_TYPE.LOAD_AUTH_STATE:
            return Object.assign({}, state, {
               // username: localStorage.getItem('yepark_username'),
               // token: localStorage.getItem('yepark_token'),
               // level: localStorage.getItem('yepark_level'),
               // failed: false,
                authState: action.authState,
            });
        case ACTION_TYPE.SUCCESS_SIGN_IN:
        case ACTION_TYPE.SUCCESS_SIGN_ON:
        case ACTION_TYPE.SUCCESS_FREE_PASS:
            localStorage.setItem('yepark_username',action.username);
            localStorage.setItem('yepark_token',action.token);
            localStorage.setItem('yepark_level',action.level);
            return Object.assign({}, state, {
                username: action.username,
                token: action.token,
                level: action.level,
                failed: false,
            });
        case ACTION_TYPE.FAIL_SIGN_IN:
        case ACTION_TYPE.FAIL_SIGN_ON:
            localStorage.removeItem('yepark_username');
            localStorage.removeItem('yepark_token');
            localStorage.removeItem('yepark_level');
            return Object.assign({}, state, {
                username: '',
                token: '',
                level: 0,
                failed: true,
            });
        case ACTION_TYPE.SIGN_OUT:
        case ACTION_TYPE.FAIL_FREE_PASS:
            localStorage.removeItem('yepark_username');
            localStorage.removeItem('yepark_token');
            localStorage.removeItem('yepark_level');
            return Object.assign({}, state, initialAuthState)
        default:
            return state;
    }
}

const userReducer = (state = initialUserState, action) => {
    switch (action.type) {
        case ACTION_TYPE.REQUEST_USER:
            return Object.assign({}, state, initialUserState);
        case ACTION_TYPE.RECEIVE_USER:
            return Object.assign({}, state, {
                username: action.user.username,
                password: action.user.password,
                token   : action.user.token,
                level   : action.user.level,
            });
    default:
        return state;
    }
}
*/

const baseReducer = (state = initialBaseState, action) => {
    switch (action.type) {
        case ACTION_TYPE.CHANGE_CNTRY:
            return Object.assign({}, state, {
                cntry: action.cntry,
            });
        case ACTION_TYPE.CHANGE_OS:
            return Object.assign({}, state, {
                os: action.os,
            });
        default:
            return state;
    }
}

const alertReducer = (state = initialAlertState, action) => {
    switch (action.type) {
        case ACTION_TYPE.REQUEST_ALERT:
            return Object.assign({}, state, initialAlertState);
        case ACTION_TYPE.RECEIVE_ALERT:
            return Object.assign({}, state, {
                rooms: action.rooms,
            });
        default:
            return state;
    }
}

const alertRoomReducer = (state = initialAlertRoomState, action) => {
    switch (action.type) {
        case ACTION_TYPE.REQUEST_ALERT_ROOM:
            return Object.assign({}, state, initialAlertRoomState);
        case ACTION_TYPE.RECEIVE_ALERT_ROOM:
            return Object.assign({}, state, {
                discs: action.discs,
            });
        case ACTION_TYPE.PUSH_DISC:
            return Object.assign({}, state, {
                discs: [...state.discs, action.new_disc]
            });
        default:
            return state;
    }
}

const dbReducer = (state = initialDBState, action) => {
    switch (action.type) {
        case ACTION_TYPE.INIT_DB:
            return state;
        default:
            return state;
    }
}

const corpReducer = (state = initialCorpState, action) => {
    switch (action.type) {
        case ACTION_TYPE.REQUEST_CORP:
            return Object.assign({}, state, initialCorpState);
        case ACTION_TYPE.RECEIVE_CORP:
            return Object.assign({}, state, {
                corps: action.corps,
            });
    default:
        return state;
    }
}

const unitReducer = (state = initialUnitState, action) => {
    switch (action.type) {
        case ACTION_TYPE.INIT_UNIT:
            return Object.assign({}, state, initialUnitState);
        case ACTION_TYPE.SET_UNIT_NAME:
            return Object.assign({}, state, {
                name: action.name,
            });
        case ACTION_TYPE.SET_UNIT_SDATE:
            return Object.assign({}, state, {
                s_date: action.s_date,
            });
        case ACTION_TYPE.SET_UNIT_EDATE:
            return Object.assign({}, state, {
                e_date: action.e_date,
            });
        case ACTION_TYPE.SET_UNIT_STOCKS:
            let stock_codes = ''
            let stock_names = ''
            action.stocks.map(stock => {
                stock_codes = stock_codes + stock.code + ' '
                stock_names = stock_names + stock.name + ' '
            })
            return Object.assign({}, state, {
                stocks: action.stocks,
                stock_codes: stock_codes.trim(),
                stock_names: stock_names.trim(),
            });
        case ACTION_TYPE.SET_UNIT_STD_DISC:
            return Object.assign({}, state, {
                std_disc: action.std_disc,
            });
        case ACTION_TYPE.SET_UNIT_DETAIL:
            return Object.assign({}, state, {
                detail: action.detail,
            });
    default:
        return state;
    }
}

const watchReducer = (state = initialWatchState, action) => {
    switch (action.type) {
        case ACTION_TYPE.INIT_WATCH:
            return Object.assign({}, state, initialWatchState);
        case ACTION_TYPE.RECEIVE_WATCHS:
            return Object.assign({}, state, {
                watchs: action.watchs,
            });
        case ACTION_TYPE.POP_WATCH:
            return Object.assign({}, state, {
                watchs: state.watchs.filter(watch =>watch !== action.delWatch)
            });
        case ACTION_TYPE.PUSH_WATCH:
            if (state.watchs.length === 0) {
                return Object.assign({}, state, {
                    watchs: [action.newWatch]
                });
            }
            return Object.assign({}, state, {
                watchs: [...state.watchs, action.newWatch]
            });
    default:
        return state;
    }
}

const listReducer = (state = initialListState, action) => {
    switch (action.type) {
        case ACTION_TYPE.INIT_LIST:
            return Object.assign({}, state, initialListState);
        case ACTION_TYPE.RECEIVE_LIST_STOCK:
            return Object.assign({}, state, {
                list_stock:[{code:'000000',name:'전체', dname:getDisassembled('전체') },
                ...action.list_stock]
            });
        case ACTION_TYPE.RECEIVE_LIST_STD_DISC:
            return Object.assign({}, state, {
                list_std_disc:action.list_std_disc
            });
    default:
        return state;
    }
}

const candleReducer = (state = initialCandleState, action) => {
    switch (action.type) {
        case ACTION_TYPE.REQUEST_OHLCV:
            return Object.assign({}, state, initialCandleState);
        case ACTION_TYPE.RECEIVE_OHLCV:
            return Object.assign({}, state, {
                ...state.ohlcvs, [action.code]: action.ohlcvs
            });
            /*
            return Object.assign({}, state, {
                ohlcvs: [{data : action.ohlcvs.map((o, i) => {
                                return {
                                    x: o.date,
                                    y:[o.open, o.high, o.low, o.close],
                                }
                            })
                        }]
            });
            */
            return Object.assign({}, state, {
                ohlcvs: action.ohlcvs.map((o, i) => {
                                return (
                                    [o.date, o.low, o.open, o.close, o.high]
                                )
                            })
                        
            });
    default:
        return state;
    }
}

const chartReducer = (state = initialChartState, action) => {
    switch (action.type) {
        case ACTION_TYPE.REQUEST_OHLCV:
            return Object.assign({}, state, initialCandleState);
        case ACTION_TYPE.RECEIVE_OHLCV:
            if (!action.ohlcvs) {
                return Object.assign({}, state, {
                    ohlcvs: [],
                });
            }
            /*
            return Object.assign({}, state, {
                ohlcvs: [{data : action.ohlcvs.map((o, i) => {
                                return {
                                    x: o.date,
                                    y:[o.open, o.high, o.low, o.close],
                                }
                            })
                        }]
            });
            */
            return Object.assign({}, state, {
                ohlcvs: action.ohlcvs.map((o, i) => {
                                return (
                                    [o.date, o.low, o.open, o.close, o.high]
                                )
                            })
                        
            });
    default:
        return state;
    }
}

const userMessagesReducer = (state = initialUserMessagesState, action) => {
    switch (action.type) {
        case ACTION_TYPE.REQUEST_USER_MESSAGES:
            return Object.assign({}, state, initialUserMessagesState);
        case ACTION_TYPE.RECEIVE_USER_MESSAGES:
            return Object.assign({}, state, {
                messages: action.discs,
            });
    default:
        return state;
    }
}

const simulaReducer = (state = initialSimulaState, action) => {
    switch (action.type) {
        case ACTION_TYPE.INIT_SIMULA:
            return Object.assign({}, state, initialSimulaState);
        case ACTION_TYPE.RECEIVE_SIMULA:
            return Object.assign({}, state, {
                simulas: action.simulas,
            });
        case ACTION_TYPE.PUSH_SIMULA:
            if (!state.simulas) {
                return Object.assign({}, state, {
                    simula:  action.newSimula,
                    simulas: [action.newSimula]
                });
            }
            return Object.assign({}, state, {
                simula:  action.newSimula,
                simulas: [...state.simulas, action.newSimula]
            });
        case ACTION_TYPE.SET_SIMULA:
            return Object.assign({}, state, {
                simulas: {...state.simulas, [action.index]:action.simula }
            });
    default:
        return state;
    }
}

const rootReducer = combineReducers({
    initReducer,
    baseReducer,
    userReducer,
    dbReducer,
    alertReducer,
    alertRoomReducer,
    corpReducer,
    candleReducer,
    userMessagesReducer,
    watchReducer,
    listReducer,
    simulaReducer,
    unitReducer,
});

export default rootReducer;

