import React from 'react';
import { RecyclerListView, DataProvider, LayoutProvider } from 'recyclerlistview';
import { Feather } from 'react-native-vector-icons';
import { SearchBar, Button } from 'react-native-elements'

import { TouchableOpacity, CheckBox, StyleSheet, Text, View, TextInput, Dimensions } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createMaterialTopTabNavigator } from '@react-navigation/material-top-tabs';
import { findText, getDisassembled } from '../util/textUtil';
import { Ionicons } from '@expo/vector-icons';
import { FontAwesome } from '@expo/vector-icons';


const Tab = createMaterialTopTabNavigator();

const SCREEN_WIDTH = Dimensions.get("window").width;


const orders_columns =
[
    "주문번호",
    "종목명",
    "매매구분",
    "주문수량",
    "주문금액",
    "체결수량",
    "체결금액",
]

class OrderComponent extends React.Component {
    constructor(props) {
        super(props);

        this._rowRenderer = this._rowRenderer.bind(this);
        this._layoutProvider = new LayoutProvider(
            index => {
                return 0;
            },
            (type, dim) => {
                dim.width = SCREEN_WIDTH;
                dim.height = 35;
            }
        );

        const dataProvider = new DataProvider((r1, r2) => { return r1 !== r2; })

        this.state = {
            index:0,
            placeholder: 'Search Stocks...',
            showStocks: false,
            sel_stock: '',
            value: '',
            qty:'',
            price:'',
            dataProvider: dataProvider.cloneWithRows(this.props.stocks),
            extendedState: {
                selected: [],
            },
        };
        this.searchStock = this.searchStock.bind(this)
        this.onFocus = this.onFocus.bind(this)
        this.handleOrderStock = this.handleOrderStock.bind(this)
    }
    componentDidUpdate(prevProps) {
        const { stocks } = this.props

        if (prevProps.stocks === stocks) {
            return
        }
        const dataProvider = this.state.dataProvider.cloneWithRows(stocks)

        this.setState({ dataProvider })
    }

    onFocus() {
        this.setState({showStocks:true})
    }

    handleSelectStock(newStock) {
        console.log(newStock)
        this.props.requestCompany('email', 'token', 'kr', newStock.code)
        this.setState({showStocks:false, sel_stock:newStock, value:newStock.name})
        return
        let unitStocks = this.props.unitStocks;

        const stocks = this.props.stocks.filter( stock =>
            findText(stock.dname, this.state.value) > -1
        );
        const dataProvider = this.state.dataProvider.cloneWithRows(stocks)

        /* 전체를 선택한 적이 있다면, */
        if (unitStocks.filter(stock => stock.code === '000000').length > 0) {

            unitStocks = []
        }
        unitStocks = [newStock]
        /*
        if (newStock.code === '000000') {
            unitStocks = [newStock]
        } else {
            if (unitStocks.indexOf(newStock) === -1) {
                unitStocks = this.addUnitStock(unitStocks, newStock)
            } else {
                unitStocks = this.delUnitStock(unitStocks, newStock)
            }
        }
        */

        const extendedState = {
            selected: unitStocks
        }

        this.setState({ dataProvider, extendedState })
        this.props.handleUnitStocks(unitStocks)
    }
    _rowRenderer(type, stock, index, extendedState) {
        const icon = extendedState.selected.filter( s =>
            s.code === stock.code
        )[0] === stock ? 'check-square' : 'square'

        return (
            <View style ={{ alignItems: 'flex-start' }} >
                <Button
                    titleStyle={{marginLeft:5}}
                    type = "clear"
                    title = {stock.name}
                    onPress={() => this.handleSelectStock(stock)}
                    iconContainerStyle={{ marginLeft:50}}
                    icon = { <Feather size={15} name={icon} /> }
                />
            </View>
        )
    }

