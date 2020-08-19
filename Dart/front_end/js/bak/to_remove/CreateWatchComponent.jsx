import React from 'react';
import { View, Text, TextInput, Dimensions, TouchableOpacity, StyleSheet, FlatList } from 'react-native'
import { Badge, SearchBar, Button, Divider } from 'react-native-elements'
import Constants from 'expo-constants';
import { RecyclerListView, DataProvider, LayoutProvider } from "recyclerlistview";
import { Feather } from 'react-native-vector-icons';

import { getDisassembled } from '../util/search';

const SCREEN_WIDTH = Dimensions.get("window").width;

class CreateWatchComponent extends React.Component {
    constructor(props) {
        super(props);

        this.searchStock = this.searchStock.bind(this)
        this.handleSelectStock = this.handleSelectStock.bind(this)
        this.handleDeselectStock = this.handleDeselectStock.bind(this)

        this._rowRenderer = this._rowRenderer.bind(this);
        this.renderSelectedStock = this.renderSelectedStock.bind(this)
        this.addWatch = this.addWatch.bind(this)
        this.delWatch = this.delWatch.bind(this)

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

    addWatch(items, newItem) {
        let index = -1

        items.map((item, idx) => {
            if (index >= 0) {
                return
            }
            if (item.id > newItem.id) {
                index = idx
            }
        })
        if (index == -1) {
            index = items.length
        }

        return [
            ...items.slice(0,index),
            newItem,
            ...items.slice(index)
        ]
    }

    delWatch(watchStocks, delItem) {
        return watchStocks.filter(stock=>stock.code != delItem.code)
    }

    searchStock(value) {
        const stocks = this.props.list_stock.filter( stock =>
            stock.dname.indexOf(getDisassembled(value)) > -1
        );

        const dataProvider = this.state.dataProvider.cloneWithRows(stocks)
        this.setState({ value, dataProvider })
    }

    handleSelectStock(newStock) {
        let watchStocks = this.props.watchStocks;

        const stocks = this.props.list_stock.filter( stock =>
            stock.dname.indexOf(getDisassembled(this.state.value)) > -1
        );
        /*
        const stocks = this.props.list_stock.filter( stock =>
            stock.dname.indexOf(getDisassembled(this.state.value)) > -1
         && watchStocks.indexOf(stock) === -1
         && stock.code !== newStock.code
        */

        const dataProvider = this.state.dataProvider.cloneWithRows(stocks)

        /* 전체를 선택한 적이 있다면, */
        if (watchStocks.filter(stock => stock.code === '000000').length > 0) {
            watchStocks = []
        }

        if (newStock.code === '000000') {
            watchStocks = [newStock]
        } else {
            if (watchStocks.indexOf(newStock) === -1) {
                watchStocks = this.addWatch(watchStocks, newStock)
            } else {
                watchStocks = this.delWatch(watchStocks, newStock)
            }
        }

        const extendedState = {
            selected: watchStocks
        }

        this.setState({ dataProvider, extendedState })
        this.props.changeWatchStocks(watchStocks)
    }

    handleDeselectStock(delStock) {
        let watchStocks = this.props.watchStocks.filter(stock=>
            stock.code!==delStock.code
        );

        const stocks = this.props.list_stock.filter( stock =>
            stock.name.indexOf(this.state.value) > -1
        );

        const dataProvider = this.state.dataProvider.cloneWithRows(stocks)
        const extendedState = {
            selected: watchStocks
        }

        this.setState({ dataProvider, extendedState })
        this.props.changeWatchStocks(watchStocks)
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
        return(
            <TouchableOpacity
                style ={{flex:1,marginLeft: 30,justifyContent: 'center', alignItems: 'center' }}
                onPress={() => this.handleDeselectStock(item.item)}
            >
                <Badge value = 'x' status='error' containerStyle={{position:'absolute', top:8, right:-10}} />
                <Text>{item.item.name}</Text>
            </TouchableOpacity>
        );
    }

    render() {
        return (
            <>
                <TextInput
                    style={styles.input}
                    placeholder='Type Watch Name'
                    underlineColorAndroid='transparent'
                    autoCapitalize='none'
                    onChangeText={this.props.changeWatchName}
                />
                {this.props.watchStocks.length > 0 &&
                    <View style={{ height:'6%' }} >
                    <FlatList
                        data = {this.props.watchStocks}
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

export default CreateWatchComponent;
