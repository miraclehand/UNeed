import { createStore, applyMiddleware } from 'redux';
import logger from 'redux-logger';
import thunk from 'redux-thunk';
import rootReducer from '../reducers/rootReducer';

/*
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'

const persistConfig = {
    key: 'root',
    storage,
}

const enhancedReducer = persistReducer(persistConfig, rootReducer)
export const persistor = persistStore(store)
*/

const middlewares = [thunk];

export const store = createStore(
    rootReducer,
    applyMiddleware(...middlewares)
)