    handleOrderStock(e) {
        console.log('handleOrderStock', this.state.sel_stock)
        const {code} = this.state.sel_stock
        const {qty, price, ordno } = this.state

        if (this.props.order === '매수') {
            this.props.requestPostBuy(code, qty, price)
        }
        else if (this.props.order === '매도') {
            this.props.requestPostSell(code, qty, price)
        }
        else if (this.props.order === '정정') {
            this.props.requestPostModify(code, qty, price, ordno)
        }
        else if (this.props.order === '취소') {
            this.props.requestPostCancel(code, qty, ordno)
        }
    }

    searchStock(value) {
        const stocks = this.props.stocks.filter(stock =>
            findText(stock.dname, value) > -1
        );
        const dataProvider = this.state.dataProvider.cloneWithRows(stocks)

        if (stocks.length > 0) {
            this.setState({ value, dataProvider })
        } else {
            this.setState({ value })
        }
    }
    render() {
        return (
            <>
            <SearchBar
                placeholder={this.state.placeholder}
                onChangeText={this.searchStock}
                value={this.state.value}
                platform='ios'
                onFocus={this.onFocus}
            />
            <TextInput
                style={styles.textInputStyle}
                placeholder="Enter Qty"
                placeholderTextColor="#60605e"
                numeric
                keyboardType={'numeric'}
                value={this.state.qty}
                onChangeText={value => this.setState({qty:value})}
            />
            <TextInput
                style={styles.textInputStyle}
                placeholder="Enter Price"
                placeholderTextColor="#60605e"
                numeric
                keyboardType={'numeric'}
                value={this.state.price}
                onChangeText={value => this.setState({price:value})}
            />
            <Button
                titleStyle={{marginLeft:5}}
                type = "clear"
                title = '현재가불러오기'
                onPress={() => this.props.handleSelectStock(stock)}
                iconContainerStyle={{ marginLeft:50}}
            />
            <Button
                titleStyle={{marginLeft:5}}
                type = "clear"
                title = {this.props.order}
                onPress={this.handleOrderStock}
                iconContainerStyle={{ marginLeft:50}}
            />
            {this.state.dataProvider._size > 0 && this.state.showStocks === true &&
            <RecyclerListView
                layoutProvider={this._layoutProvider}
                dataProvider={this.state.dataProvider}
                rowRenderer={this._rowRenderer}
                extendedState={this.state.extendedState}
                style={{ flex:1 }}
            />
            }
            </>
        )
    }
}

/*
            <View style={{width: '55%', height: '100%', backgroundColor: 'powderblue'}}>
            <View style={{width: '45%', height: '100%', backgroundColor: 'steelblue'}}>
*/
class BuyComponent extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems:'center', flexDirection: 'row' }}>
                <View style={{width: '55%', height: '100%' }}>
                </View>
                <View style={{width: '45%', height: '100%'}}>
                    <OrderComponent {...this.props} order='매수'/>
                </View>
            </View>
        )
    }
}

class SellComponent extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems:'center', flexDirection: 'row' }}>
                <View style={{width: '55%', height: '100%' }}>
                </View>
                <View style={{width: '45%', height: '100%'}}>
                    <OrderComponent {...this.props} order='매도'/>
                </View>
            </View>
        )
    }
}

class ModifyComponent extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems:'center', flexDirection: 'row' }}>
                <View style={{width: '55%', height: '100%' }}>
                </View>
                <View style={{width: '45%', height: '100%'}}>
                    <OrderComponent {...this.props} order='정정'/>
                </View>
            </View>
        )
    }
}

class LeftComponent extends React.Component {
    constructor(props) {
        super(props);

        this._rowRenderer = this._rowRenderer.bind(this);
        this._layoutProvider = new LayoutProvider(
            index => {
                return 0;
            },
            (type, dim) => {
                dim.width = SCREEN_WIDTH / 2;
                dim.height = 35;
            }
        );

        const dataProvider = new DataProvider((r1, r2) => { return r1 !== r2; })

        this.state = {
            sel_stock: '',
            value: '',
            qty:'',
            price:'',
            order:{},
            dataProvider: dataProvider.cloneWithRows(this.props.rows),
            extendedState: {
                selected: [],
            },
        };
    }
    componentDidUpdate(prevProps) {
        const { rows } = this.props

        if (prevProps.rows === rows) {
            return
        }
        const dataProvider = this.state.dataProvider.cloneWithRows(rows)

        this.setState({ dataProvider })
    }

