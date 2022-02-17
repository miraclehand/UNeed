import { combineReducers } from 'redux';
import { Platform } from 'react-native'
import * as ACTION_TYPE from '../constants/action-types';
//import authReducer from './persistReducer';
import * as SQLite from 'expo-sqlite';
import { getDisassembled } from '../util/textUtil';
import dayjs from 'dayjs';
import produce from 'immer';

const DB_NAME  = 'dart.db'
const DB_VERSION  = '0.1'

/* kr:korea, us:united states */
const initialBaseState = {
    cntry: 'kr',
    os: Platform.select({web:'web',android:'android',ios:'ios' }),
    navigation: null,
};

const initialUserState = {
    name     : null,
    email    : null,
    pushToken: null,
    level    : null,
};

const initialDBState = {
    dbName: DB_NAME,
    db: Platform.select({web:'web',android:'android',ios:'ios' }) === 'web'
            ? ''
            : SQLite.openDatabase(DB_NAME, DB_VERSION),
    metadata: {},
    stocks: [],
    std_discs: [],
    alerts: [],
    /*
    version: {},
    chat_id: '000000000000000000000000',
    */
};

const initialChatRoomState = {
    rooms: [],
};

const initialChatState = {
    chats: [],
};

const initialBalanceState = {
    est_acc: [],
    position: [],
};

const initialOrdersState = {
    orders: [],
};

/*
const initialAlertRoomState = {
    discs: [],
    last_disc: '',
    alert_cnt: 0,
};
*/

const initialCompanyState = {
    company: [],
};

const initialMessageState = {
    messages: [],
};

const initialUnitState = {
    id : 0,
    name : '',
    s_date : dayjs(new Date(dayjs().add(-1,'month'))).format('YYYY-MM-DD'),
    e_date : dayjs(new Date()).format('YYYY-MM-DD'),
    stocks: [],
    label: '',
    stock_codes: '',
    stock_names: '',
    std_disc: null,
    detail: {},
}

const initialWatchState = {
    watch  : initialUnitState,
    watchs : [],
};

const initialBadgeState = {
    count  : 0,
    badges : [],
};

