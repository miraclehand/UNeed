import { combineReducers } from 'redux';
import * as ACTION_TYPE from '../constants/action-types';

/* kr:korea, us:united states */
const initialBaseState = {
    cntry: 'kr',
};

const initialChartState = {
    charts: [],
    companies: [],
};

const initialPairState = {
    node_pairs: {},
    picked_pairs: {},
};

const initialSimulaState = {
    simulas: [],
};

const initialStockState = {
    stocks: [],
};

const initialAuthState = {
    username: '',
    token: '',
    level: 0,
    failed: false,
};

const initialAssetState = {
    username: '',
    budget:0,
};

const initialStrainerState = {
    username: '',
    strainers: [],
};

const initialTradingState = {
    username: '',
    entries:[],
};

const initialTickState = {
    ticks: {},
};

const initialStrategyState = {
    username: '',
    seconds: 0,
    progress: 100,
};

const initialPopupState = {
    open: false,
    title: '',
    content: '',
};

const initialCalendarState = {
    date: '',
}

const stockReducer = (state = initialStockState, action) => {
    switch (action.type) {
        case ACTION_TYPE.REQUEST_LIST_STOCK:
            return Object.assign({}, state, initialStockState);
        case ACTION_TYPE.RECEIVE_LIST_STOCK:
            return Object.assign({}, state, {
                stocks: action.stocks,
            });
        default:
            return state;
    }
}

const authReducer = (state = initialAuthState, action) => {
    switch (action.type) {
        case ACTION_TYPE.LOAD_AUTH:
            return Object.assign({}, state, {
                username: localStorage.getItem('yepark_username'),
                token: localStorage.getItem('yepark_token'),
                level: localStorage.getItem('yepark_level'),
                failed: false,
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

const chartReducer = (state = initialChartState, action) => {
    switch (action.type) {
        case ACTION_TYPE.RECEIVE_NORM_CHART:
        case ACTION_TYPE.RECEIVE_LOG_CHART:
        case ACTION_TYPE.RECEIVE_HIST_CHART:
        case ACTION_TYPE.RECEIVE_VOL_CHART:
            return Object.assign({}, state, {
                charts: Object.assign({}, state.charts, {[action.index]:action.img_src}),
            });
        case ACTION_TYPE.RECEIVE_COMPANY:
            return Object.assign({}, state, {
                companies: Object.assign({}, state.companies, {[action.index]:action.company}),
            });
        case ACTION_TYPE.CLEAR_CHART:
            return Object.assign({}, state, initialChartState)
        default:
            return state;
    }
}

const pairReducer = (state = initialPairState, action) => {
    switch (action.type) {
        case ACTION_TYPE.RECEIVE_NODE_PAIR:
            let node_pairs = Object.assign({}, state.node_pairs)

            node_pairs[action.cntry] = action.node_pairs
            return Object.assign({}, state, {
                node_pairs: node_pairs,
            });
        case ACTION_TYPE.RECEIVE_PICKED_PAIR:
            let picked_pairs = Object.assign({}, state.picked_pairs)

            picked_pairs[action.cntry] = action.picked_pairs
            return Object.assign({}, state, {
                picked_pairs: picked_pairs,
            });
        default:
            return state;
    }
}

const simulaReducer = (state = initialSimulaState, action) => {
    switch (action.type) {
        case ACTION_TYPE.RECEIVE_SIMULA:
            return Object.assign({}, state, {
                username: action.username,
                simulas: action.simulas,
            });
        default:
            return state;
    }
}

const assetReducer = (state = initialAssetState, action) => {
    switch (action.type) {
        case ACTION_TYPE.RECEIVE_ASSET:
            return Object.assign({}, state, {
                username: action.username,
                budget:   action.budget,
            });
        default:
            return state;
    }
}


const strainerReducer = (state = initialStrainerState, action) => {
    switch (action.type) {
        case ACTION_TYPE.RECEIVE_STRAINER:
            return Object.assign({}, state, {
                username:  action.username,
                strainers: action.strainers,
            });
        default:
            return state;
    }
}

const tradingReducer = (state = initialTradingState, action) => {
    switch (action.type) {
        case ACTION_TYPE.RECEIVE_TRADING:
            return Object.assign({}, state, {
                username: action.username,
                entries:  action.entries,
            });
        default:
            return state;
    }
}

const tickReducer = (state = initialTickState, action) => {
    switch (action.type) {
        case ACTION_TYPE.RECEIVE_TICK:
            return Object.assign({}, state, {
                ticks: Object.assign({}, state.ticks, action.tick),
            });
        default:
            return state;
    }
}

const baseReducer = (state = initialBaseState, action) => {
    switch (action.type) {
        case ACTION_TYPE.CHANGE_CNTRY:
            return Object.assign({}, state, {
                cntry: action.cntry,
            });
        default:
            return state;
    }
}

const strategyReducer = (state = initialStrategyState, action) => {
    switch (action.type) {
        case ACTION_TYPE.REQUEST_SIMULA:
            return Object.assign({}, state, {
                username: action.username,
                seconds:  0,
                progress: 0,
            });
        case ACTION_TYPE.REQUEST_TRADING:
            return Object.assign({}, state, initialStrategyState);
        case ACTION_TYPE.RECEIVE_PROGRESS:
            return Object.assign({}, state, {
                username: action.username,
                seconds:  action.seconds,
                progress: action.progress,
            });
        default:
            return state;
    }
}

const popupReducer = (state = initialPopupState, action) => {
    switch (action.type) {
        case ACTION_TYPE.POPUP_OPEN:
            return Object.assign({}, state, {
                open: true,
                title: action.title,
                content: action.content,
            });
        case ACTION_TYPE.POPUP_CLOSE:
            return Object.assign({}, state, {
                open: false,
            });
        default:
            return state;
    }
}

const calendarReducer = (state = initialCalendarState, action) => {
    switch (action.type) {
        case ACTION_TYPE.CHANGE_CALENDAR:
            return Object.assign({}, state, {
                date: action.date,
            });
        default:
            return state;
    }
}

const rootReducer = combineReducers({
    baseReducer,
    stockReducer,
    chartReducer,
    pairReducer,
    authReducer,
    assetReducer,
    simulaReducer,
    strainerReducer,
    tradingReducer,
    tickReducer,
    strategyReducer,
    popupReducer,
    calendarReducer,
});
export default rootReducer;
