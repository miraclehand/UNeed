import React from 'react';
import { Image, Button, View, Text, TextInput, Dimensions, TouchableOpacity, StyleSheet, FlatList } from 'react-native'
import Constants from 'expo-constants';
import { RecyclerListView, DataProvider, LayoutProvider } from "recyclerlistview";
import * as WebBrowser from 'expo-web-browser';

import { getDisassembled } from '../util/textUtil';
import CandleChartComponent from './CandleChartComponent';

const ViewTypes = {
    TABLE_HEADER: 0,
    TABLE_BODY: 1,
    DISC_CONTENT: 2,
};

const SCREEN_WIDTH = Dimensions.get("window").width;

class StatsSimulaComponent extends React.Component {
    constructor(props) {
        super(props);

        this.handleStockLink = this.handleStockLink.bind(this)
        this.handleCandleChart = this.handleCandleChart.bind(this)
        this.handleDiscLink = this.handleDiscLink.bind(this)
        this.handlePress = this.handlePress.bind(this)

        this._rowRenderer = this._rowRenderer.bind(this);

        this._layoutProvider = new LayoutProvider(
            index => {
                if (index == 0) {
                    return ViewTypes.TABLE_HEADER;
                } else {
                    return ViewTypes.TABLE_BODY;
                }
            },
            (type, dim) => {
                dim.width = SCREEN_WIDTH;
                dim.height = 100;
            }
        );

        const dataProvider = new DataProvider((r1, r2) => { return r1 !== r2; })

        /*
        const data = [...this.props.simula.stats, ...this.props.simula.stats]
        const data = [...this.props.simula.stats]
        */
        console.log('Stat', this.props.simula)
        this.state = {
            dataProvider: dataProvider.cloneWithRows(this.props.simula.stats),
        };
    }

    handlePress(stock_code) {
        this.props.handlePress(stock_code)
    }

    handleStockLink(stock_code) {
        const url = 'http://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A' + stock_code + '&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=&strResearchYN='

        WebBrowser.openBrowserAsync(url)
    }

    handleCandleChart(stock_code) {
    }

    handleDiscLink(url) {
        WebBrowser.openBrowserAsync(url)
    }

    componentDidUpdate(prevProps) {
        const { simula } = this.props

        if (prevProps.simula === simula) {
            return
        }
        /*
        console.log('componentDidUpdate')
        //const data = [...simula.stats, simula.stats.discs]
        const data = [...simula.stats]
        const dataProvider = this.state.dataProvider.cloneWithRows(simula.stats)
        this.setState({ dataProvider })
        */
    }

    _rowRenderer(type, stats, index, extendedState) {
        switch (type) {
            case ViewTypes.TABLE_HEADER:
                return (
                    <View style={styles.stats}>
                    <View style={styles.flexRow}>
                        <Text style={styles.textBox}> 종목 </Text>
                        <Text style={styles.textBox}> 공시일자 </Text>
                        <Text style={styles.textBox}> 한달전 </Text>
                        <Text style={styles.textBox}> 한주전 </Text>
                        <Text style={styles.textBox}> 공시일 </Text>
                        <Text style={styles.textBox}> 한주후 </Text>
                        <Text style={styles.textBox}> 한달후 </Text>
                        <Text style={styles.textBox}> 등락   </Text>
                    </View>
                    </View>
                )
            case ViewTypes.TABLE_BODY:
                const { cell_red, cell_blue } = styles;
                const prrt = (stats.closeAf30 - stats.close)/stats.close * 100
                const cell_color = isNaN(prrt) ? '' : prrt > 0 ? cell_red : cell_blue
                return (
                    <View style={styles.stats}>
                    <View style={styles.flexRow}>
                        <TouchableOpacity onPress={() => this.handleStockLink(stats.disc.stock_code)}>

                            <Text style={styles.textBox}> {stats.corp.corp_name} </Text>
                        </TouchableOpacity>
                        <Text style={styles.textBox}> {stats.disc.rcept_dt} </Text>
                        <Text style={styles.textBox}> {stats.closeBf30.toLocaleString()} </Text>
                        <Text style={styles.textBox}> {stats.closeBf7.toLocaleString()} </Text>
                        <Text style={styles.textBox}> {stats.close.toLocaleString()} </Text>
                        <Text style={styles.textBox}> {stats.closeAf7.toLocaleString()} </Text>
                        <Text style={styles.textBox}> {stats.closeAf30.toLocaleString()} </Text>
                        <TouchableOpacity onPress={() => this.handlePress(stats.disc.stock_code)}>
                            <Text style={cell_color}> {prrt.toLocaleString()} </Text>
                        </TouchableOpacity>
                    </View>
                    </View>
                )
            case ViewTypes.DISC_CONTENTS:
                return <></>
            default:
                return null;
        }
    }