    handlePress(order) {
        this.setState({order:order})
    }

    _rowRenderer(type, row, index, extendedState) {
        const icon = 'square'

        return (
            <TouchableOpacity
                key={index}
                style={styles.tableRow}
                onPress={() => this.handlePress(row) }
            >
                <Text style={styles.columnRowTxt0}>{row.ordno}</Text>
                <Text style={styles.columnRowTxt0}>{row.expname}</Text>
                <Text style={styles.columnRowTxt0}>{row.medosu}</Text>
                <Text style={styles.columnRowTxt0}>{row.qty}</Text>
                <Text style={styles.columnRowTxt0}>{row.price}</Text>
                <Text style={styles.columnRowTxt0}>{row.cheqty}</Text>
                <Text style={styles.columnRowTxt0}>{row.cheprice}</Text>
            </TouchableOpacity>
        )
    }

    render() {
        const { email, token, columns } = this.props
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems:'center' }}>
                <View style={{width: '100%', height: '70%' }}>
                    <View style={styles.tableHeader}>
                    {columns.map((column, index) => {
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
                    {this.state.dataProvider._size > 0 &&
                    <RecyclerListView
                        layoutProvider={this._layoutProvider}
                        dataProvider={this.state.dataProvider}
                        rowRenderer={this._rowRenderer}
                        extendedState={this.state.extendedState}
                        style={{ flex:1 }}
                    />
                    }
                </View>
                <View style={{width: '100%', height: '30%' }}>
                <Button
                    titleStyle={{marginLeft:5}}
                    type = "clear"
                    title = '조회'
                    onPress={() => this.props.requestOrders(email,token,'2')}
                    iconContainerStyle={{ marginLeft:50}}
                />
                </View>
            </View>
        )
    }
}

class CancelComponent extends React.Component {
    constructor(props) {
        super(props);

        this.handlePress = this.handlePress.bind(this)

        this.state = {
            sel_stock: '',
            value: '',
            qty:'',
            price:'',
            order:{},
        };
    }

    handlePress(order) {
        this.setState({order:order})
    }

    render() {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems:'center', flexDirection: 'row' }}>
                <View style={{width: '55%', height: '100%' }}>
                    <LeftComponent {...this.props} columns = {orders_columns} rows = {this.props.orders} />
                </View>
                <View style={{width: '45%', height: '100%'}}>
                    <OrderComponent {...this.props} {...this.state} columns = {orders_columns} rows = {this.props.orders} order='취소'/>
                </View>
            </View>
        )
    }
}

class TraderComponent extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Tab.Navigator>
                <Tab.Screen name="매도">
                    {(props) => <SellComponent {...props} {...this.props} />}
                </Tab.Screen>
                <Tab.Screen name="매수">
                    {(props) => <BuyComponent {...props} {...this.props} />}
                </Tab.Screen>
                <Tab.Screen name="정정">
                    {(props) => <ModifyComponent {...props} {...this.props} />}
                </Tab.Screen>
                <Tab.Screen name="취소">
                    {(props) => <CancelComponent {...props} {...this.props} />}
                </Tab.Screen>
            </Tab.Navigator>
        )
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
    width: "14.2%",
    justifyContent: "center",
    alignItems:"center"
  },
  columnRowTxt0: {
    width:"14.2%",
    textAlign:"center",
  },
  textInputStyle: {
    width: 250,
    backgroundColor: '#dde8c9',
    padding: 16,
  },
  container2: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
export default TraderComponent;

