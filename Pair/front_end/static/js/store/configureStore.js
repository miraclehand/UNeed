import { createStore, applyMiddleware } from 'redux';
import logger from 'redux-logger';
import thunk from 'redux-thunk';
import rootReducer from '../reducers/rootReducer';

/*
const middlewares = [logger,thunk];
*/
/* it doen't always work */
/*
const auth_header = {
    metohd: 'GET',
    headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        'username': localStorage.getItem('username'),
        'x-access-token': localStorage.getItem('token'),
    }
}
const middlewares = [thunk.withExtraArgument(auth_header)]
*/
const middlewares = [thunk];

const store = createStore(
    rootReducer,
    applyMiddleware(...middlewares)
)
export default store
