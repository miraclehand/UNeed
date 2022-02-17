import React from 'react';
import { RecyclerListView, DataProvider, LayoutProvider } from 'recyclerlistview';
import { Feather } from 'react-native-vector-icons';
import { SearchBar, Button } from 'react-native-elements'

import { TouchableOpacity, CheckBox, StyleSheet, Text, View, TextInput, Dimensions } from 'react-native';
import { findText, getDisassembled } from '../../util/textUtil';
import { Ionicons } from '@expo/vector-icons';
import { FontAwesome } from '@expo/vector-icons';

const SCREEN_WIDTH = Dimensions.get("window").width;

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
            placeholder: 'Search Stocks...',
            showStocks: false,
            code: '',
            name: '',
            value: '',
            qty:'',
            price:'',
            ordno:0,
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
        const { code, name, stocks, stock, qty, price, ordno  } = this.props

        if (prevProps.stocks !== stocks) {
            const dataProvider = this.state.dataProvider.cloneWithRows(stocks)
            this.setState({ dataProvider })
        }
        if (prevProps.code !== code) {
            this.setState({ code })
        }
        if (prevProps.name !== name) {
            this.setState({ name })
        }
        if (prevProps.qty !== qty) {
            this.setState({ qty })
        }
        if (prevProps.price !== price) {
            this.setState({ price })
        }
        if (prevProps.ordno !== ordno) {
            this.setState({ ordno })
        }
    }

    onFocus() {
        this.setState({showStocks:true})
    }

    handleSelectStock(newStock) {
        this.props.requestCompany(newStock.code)
        this.setState({showStocks:false, value:newStock.name, code:newStock.code, name:newStock.name})
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
                    title = {stock.label}
                    onPress={() => this.handleSelectStock(stock)}
                    iconContainerStyle={{ marginLeft:50}}
                    icon = { <Feather size={15} name={icon} /> }
                />
            </View>
        )
    }

    handleOrderStock(e) {
        const {code, qty, price, ordno } = this.state
        this.props.handleOrder(code, qty, price, ordno)
    }

    searchStock(code) {
        const stocks = this.props.stocks.filter(stock =>
            findText(stock.dname, code) > -1
        );
        const dataProvider = this.state.dataProvider.cloneWithRows(stocks)

        if (stocks.length > 0) {
            this.setState({ code, dataProvider })
        } else {
            this.setState({ code })
        }
    }

    render() {
        return (
            <View style = {{flex:1}}>
                <View style= {styles.container_row} >
                    <Text style= {styles.label} > 종목 </Text>
                    <SearchBar
                        placeholder={this.state.placeholder}
                        onChangeText={this.searchStock}
                        value={this.state.code}
                        platform='ios'
                        onFocus={this.onFocus}
                    />
                    <Text style={styles.label}> {this.state.name} </Text>
                </View>
                {this.state.dataProvider._size > 0 && this.state.showStocks === true &&
                    <RecyclerListView
                        layoutProvider={this._layoutProvider}
                        dataProvider={this.state.dataProvider}
                        rowRenderer={this._rowRenderer}
                        extendedState={this.state.extendedState}
                        style={{ flex:1 }}
                    />
                }
                <View style= {styles.container_row} >
                    <Text style={styles.label} > 수량 </Text>
                    <TextInput
                        style={styles.inputext}
                        placeholder="Enter Qty"
                        placeholderTextColor="#60605e"
                        numeric
                        keyboardType={'numeric'}
                        value={this.state.qty}
                        onChangeText={value => this.setState({qty:value})}
                    />
                </View>
                <View style= {styles.container_row} >
                    <Text style={styles.label} > 가격 </Text>
                    <TextInput
                        style={styles.inputext}
                        placeholder="Enter Price"
                        placeholderTextColor="#60605e"
                        numeric
                        keyboardType={'numeric'}
                        value={this.state.price}
                        onChangeText={value => this.setState({price:value})}
                    />
                </View>
                {this.state.ordno > 0 &&
                <View style= {{flexDirection:'row' }} >
                    <Text style={styles.label} > 주문번호 </Text>
                    <TextInput
                        style={styles.inputext}
                        placeholder="Enter ordno"
                        placeholderTextColor="#60605e"
                        numeric
                        keyboardType={'numeric'}
                        value={this.state.ordno}
                        onChangeText={value => this.setState({ordno:value})}
                    />
                </View>
                }
                <Button
                    titleStyle={{marginLeft:5}}
                    type = "clear"
                    title = '현재가불러오기'
                    onPress={() => this.props.requestCompany(this.state.code)}
                    iconContainerStyle={{ marginLeft:50}}
                />
                <Button
                    titleStyle={{marginLeft:5}}
                    type = "clear"
                    title = {this.props.order}
                    onPress={this.handleOrderStock}
                    iconContainerStyle={{ marginLeft:50}}
                />
            </View>
        )
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#00fffff',
        alignItems: 'center',
        justifyContent: 'center',
        paddingTop:80
    },
    container_row: {
        flexDirection:'row'
    },
    label: {
        width: 100,
        height: 44,
        padding: 10,
        borderWidth: 0,
        borderColor: 'black',
        marginBottom: 10,
        justifyContent: "center",
        alignItems: "center",
        borderRadius: 4,
    },
    textInput: {
        width: 200,
        height: 44,
        padding: 10,
        textAlign:'right',
        borderWidth: 1,
        borderColor: 'black',
        marginBottom: 10,
    },
});
export default OrderComponent;