const initialCandleState = {
    code : '',
    name : '',
    date1: '',
    date2: '',
    ohlcvs : [],
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

const userReducer = (state = initialUserState, action) => {
    switch (action.type) {
        case ACTION_TYPE.SET_AUTH_STATE:
            return Object.assign({}, state, {
                name      : action.name,
                email     : action.email,
                level     : action.level,
            });
        case ACTION_TYPE.SET_PUSH_TOKEN:
            return Object.assign({}, state, {
                pushToken : action.pushToken,
            });
        case ACTION_TYPE.SIGN_OUT:
            return Object.assign({}, state, initialUserState)
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
        case ACTION_TYPE.SET_NAVIGATION:
            return Object.assign({}, state, {
                navigation: action.navigation,
            });
        default:
            return state;
    }
}

/*
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
*/

const chatRoomReducer = (state = initialChatRoomState, action) => {
    let rooms

    switch (action.type) {
        case ACTION_TYPE.REQUEST_CHAT_ROOM:
            return Object.assign({}, state, initialChatRoomState);
        case ACTION_TYPE.RECEIVE_CHAT_ROOM:
            return Object.assign({}, state, {
                rooms: action.rooms
            });
        case ACTION_TYPE.UPSERT_CHAT_ROOM:
            if (state.rooms.length === 0) {
                return Object.assign({}, state, {
                    rooms: [action.room]
                });
            }
            const room = state.rooms.filter(room => room.watch_id === action.room.watch_id)[0]
            const badge = room.badge

            rooms = state.rooms.filter(room => room.watch_id !== action.room.watch_id)
            action.room.badge = action.room.badge + badge
            return Object.assign({}, state, {
                rooms: [action.room, ...rooms]
            });
        case ACTION_TYPE.POP_CHAT_ROOM:
            return Object.assign({}, state, {
                rooms: state.rooms.filter(room => room !== action.delRoom)
            });
        case ACTION_TYPE.UPDATE_BADGE:
            rooms = produce(state.rooms, draft => {
                const index = draft.findIndex(room => room.watch_id === action.watch_id)
                draft[index].badge =  0
            })
            return Object.assign({}, state, {
                rooms: rooms
            });
        default:
            return state;
    }
}

const chatReducer = (state = initialChatState, action) => {
    switch (action.type) {
        case ACTION_TYPE.REQUEST_CHAT:
            return Object.assign({}, state, initialChatState);
        case ACTION_TYPE.RECEIVE_CHAT:
            return Object.assign({}, state, {
                chats: action.chats
            });
        case ACTION_TYPE.UPSERT_CHAT:
            if (state.chats.length === 0) {
                return Object.assign({}, state, {
                    chats: [action.chat]
                });
            }

            if (action.chat.watch_id != state.chats[0].watch_id) {
                return state
            }

            return Object.assign({}, state, {
                chats: [...state.chats, action.chat]
            });
        case ACTION_TYPE.UPSERT_CHATS:
            return Object.assign({}, state, {
                chats: [...state.chats, ...action.chats]
            });
        case ACTION_TYPE.POP_CHAT:
            return Object.assign({}, state, {
                chats: state.chats.filter(chat => chat !== action.chat)
            });
        default:
            return state;
    }
}

const dbReducer = (state = initialDBState, action) => {
    let metadata;
    switch (action.type) {
        case ACTION_TYPE.INIT_DB:
            return state;
            /*
        case ACTION_TYPE.SET_VERSION:
            return Object.assign({}, state, {
                version: action.version,
            });
            */
        case ACTION_TYPE.SET_META_DATA:
            return Object.assign({}, state, {
                metadata:action.metadata
            });
        case ACTION_TYPE.SET_LAST_WATCH_ID:
            metadata = state.metadata
            metadata['last_watch_id'] = action.id
            return Object.assign({}, state, {
                metadata: metadata
            });
        case ACTION_TYPE.SET_LAST_SIMULA_ID:
            metadata = state.metadata
            metadata['last_simula_id'] = action.id
            return Object.assign({}, state, {
                metadata: metadata
            });
        case ACTION_TYPE.SET_VERSION:
            metadata = state.metadata
            metadata['stock_ver']    = action.version.stock_ver
            metadata['std_disc_ver'] = action.version.std_disc_ver
            return Object.assign({}, state, {
                metadata: metadata,
            });
        case ACTION_TYPE.SET_CHAT_ID:
            metadata = state.metadata
            metadata['last_chat_id'] = action.chat_id
            return Object.assign({}, state, {
                metadata: metadata,
            });
        case ACTION_TYPE.SET_STOCKS:
            return Object.assign({}, state, {
                stocks:action.stocks
            });
        case ACTION_TYPE.SET_STD_DISCS:
            return Object.assign({}, state, {
                std_discs:action.std_discs
            });
        case ACTION_TYPE.SET_ALERTS:
            return Object.assign({}, state, {
                alerts:action.alerts
            });
        default:
            return state;
    }
}

const companyReducer = (state = initialCompanyState, action) => {
    switch (action.type) {
        case ACTION_TYPE.REQUEST_COMPANY:
            return Object.assign({}, state, initialCompanyState);
        case ACTION_TYPE.RECEIVE_COMPANY:
            console.log(action.company)
            return Object.assign({}, state, {
                company: action.company,
            });
        default:
            return state;
    }
}

const unitReducer = (state = initialUnitState, action) => {
    switch (action.type) {
        case ACTION_TYPE.INIT_UNIT:
            return Object.assign({}, state, initialUnitState);
        case ACTION_TYPE.SET_UNIT_ID:
            return Object.assign({}, state, {
                id: action.id,
            });
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
            if (initialBaseState.os !== 'web') {
                action.watchs.map( watch => {
                    watch['std_disc'] = {}
                    watch['std_disc']['id']         = watch.std_disc_id
                    watch['std_disc']['report_nm']  = watch.std_disc_report_nm
                    watch['std_disc']['report_dnm'] = watch.std_disc_report_dnm
                })
            }
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

const balanceReducer = (state = initialBalanceState, action) => {
    switch (action.type) {
        case ACTION_TYPE.RECEIVE_HTS_BALANCE:
            return Object.assign({}, state, {
                est_acc: action.balance.est_acc,
                position: action.balance.position,
            });
        default:
            return state;
    }
}

const ordersReducer = (state = initialOrdersState, action) => {
    switch (action.type) {
        case ACTION_TYPE.RECEIVE_HTS_ORDERS:
            return Object.assign({}, state, {
                orders: action.orders,
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
            console.log('RECEIVE OHLCV1', action.code)
            return Object.assign({}, state, {
                code: action.code,
                name: action.name,
                date1: action.date1,
                date2: action.date2,
                ohlcvs: action.ohlcvs,
            });
            /*
            return Object.assign({}, state, {
                ...state.arr_ohlcvs, [action.code]: action.ohlcvs,
                ohlcvs: action.ohlcvs

            });
            */
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
/*
const messageReducer = (state = initialMessageState, action) => {
    switch (action.type) {
        case ACTION_TYPE.REQUEST_MESSAGE:
            return Object.assign({}, state, initialMessageState);
        case ACTION_TYPE.RECEIVE_MESSAGE:
            return Object.assign({}, state, {
                messages: action.messages,
            });
        case ACTION_TYPE.UPSERT_MESSAGE:
            if (state.messages.length === 0) {
                return Object.assign({}, state, {
                    messages: [action.message]
                });
            }
            return Object.assign({}, state, {
                messages: [...state.messages, action.message]
            });
        default:
            return state;
    }
}
*/

const simulaReducer = (state = initialSimulaState, action) => {
    switch (action.type) {
        case ACTION_TYPE.INIT_SIMULA:
            return Object.assign({}, state, initialSimulaState);
        case ACTION_TYPE.RECEIVE_SIMULA:
            return Object.assign({}, state, {
                simulas: action.simulas,
            });
        case ACTION_TYPE.POP_SIMULA:
            return Object.assign({}, state, {
                simulas:state.simulas.filter(simula=>simula!==action.delSimula)
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

const badgeReducer = (state = initialBadgeState, action) => {
    let badge

    switch (action.type) {
        case ACTION_TYPE.INC_BADGE:
            badge= state.badges[action.watch_id]
            if (badge=== undefined) badge= 0

            return Object.assign({}, state, {
                count :  state.count + 1,
                badges: {...state.badges, [action.watch_id]:badge+ 1 }
            });
        case ACTION_TYPE.CLR_BADGE:
            badge= state.badges[action.watch_id]
            if (badge=== undefined) badge= 0

            return Object.assign({}, state, {
                count :  state.count - badge,
                badges: {...state.badges, [action.watch_id]:0 }
            });
        default:
            return state;
    }
}

const rootReducer = combineReducers({
    baseReducer,
    userReducer,
    dbReducer,
    chatRoomReducer,
    chatReducer,
    //alertReducer,
    //alertRoomReducer,
    companyReducer,
    candleReducer,
    //messageReducer,
    watchReducer,
    simulaReducer,
    unitReducer,
    balanceReducer,
    ordersReducer,
});

export default rootReducer;

