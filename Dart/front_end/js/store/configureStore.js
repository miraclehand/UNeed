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

/*
module.exports = function(app) {
    app.use(
        createProxyMiddleware('/naver', {
        target: 'https://openapi.naver.com',
        changeOrigin: true,
    })
    )
}
*/

const middlewares = [thunk];

export const store = createStore(
    rootReducer,
    applyMiddleware(...middlewares)
)

