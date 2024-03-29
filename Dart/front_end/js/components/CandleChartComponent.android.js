import React from 'react';
import { Platform, StyleSheet, View, Text } from 'react-native';
import { AppLoading } from 'expo';
import * as Font from 'expo-font';

import { VictoryBar, VictoryChart, VictoryTheme } from 'victory-native';

const data = [
  { quarter: 1, earnings: 53000 },
  { quarter: 2, earnings: 16500 },
  { quarter: 3, earnings: 14250 },
  { quarter: 4, earnings:  3000 },
];

export default class CandleChartComponent extends React.Component {
  state = { isReady: false };

  _loadFontAsync = () => {
    return Font.loadAsync({ Roboto: require('./Roboto.ttf') });
  };

  render() {
    if (!this.state.isReady) {
      return (
        <AppLoading
          startAsync={this._loadFontAsync}
          onFinish={() => this.setState({ isReady: true })}
          onError={e => console.log(e)}
        />
      );
    }

    return (
      <View style={styles.container}>
        <Text> android =>  {this.props.ohlcvs} </Text>
        <VictoryChart
          width={350}
          /**
           * the material theme uses the Roboto font, and react-native-svg isn't
           * compatible with expo-font, so we can't use this theme:
           * theme={VictoryTheme.material}
           **/
        >
          <VictoryBar data={data} x="quarter" y="earnings" />
        </VictoryChart>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5fcff',
  },
});

