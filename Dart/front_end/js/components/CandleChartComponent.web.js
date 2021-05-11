import React from 'react';
import { Platform, StyleSheet, View, Text } from 'react-native';
import { AppLoading } from 'expo';
import * as Font from 'expo-font';
//import Chart from "react-google-charts";

export default class CandleChartComponent extends React.Component {
    constructor(props) {
        super(props)

    }
    /*
    componentDidUpdate(prevProps) {
        const { ohlcvs } = this.props

        console.log('componentDidUpdate3')
        if (prevProps.ohlcvs === ohlcvs) {
            return
        }
        console.log('componentDidUpdate4')
        console.log('componentDidUpdate')
        //const data = [...simula.stats, simula.stats.discs]
        const data = [...simula.stats]
        const dataProvider = this.state.dataProvider.cloneWithRows(simula.stats)
        this.setState({ dataProvider })
    }
    */

    render() {
        const {code, ohlcvs } = this.props
        console.log('CandleChartComponent', ohlcvs['ohlcvs'])

        return (
            <Text> {ohlcvs} </Text>
        )
        return (
            <>
                { ohlcvs && ohlcvs['ohlcvs'] && ohlcvs['ohlcvs'].map((k, i) => {
                    console.log('dddddddddddddddd')
                    return (
                        <Text> {i} </Text>
                    )}
                )}
                }
            </>
    )
      return (
       <Chart
           width={400}
           height={300}
           chartType="ColumnChart"
           loader={<div>Loading Chart</div>}
           data={[
           ['City', '2010 Population', '2000 Population'],
           ['New York City, NY', 8175000, 8008000],
           ['Los Angeles, CA', 3792000, 3694000],
           ['Chicago, IL', 2695000, 2896000],
           ['Houston, TX', 2099000, 1953000],
           ['Philadelphia, PA', 1526000, 1517000],
           ]}

   options={{
         title: 'Population of Largest U.S. Cities',
         chartArea: { width: '30%' },
         hAxis: {
             title: 'Total Population',
             minValue: 0,
         },
         vAxis: {
         title: 'City',
         },
         }}
         />
         )
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
