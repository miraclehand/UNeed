import React from 'react';
import { View, Text, TextInput, Dimensions, TouchableOpacity, StyleSheet, FlatList } from 'react-native'
import { SearchBar, Button } from 'react-native-elements'
import Constants from 'expo-constants';
import { RecyclerListView, DataProvider, LayoutProvider } from "recyclerlistview";
import { Feather } from 'react-native-vector-icons';

import { findText, getDisassembled } from '../util/textUtil';
//import DatePicker from "react-datepicker";
//import "react-datepicker/dist/react-datepicker.css";

const SCREEN_WIDTH = Dimensions.get("window").width;

class CreateUnitComponent extends React.Component {
    constructor(props) {
        super(props);

        this.searchStock = this.searchStock.bind(this)
        this.handleSelectStock = this.handleSelectStock.bind(this)
        this.handleDeselectStock = this.handleDeselectStock.bind(this)

        this._rowRenderer = this._rowRenderer.bind(this);
        this.renderSelectedStock = this.renderSelectedStock.bind(this)
        this.addUnitStock = this.addUnitStock.bind(this)
        this.delUnitStock = this.delUnitStock.bind(this)
        this.handleChangeDate = this.handleChangeDate.bind(this)

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
            value: '',
            s_date: this.props.unitSDate,
            e_date: this.props.unitEDate,
            dataProvider: dataProvider.cloneWithRows(this.props.stocks),
            extendedState: {
                selected: [],
            },
        };
    }

    componentDidUpdate(prevProps) {
        const { stocks } = this.props

        if (prevProps.stocks === stocks) {
            return
        }
        const dataProvider = this.state.dataProvider.cloneWithRows(stocks)

        this.setState({ dataProvider })
    }

    addUnitStock(unitStocks, newStock) {
        let index = -1

        unitStocks.map((stock, idx) => {
            if (index >= 0) {
                return
            }
            if (stock.id > newStock.id) {
                index = idx
            }
        })
        if (index == -1) {
            index = unitStocks.length
        }

        return [
            ...unitStocks.slice(0,index),
            newStock,
            ...unitStocks.slice(index)
        ]
    }

    delUnitStock(unitStocks, delStock) {
        return unitStocks.filter(stock=>stock !== delStock)
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

    handleSelectStock(newStock) {
        let unitStocks = this.props.unitStocks;

        const stocks = this.props.stocks.filter( stock =>
            findText(stock.dname, this.state.value) > -1
        );
        const dataProvider = this.state.dataProvider.cloneWithRows(stocks)

        /* 전체를 선택한 적이 있다면, */
        if (unitStocks.filter(stock => stock.code === '000000').length > 0) {
            unitStocks = []
        }

        if (newStock.code === '000000') {
            unitStocks = [newStock]
        } else {
            if (unitStocks.indexOf(newStock) === -1) {
                unitStocks = this.addUnitStock(unitStocks, newStock)
            } else {
                unitStocks = this.delUnitStock(unitStocks, newStock)
            }
        }

        const extendedState = {
            selected: unitStocks
        }

        this.setState({ dataProvider, extendedState })
        this.props.handleUnitStocks(unitStocks)
    }

    handleDeselectStock(delStock) {
        let unitStocks = this.props.unitStocks.filter(stock=>
            stock.code !== delStock.code
        );

        const stocks = this.props.stocks.filter(stock =>
            findText(stock.dname, this.state.value) > -1
        );

        const dataProvider = this.state.dataProvider.cloneWithRows(stocks)
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

    renderSelectedStock(item) {
        return (
            <Button
                buttonStyle={{borderRadius:25, marginLeft:10}}
                titleStyle={{marginLeft:5}}
                type = "outline"
                title = {item.item.name}
                onPress={() => this.handleDeselectStock(item.item)}
                icon = { <Feather size={15} name="x-circle" /> }
            />
        )
    }

    handleChangeDate(id, date) {
        if (id === 1) {
            this.setState({s_date:date})
            this.props.handleUnitSDate(date)
        } else {
            this.setState({e_date:date})
            this.props.handleUnitEDate(date)
        }
    }
    render() {
        return (
            <>
                <TextInput
                    style={styles.input}
                    placeholder='Type Name'
                    underlineColorAndroid='transparent'
                    autoCapitalize='none'
                    onChangeText={this.props.handleUnitName}
                />
                {/*this.props.simula &&
                    <>
                        <DatePicker
                            dateFormat='yyyy/MM/dd'
                            selected={this.state.s_date}
                            onChange={(date) => this.handleChangeDate(1, date) }
                        />
                        <DatePicker
                            dateFormat='yyyy/MM/dd'
                            selected={this.state.e_date}
                            onChange={(date) => this.handleChangeDate(2, date) }
                        />
                    </>
               */ }
                {this.props.unitStocks.length > 0 &&
                    <View style={{ height:'6%' }} >
                    <FlatList
                        data = {this.props.unitStocks}
                        horizontal 
                        keyExtractor={item=>item.code}
                        renderItem = {this.renderSelectedStock}
                    />
                    </View>
                }
                <SearchBar
                    placeholder={this.state.placeholder}
                    onChangeText={this.searchStock}
                    value={this.state.value}
                    platform='ios'
                />
                {this.state.dataProvider._size > 0 &&
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

const styles = StyleSheet.create({
    container: {
        backgroundColor: '#fff',
        justifyContent: 'center',
        flex:1,
    },
    flexRow: {
        flex:1,
        flexDirection: 'row',
        alignItems:'flex-start',
    },
    container2: {
        backgroundColor: '#fff',
        justifyContent: 'center',
        height:100
    },
    input: {
        margin: 15,
        height: 40,
        borderColor: "#7a42f4",
        borderWidth: 1
    },
})

export default CreateUnitComponent;
