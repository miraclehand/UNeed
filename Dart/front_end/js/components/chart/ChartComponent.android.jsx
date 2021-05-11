import React from 'react';
import { Platform, StyleSheet, View } from 'react-native';
import { AppLoading } from 'expo';
import * as Font from 'expo-font';

import { VictoryBar, VictoryCandlestick, VictoryChart, VictoryTheme } from 'victory-native';


const getData = () => {
  const colors = [
    "violet",
    "cornflowerblue",
    "gold",
    "orange",
    "turquoise",
    "tomato",
    "greenyellow"
  ];
  return range(50).map(() => {
    return {
      x: random(600),
      open: random(600),
      close: random(600),
      high: random(450, 600),
      low: random(0, 150),
      size: random(15) + 3,
      fill: colors[random(0, 6)],
      opacity: random(0.3, 1)
    };
  });
};

const style = {
  parent: {
    border: "1px solid #ccc",
    margin: "2%",
    maxWidth: "40%"
  }
};

const data = [
  { x: new Date(2016, 6, 1), open: 9, close: 30, high: 56, low: 7 },
  { x: new Date(2016, 6, 2), open: 80, close: 40, high: 120, low: 10 },
  { x: new Date(2016, 6, 3), open: 50, close: 80, high: 90, low: 20 },
  { x: new Date(2016, 6, 4), open: 70, close: 22, high: 70, low: 5 }
];


class ChartComponent extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            data: data,
        }

        this._loadFontAsync = this._loadFontAsync.bind(this)
    }

    _loadFontAsync = () => {
        return Font.loadAsync({ Roboto: require('./Roboto.ttf') });
    };

    render() {
 const containerStyle = {
      display: "flex",
      flexDirection: "row",
      flexWrap: "wrap",
      alignItems: "center",
      justifyContent: "center"
    };

      if (!this.state.isReady) {
          return (
            <AppLoading
              startAsync={this._loadFontAsync}
              onFinish={() => this.setState({ isReady: true })}
              onError={e => console.log(e)}
            />
          );
        }
        const DATA = [
          { x: 0, y: 100 },
          { x: 1, y: 103 },
          { x: 2, y: 121 },
          { x: 3, y: 110 },
          { x: 4, y: 108 },
          { x: 5, y: 110 },
          { x: 6, y: 105 },
          { x: 7, y: 105 },
          { x: 8, y: 107 },
          { x: 9, y: 105 },
          { x: 10, y: 103 },
          { x: 11, y: 102 },
          { x: 12, y: 104 },
          { x: 13, y: 121 },
          { x: 14, y: 117 },
          { x: 15, y: 105 },
          { x: 16, y: 105 },
          { x: 17, y: 105 },
          { x: 18, y: 105 },
          { x: 19, y: 105 },
          { x: 20, y: 105 }
        ];
     return (
        <VictoryChart padding={0} height={200} width={360 - 30}>
            <VictoryCandlestick
                data={this.props.ohlcvs}
                open={d => d[1]}
                close={d => d[2]}
                high={d => d[3]}
                low={d => d[3]}
                candleColors={{ positive: "#5f5c5b", negative: "#c43a31" }}
            />
        </VictoryChart>
     )
     return (
      <View style={styles.container}>
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

export default ChartComponent;
