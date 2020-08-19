import React from 'react';
import { Provider} from 'react-redux';
import { StyleSheet, Text, View } from 'react-native';
//import { store, persistor} from './js/store/configureStore'
import { store } from './js/store/configureStore'
import Home from './js/Home';

/* https://dart.uneed.com */
export default function App() {
  return (
        <Provider store={store}>
            <Home />
        </Provider>
  );
  return (
        <Provider store={store} persistor={persistor}>
            <Home />
        </Provider>
  );
  return (
    <View style={styles.container}>
        <Provider store={store}>
            <Home />
        </Provider>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
