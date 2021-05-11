import React from 'react';
import { View, Text, TextInput, Dimensions, TouchableOpacity, StyleSheet, FlatList } from 'react-native'
import { Badge, SearchBar, Button, Divider } from 'react-native-elements'
import { RecyclerListView,DataProvider,LayoutProvider } from "recyclerlistview";
import { Feather } from 'react-native-vector-icons';

import { getDisassembled } from '../util/search';

const SCREEN_WIDTH = Dimensions.get("window").width;

class SearchStockComponent extends React.Component {
    constructor(props) {
        super(props);

        this.searchStock = this.searchStock.bind(this)
        this.handleSelectStock = this.handleSelectStock.bind(this)
        this.handleDeselectStock = this.handleDeselectStock.bind(this)

        this._rowRenderer = this._rowRenderer.bind(this);
        this.renderSelectedStock = this.renderSelectedStock.bind(this)
        this.addStock = this.addStock.bind(this)
        this.delStock = this.delStock.bind(this)

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
            dataProvider: dataProvider.cloneWithRows(this.props.list_stock),
            extendedState: {
                selected: [],
            },
        };
    }

    componentDidUpdate(prevProps) {
        const { list_stock } = this.props

        if (prevProps.list_stock === list_stock) {
            return
        }
        const dataProvider = this.state.dataProvider.cloneWithRows(list_stock)

        this.setState({ dataProvider })
    }

    addStock(selectedStocks, newStock) {
        let index = -1

        selectedStocks.map((item, idx) => {
            if (index >= 0) {
                return
            }
            if (item.id > newStock.id) {
                index = idx
            }
        })
        if (index == -1) {
            index = selectedStocks.length
        }

        return [
            ...selectedStocks.slice(0,index),
            newStock,
            ...selectedStocks.slice(index)
        ]
    }

    delStock(selectedStocks, delStock) {
        return selectedStocks.filter(stock=>stock.code != delStock.code)
    }

    searchStock(value) {
        const new_stocks = this.props.list_stock.filter( stock =>
            stock.dname.indexOf(getDisassembled(value)) > -1
        );

        const dataProvider = this.state.dataProvider.cloneWithRows(new_stocks)
        this.setState({ value, dataProvider })
    }

    handleSelectStock(newStock) {
        let selectedStocks = this.props.selectedStocks;

        const new_stocks = this.props.list_stock.filter( stock =>
            stock.dname.indexOf(getDisassembled(this.state.value)) > -1
        );

        const dataProvider = this.state.dataProvider.cloneWithRows(new_stocks)

        /* 전체를 선택한 적이 있다면, */
        if (selectedStocks.filter(stock => stock.code === '000000').length > 0) {
            selectedStocks = []
        }

        if (newStock.code === '000000') {
            selectedStocks = [newStock]
        } else {
            if (selectedStocks.indexOf(newStock) === -1) {
                selectedStocks = this.addStock(selectedStocks, newStock)
            } else {
                selectedStocks = this.delStock(selectedStocks, newStock)
            }
        }

        const extendedState = {
            selected: selectedStocks
        }

        this.setState({ dataProvider, extendedState })
        this.props.handleSelectStocks(selectedStocks)
    }

    handleDeselectStock(delStock) {
        let selectedStocks = this.props.selectedStocks.filter(stock=>
            stock.code !== delStock.code
        );

        const new_stocks = this.props.list_stock.filter( stock =>
            stock.name.indexOf(this.state.value) > -1
        );

        const dataProvider = this.state.dataProvider.cloneWithRows(new_stocks)
        const extendedState = {
            selected: selectedStocks
        }

        this.setState({ dataProvider, extendedState })
        this.props.handleSelectStocks(selectedStocks)
    }

    _rowRenderer(type, stock, index, extendedState) {
        const icon = extendedState.selected.filter( s =>
            s.code === stock.code
        )[0] === stock ? 'check-square' : 'square'

        return (
            <Button
                style = {{ alignItems: 'flex-start', justifyContent:'center' }}
                titleStyle={{marginLeft:5}}
                type = "clear"
                title = {stock.name}
                onPress={() => this.handleSelectStock(stock)}
                iconContainerStyle={{ marginLeft:50}}
                icon = { <Feather size={15} name={icon} /> }
            />
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
                icon = {
                    <Feather 
                        size={15}
                        name="x-circle" />
                }
            />
        )
    }

    render() {
        return (
            <>
                {this.props.selectedStocks.length > 0 &&
                    <View style={{ height:'6%' }} >
                    <FlatList
                        data = {this.props.selectedStocks}
                        horizontal 
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
                <RecyclerListView
                    layoutProvider={this._layoutProvider}
                    dataProvider={this.state.dataProvider}
                    rowRenderer={this._rowRenderer}
                    extendedState={this.state.extendedState}
                    style={{ flex:1 }}
                />
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

export default SearchStockComponent;
