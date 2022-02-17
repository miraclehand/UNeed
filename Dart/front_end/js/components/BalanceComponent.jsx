import React from 'react';
import { StyleSheet, Text, View, FlatList, TouchableOpacity } from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import _ from "lodash"
import { Button } from 'react-native-elements'

const columns0 = 
[
    "추정순자산",
    "실현손익",
    "매입금액",
    "평가금액",
    "평가손익",
    "추정D2예수금",
]
const columns = 
[
    "종목코드",
    "종목명",
    "수량",
    "단가",
    "현재가",
    "평가금액",
    "손익금액",
    "수익률",
]

class BalanceComponent extends React.Component {
    constructor(props) {
        super(props);

        this.tableHeader0 = this.tableHeader0.bind(this)
        this.tableHeader = this.tableHeader.bind(this)
        this.sortTable= this.sortTable.bind(this)

        this.state = {
            selectedColumn: '',
            direction: '',
            accno:      props.accno,
            cur_asset:  props.cur_asset,
            profit:     props.profit,
            org_inv:    props.org_inv,
            est_amount: props.est_amount,
            est_profit: props.est_profit,
            deposit:    props.deposit,
            pos: [
            {
                code:    props.code,
                name:    props.name,
                qty :    props.qty,
                org_uv:  props.org_uv,
                org_amt: props.org_amt,
                curr:    props.curr,
                est_amt: props.est_amt,
                profit:  props.profit,
                prrt:    props.prrt,
            },
            ],
        };
    }

     sortTable(column) {
         const newDirection = this.state.direction === "desc" ? "asc" : "desc"
         const sortedData = _.orderBy(this.state.pets, [column],[newDirection])

         this.setState({selectedColumn:column})
         this.setState({direction:newDirection})
         this.setState({pets:sortedData})
       }

    tableHeader0() {
        return (
            <View style={styles.tableHeader}>
                {columns0.map((column, index) => {
                    return (
                        <TouchableOpacity 
                            key={index}
                            style={styles.columnHeader0} 
                        >
                            <Text style={styles.columnHeaderTxt}>{column + " "} 
                                { this.state.selectedColumn === column && <MaterialCommunityIcons
                     name={this.state.direction === "desc" ? "arrow-down-drop-circle" : "arrow-up-drop-circle"}
                            />
                                 }
                            </Text>
                        </TouchableOpacity>
                    )
                })
                }
            </View>
        )
    }
    tableHeader() {
        return (
            <View style={styles.tableHeader}>
                {columns.map((column, index) => {
                    return (
                        <TouchableOpacity 
                            key={index}
                            style={styles.columnHeader} 
                            onPress={()=> this.sortTable(column)}
                        >
                            <Text style={styles.columnHeaderTxt}>{column + " "} 
                                { this.state.selectedColumn === column && <MaterialCommunityIcons
                     name={this.state.direction === "desc" ? "arrow-down-drop-circle" : "arrow-up-drop-circle"}
                            />
                                 }
                            </Text>
                        </TouchableOpacity>
                    )
                })
                }
            </View>
        )
    }

    componentDidUpdate(prevProps) {
    }

    componentDidMount() {
    }

    render() {
        return (
            <>
            <View style={styles.container}>
                <FlatList 
                    data={this.props.est_acc}
                    style={{width:"90%"}}
                    keyExtractor={(item, index) => index+""}
                    ListHeaderComponent={this.tableHeader0}
                    stickyHeaderIndices={[0]}
                    renderItem={({item, index})=> {
                        return (
                          <View style={styles.tableRow}>
                          <Text style={styles.columnRowTxt0}>{item.cur_asset}</Text>
                          <Text style={styles.columnRowTxt0}>{item.profit}</Text>
                          <Text style={styles.columnRowTxt0}>{item.org_inv}</Text>
                          <Text style={styles.columnRowTxt0}>{item.est_amount}</Text>
                          <Text style={styles.columnRowTxt0}>{item.est_profit}</Text>
                          <Text style={styles.columnRowTxt0}>{item.deposit}</Text>
                          </View>
                        )
                    }}
                />
            </View>
            <View style={styles.container}>
                <FlatList 
                    data={this.props.position}
                    style={{width:"90%"}}
                    keyExtractor={(item, index) => index+""}
                    ListHeaderComponent={this.tableHeader}
                    stickyHeaderIndices={[0]}
                    renderItem={({item, index})=> {
                        return (
                          <View style={styles.tableRow}>
                          <Text style={styles.columnRowTxt}>{item.code}</Text>
                          <Text style={styles.columnRowTxt}>{item.name}</Text>
                          <Text style={styles.columnRowTxt}>{item.qty}</Text>
                          <Text style={styles.columnRowTxt}>{item.org_uv}</Text>
                          <Text style={styles.columnRowTxt}>{item.curr}</Text>
                          <Text style={styles.columnRowTxt}>{item.est_amt}</Text>
                          <Text style={styles.columnRowTxt}>{item.profit}</Text>
                          <Text style={styles.columnRowTxt}>{item.prrt}</Text>
                          </View>
                        )
                    }}
                />
            </View>
            <Text> last updated: {this.state.last_updated} </Text>
            <Button
                title = '잔고 조회'
                onPress={this.props.handlePress}
            />

            </>
        );
    }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop:80
  },
  tableHeader: {
    flexDirection: "row",
    justifyContent: "space-evenly",
    alignItems: "center",
    backgroundColor: "#37C2D0",
    borderTopEndRadius: 10,
    borderTopStartRadius: 10,
    height: 50
  },
  tableRow: {
    flexDirection: "row",
    height: 40,
    alignItems:"center",
  },
  columnHeader: {
    width: "12.5%",
    justifyContent: "center",
    alignItems:"center"
  },
  columnHeaderTxt: {
    color: "white",
    fontWeight: "bold",
  },
  columnRowTxt: {
    width:"12.5%",
    textAlign:"center",
  },
  columnHeader0: {
    width: "16.6%",
    justifyContent: "center",
    alignItems:"center"
  },
  columnRowTxt0: {
    width:"16.6%",
    textAlign:"center",
  },
});
export default BalanceComponent;

