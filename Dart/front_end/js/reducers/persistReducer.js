import * as ACTION_TYPE from '../constants/action-types';

const initialAuthState = {
    username: '',
    pushToken: '',
    level: 0,
    failed: false,
    authState: null,
};

const authReducer = (state = initialAuthState, action) => {
    switch (action.type) {
        case ACTION_TYPE.LOAD_PUSH_TOKEN:
            return Object.assign({}, state, {
                pushToken: action.pushToken,
            });

        case ACTION_TYPE.LOAD_AUTH:
            return Object.assign({}, state, {
            /*
                username: localStorage.getItem('yepark_username'),
                token: localStorage.getItem('yepark_token'),
                level: localStorage.getItem('yepark_level'),
                failed: false,
                */
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

export default authReducer;
