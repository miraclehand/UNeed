import React from 'react';
import { View, Text, TextInput, Dimensions, TouchableOpacity, StyleSheet, FlatList } from 'react-native'
import { Badge, SearchBar, Button, Divider } from 'react-native-elements'
import Constants from 'expo-constants';
import { RecyclerListView, DataProvider, LayoutProvider } from "recyclerlistview";
import { Feather } from 'react-native-vector-icons';
import { getDisassembled } from '../util/search';

const SCREEN_WIDTH = Dimensions.get("window").width;

class SetupWatchComponent extends React.Component {
    constructor(props) {
        super(props);

        this.searchStdDisc = this.searchStdDisc.bind(this)
        this.handleSelectStdDisc = this.handleSelectStdDisc.bind(this)
        this.handleDeselectStdDisc = this.handleDeselectStdDisc.bind(this)

        this._rowRenderer = this._rowRenderer.bind(this);
        this.renderSelectedStdDisc = this.renderSelectedStdDisc.bind(this)

        this.onFocus = this.onFocus.bind(this)

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
            placeholder: 'Search Discs...',
            value: '',
            visibleItems: true,
            dataProvider: dataProvider.cloneWithRows(this.props.list_std_disc)
        };
    }

    componentDidUpdate(prevProps) {
        const { list_std_disc } = this.props

        if (prevProps.list_std_disc === list_std_disc) {
            return
        }
        const dataProvider=this.state.dataProvider.cloneWithRows(list_std_disc)

        this.setState({ dataProvider })
    }

    searchStdDisc(value) {
        const std_discs = this.props.list_std_disc.filter( std_disc =>
            std_disc.report_dnm.indexOf(getDisassembled(value)) > -1
        );

        const dataProvider = this.state.dataProvider.cloneWithRows(discs)
        this.setState({ value, dataProvider })
    }

    handleSelectStdDisc(newStdDisc) {
        const std_discs = this.props.list_std_disc.filter( std_disc =>
            std_disc.report_nm.indexOf(this.state.value) > -1
         && std_disc.id !== newStdDisc.id
        );

        const dataProvider = this.state.dataProvider.cloneWithRows(std_discs)

        this.setState({ dataProvider, visibleItems:false })
        this.props.changeWatchStdDisc(newStdDisc)
    }

    onFocus() {
        this.setState({ visibleItems:true })
    }

    handleDeselectStdDisc(delStdDisc) {
        this.props.changeWatchStdDisc('')
        this.onFocus()
    }

    _rowRenderer(type, item, index, extendedState) {
        return (
            <Button
                style = {{ alignItems: 'flex-start', justifyContent:'center'}}
                titleStyle={{marginLeft:5}}
                type = "clear"
                title = {item.report_nm}
                onPress={() => this.handleSelectStdDisc(item)}
                icon = { <Feather size={15} name="square" /> }
            />
        )
    }

    renderSelectedStdDisc(item) {
        return (
            <Button
                buttonStyle={{borderRadius:25, marginLeft:10}}
                titleStyle={{marginLeft:5}}
                type = "outline"
                title = {item.item.report_nm}
                onPress={() => this.handleDeselectStdDisc(item.item)}
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
                {this.props.watchStdDisc &&
                    <View style={{ height:'6%' }} >
                        <FlatList
                            data = {[this.props.watchStdDisc]}
                            horizontal
                            renderItem = {this.renderSelectedStdDisc}
                        />
                    </View>
                }
                <SearchBar
                    placeholder={this.state.placeholder}
                    onChangeText={this.searchStdDisc}
                    value={this.state.value}
                    onFocus={this.onFocus}
                    platform='ios'
                />
                {this.state.visibleItems &&
                <RecyclerListView
                    layoutProvider={this._layoutProvider}
                    dataProvider={this.state.dataProvider}
                    rowRenderer={this._rowRenderer}
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
})

export default SetupWatchComponent;