    render() {
        if (!this.props.simula) {
            return <></>
        }

        const { name, s_date, e_date, std_disc, stats } = this.props.simula
        return (
            <>
                <Text style={styles.title}> { name } </Text>
                <Text> {std_disc.report_nm} </Text>
                <View style={styles.period}>
                    <Text> { s_date } </Text>
                    <Text> { e_date } </Text>
                </View>
                {this.state.dataProvider._size > 0 &&
                <View  style = {styles.MainContainer}>
                    <RecyclerListView
                        layoutProvider={this._layoutProvider}
                        dataProvider={this.state.dataProvider}
                        rowRenderer={this._rowRenderer}
                        forceNonDeterministicRendering={true}
                        style={{ flex:1 }}
                    />
                </View>
                }
            </>
        )
        /*
                <FlatList
                    data= {this.state.dataSource}
                    renderItem={({ item }) => (
                        <View style={{ flex: 1, flexDirection: 'column', margin: 1 }}>
                            <Image style={styles.imageThumbnail} source={{ uri: item.src }} />
                        </View>
                    )}
                    numColumns={8}
                    keyExtractor={(item, index) => index}
                />
                */
    }
}

const styles = StyleSheet.create({
  aaa: {
    flex: 1,
  },
  MainContainer: {
    justifyContent: 'center',
    flex: 1,
    paddingTop: 10,
  },

  imageThumbnail: {
    justifyContent: 'center',
    alignItems: 'center',
    height: 100,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  period: {
    flexDirection: 'row',
    alignItems:'flex-start',
  },
  flexRow: {
    flex:1,
    flexDirection: 'row',
    alignItems:'flex-start',
    borderColor: '#ccc',
    borderBottomWidth: 1,
      alignItems: 'center',
          justifyContent: 'center',
  },
  textBox: {
    flex: 1,
    fontSize:16,
    textAlign: 'right', 
    marginRight: 10, 
    width: 160,
  },
  textBox2: {
     flex: 1,
     fontSize: 20,
     fontStyle: 'italic',
     fontWeight: 'bold',
     textAlign: "left",
     textAlignVertical: "center",
     borderColor: '#ccc',
     borderWidth: 1,
    height:100,
  },
  cell_red: {
    color: 'rgb(255,250,250)',
    backgroundColor: 'rgba(220, 20, 60, 1)',
    textAlign: 'right', 
    flex: 1,
    fontSize:16,
    marginRight: 10, 
    width: 160,
  },
  cell_blue: {
    color: 'rgb(255,250,250)',
    backgroundColor: 'rgba(0, 0, 255, 1)',
    textAlign: 'right',
    flex: 1,
    fontSize:16,
    marginRight: 10, 
    width: 160,
  },
  container: { flex: 1, padding: 16, paddingTop: 30, backgroundColor: '#fff' },
  head: { height: 40, backgroundColor: '#f1f8ff' },
  text: { margin: 6 },
  stats: {
    justifyContent: "space-around",
    alignItems: 'flex-start',
    flex: 1,
    backgroundColor: 'transparent',
    marginTop: 0,
    marginBottom: 0,
    marginLeft: 10,
    marginRight: 10,
    minWidth: SCREEN_WIDTH - (50),
    maxWidth: SCREEN_WIDTH - (50),
  }
});


export default StatsSimulaComponent;
