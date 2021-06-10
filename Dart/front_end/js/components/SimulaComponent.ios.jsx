import React from 'react';
import { Platform, View, StyleSheet, Text, TextInput, SafeAreaView } from 'react-native'
import { Button } from 'react-native-elements'
import Constants from 'expo-constants';


/*
    import { VictoryBar, VictoryChart, VictoryTheme } from 'victory-native';
import { LineChart, Path, Grid } from 'react-native-svg-charts'
*/

/*
import Chart from 'react-apexcharts';
if (Platform.OS == 'web') {
}
console.log(11112, Platform.OS)
*/

/*
import { LineChart, Path, Grid } from 'react-native-svg-charts'
*/

/* mobile */
/*
import { BarChart, XAxis } from 'react-native-svg-charts'
*/

/* web */
/*
import Chart from 'react-apexcharts';
*/

/*
import {VictoryCandlestick } from 'victory-native';
import Chart from "react-google-charts";
mobile
import {VictoryCandlestick } from 'victory-native';
mobile
react-native-charts-wrapper
web
import Chart from 'react-apexcharts';
import { BarChart, XAxis } from 'react-native-svg-charts'
*/

class SimulaComponent extends React.Component {
    constructor(props) {
        super(props);
        this.handlePress = this.handlePress.bind(this)
    }

    handlePress() {
        this.props.handlePress(this.state.text)
    }

    render() {
        return (
        <>
            <Text>iosiosios</Text>
            <Button
                title = '데이터 삭제'
                onPress={this.handlePress}
            />
        </>
        )
  const data = [ 50, 10, 40, 95, -4, -24, 85, 91, 35, 53, -53, 24, 50, -20, -80 ]

        const Shadow = ({ line }) => (
            <Path
                key={'shadow'}
                y={2}
                d={line}
                fill={'none'}
                strokeWidth={4}
                stroke={'rgba(134, 65, 244, 0.2)'}
            />
        )

        return (
            <LineChart
                style={ { height: 200 } }
                data={ data }
                svg={{ stroke: 'rgb(134, 65, 244)' }}
                contentInset={ { top: 20, bottom: 20 } }
            >
                <Grid/>
                <Shadow/>
            </LineChart>
        )
/*
const data = [
  { quarter: 1, earnings: 13000 },
  { quarter: 2, earnings: 16500 },
  { quarter: 3, earnings: 14250 },
  { quarter: 4, earnings: 19000 }
];
 return (
      <View style={styles.container}>
        <VictoryChart width={350} theme={VictoryTheme.material}>
          <VictoryBar data={data} x="quarter" y="earnings" />
        </VictoryChart>
      </View>
    );
*/
        return <></>
        return <></>
    }

    /*
        const { options, ohlcvs } = this.props
        ohlcvs.splice(ohlcvs, 0, ['date', 'low', 'open', 'close', 'high'])

        return (
            <View>
                <Chart
                    options={options}
                    series={ohlcvs}
                    type="candlestick"
                />
            </View>
        )
        */
    /*
        return (
            <View>
            </View>
        )
        */
        /*
const candleData = [
  { x: 1, open: 9, close: 30, high: 56, low: 7 },
    { x: 2, open: 80, close: 40, high: 120, low: 10 },
      { x: 3, open: 50, close: 80, high: 90, low: 20 },
        { x: 4, open: 70, close: 22, high: 70, low: 5 },
          { x: 5, open: 20, close: 35, high: 50, low: 10 },
            { x: 6, open: 35, close: 30, high: 40, low: 3 },
              { x: 7, open: 30, close: 90, high: 95, low: 30 },
                { x: 8, open: 80, close: 81, high: 83, low: 75 }
                ];
    return (
   <VictoryChart>
           <VictoryCandlestick data={candleData} />
                 </VictoryChart>
    )

*/
/*
        */
    /*    
    return <></>
console.log(ohlcvs)
console.log(ohlcvs[0])
const data=[
            ['day', 'a', 'b', 'c', 'd'],
            ['Mon', 20, 28, 38, 45],
            ['Tue', 31, 38, 55, 66],
            ['Wed', 50, 55, 77, 80],
            ['Thu', 77, 77, 66, 50],
            ['Fri', 68, 66, 22, 15],
          ]
console.log(data)

const data1=[
            ['day', 'low', 'open', 'close', 'high'],
            ['2019-01-03', 10, 20, 30, 40],
            ['2019-01-04', 10, 30, 20, 40],
            ['2019-01-07', 40, 20, 30, 10],
            ['2019-01-08', 10, 20, 30, 40],
            ['2019-01-09', 10, 20, 30, 40],
          ]
*/
/*
    return (
        <Chart
          width={'100%'}
          height={350}
          chartType="CandlestickChart"
          loader={<div>Loading Chart</div>}
          data={ohlcvs}
          options={{
             legend: 'none',
                bar: { groupWidth: '100%' }, // Remove space between bars.
                candlestick: {
                  risingColor:  { strokeWidth: 0, fill: '#FF0000' }, // red
                  fallingColor: { strokeWidth: 0, fill: '#0000FF' }, // blue
                },
          }}
          rootProps={{ 'data-testid': '1' }}
        />
    )
    */
    /*
    return (
        <Chart
          width={'100%'}
          height={350}
          chartType="CandlestickChart"
          loader={<div>Loading Chart</div>}
          data={[
            ['day', 'a', 'b', 'c', 'd'],
            ['Mon', 20, 28, 38, 45],
            ['Tue', 31, 38, 55, 66],
            ['Wed', 50, 55, 77, 80],
            ['Thu', 77, 77, 66, 50],
            ['Fri', 68, 66, 22, 15],
          ]}
          options={{
            legend: 'none',
          }}
          rootProps={{ 'data-testid': '1' }}
        />
    )
*/


/*
        return (
            <View>
                <Text> dd </Text>
                <Chart
                    options={options}
                    series={ohlcvs}
                    type="candlestick"
                />
            </View>
        )
        */
}

const styles = StyleSheet.create({
  container: {
      flex: 1,
          justifyContent: "center",
              alignItems: "center",
                  backgroundColor: "#f5fcff"
                    }
});
export default SimulaComponent;
