import { combineReducers } from 'redux';
import * as ACTION_TYPE from '../constants/action-types';

/* kr:korea, us:united states */
const initialBaseState = {
    cntry: 'kr',
};

const initialAuthState = {
    username: '',
    token: '',
    level: 0,
    failed: false,
};

const initialCorpState = {
    corps: [],
};

const initialDiscState = {
    discs: [],
};

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

const discReducer = (state = initialDiscState, action) => {
    switch (action.type) {
        case ACTION_TYPE.REQUEST_DISC:
            return Object.assign({}, state, initialDiscState);
    case ACTION_TYPE.RECEIVE_DISC:
        return Object.assign({}, state, {
            discs: action.discs,
        });
    default:
        return state;
    }
}

const rootReducer = combineReducers({
    baseReducer,
    authReducer,
    corpReducer,
    discReducer,
});

export default rootReducer;

