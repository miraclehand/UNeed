import React, { useEffect, useState } from 'react';
import { Provider} from 'react-redux';
import { store } from './js/store/configureStore'
import Home from './js/Home';
import AppLoadScreen from './js/screens/AppLoadScreen';

/* https://dart.uneed.com */
export default function App() {
    const [isReady, setReady] = useState(false);

    return (
        <Provider store={store}>
            {!isReady ? <AppLoadScreen setReady={setReady} /> : <Home />}
        </Provider>
    )
}
