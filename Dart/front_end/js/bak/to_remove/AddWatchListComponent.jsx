import React from 'react';
import { View, Text, TextInput, SafeAreaView, Dimensions, TouchableHighlight, TouchableOpacity, StyleSheet, ScrollView } from 'react-native'
import { SearchBar, Button, Divider } from 'react-native-elements'
import Constants from 'expo-constants';
import { RecyclerListView, DataProvider, LayoutProvider } from "recyclerlistview";
import { MaterialIcons } from 'react-native-vector-icons';


const SCREEN_WIDTH = Dimensions.get("window").width;
/*
https://snack.expo.io/@arunreddy10/rlv-extendedstate-demo
*/

class ScrollViewWithHeader extends React.Component {
    constructor(props) {
        super(props);
    }
    render () {
        console.log(this.props.extendedState)
        return  (
            <>
                <Text> headerheader </Text>
                <Divider style={{ backgroundColor: 'blue'}} />
                <ScrollView {...this.props} />
            </>
        )
    }
}
const disc = [
{ id:1,
 title: '단일판매 공급계약',
},
{ id:2,
title: '공개매수 신고서',
},
{ id:3,
title:'자기주식취득결정',
}
]
class AddWatchListComponent extends React.Component {
    constructor(props) {
        super(props);
        this.handleSelectItem = this.handleSelectItem.bind(this)
        this.searchItem = this.searchItem.bind(this)
        this.onFocus = this.onFocus.bind(this)
        this.onBlur = this.onBlur.bind(this)
        this.onCancel = this.onCancel.bind(this)
        this.onClear = this.onClear.bind(this)

        this.onFocus2 = this.onFocus2.bind(this)
        this.onBlur2 = this.onBlur2.bind(this)
        this.onCancel2 = this.onCancel2.bind(this)
        this.onClear2 = this.onClear2.bind(this)

        this._layoutProvider = new LayoutProvider(
            index => {
                return 0;
            },
            (type, dim) => {
                dim.width = SCREEN_WIDTH;
                dim.height = 25;
            }
        );
        this._rowRenderer = this._rowRenderer.bind(this);
        this._layoutProvider2 = new LayoutProvider(
            index => {
                return 0;
            },
            (type, dim) => {
                dim.width = SCREEN_WIDTH;
                dim.height = 30;
            }
        );
  let dataProvider2 = new DataProvider((r1, r2) => {
            return r1 !== r2;
        })

        this._rowRenderer2 = this._rowRenderer2.bind(this);
        this.state = {
            focus: true,
            search: '',
            visibleItems: false,
            visibleDiscs: false,
            stock_list: [],
            dataProvider: new DataProvider(
                (r1, r2) => {
                    return r1 !== r2;
                },
                (index) => this.state.stock_list[index].code
            ),
            dataProvider2: dataProvider2.cloneWithRows(disc),
            extendedState: {
                selected: {},
            },
            extendedState2: {
                selected: {},
            }
        };
    }

    componentDidUpdate(prevProps) {
        const { stock_list } = this.props
        if (prevProps.stock_list === stock_list) {
            return
        }
        this.setState({
            stock_list: stock_list,
            dataProvider: this.state.dataProvider.cloneWithRows(stock_list)
        })
    }

    handleDeselectItem(index, code) {
    }

    handleSelectItem(index, code) {
        let selectedItems = this.state.extendedState.selected;
        let stock_list = this.state.stock_list.filter(stock=>stock.code!==code);


        console.log(index, code);
        if (selectedItems.length > 0) {
        selectedItems.map( (item, idx) => {
                console.log('selectedItems22', idx)
                if (item.code === code) {
                }
            }
        )
        }

        selectedItems = [selectedItems, {code:code, index:index}]
        this.setState({
            extendedState: {
                selected: selectedItems
            },
            stock_list: stock_list,
            dataProvider: this.state.dataProvider.cloneWithRows(stock_list)
        })
        return
/*
        [{code:'005930', index:1},
         {code:'005930', index:2},
        ]

        index code selectedItems
        selectedItems = [
        ]
        */
        if (code in selectedItems) {
            delete selectedItems[code];
        } else {
            selectedItems[code] = 'true'
        }

        this.setState({
            extendedState: {
                selected: selectedItems
            },
            stock_list: stock_list,
            dataProvider: this.state.dataProvider.cloneWithRows(stock_list)
        })
    }

    /* 선택한것은 위에 나와야 함 */
    /* 선택한것과 선택하지 않은것 사이에는 길게 있어야 함 */
    _rowRenderer(type, stock, index, extendedState) {
        return (
            <View>
                <TouchableOpacity
                    style={styles.flexRow}
                    onPress={() =>this.handleSelectItem(index, stock.code)}>
                    <Text> {stock.name} </Text>
                    { extendedState.selected[stock.code] &&
                        <MaterialIcons name="done" />
                    }
                </TouchableOpacity>
            </View>
        )
    }

    _rowRenderer2(type, disc, index, extendedState) {
        console.log(disc)
        return (
            <View>
                <TouchableOpacity
                    style={styles.flexRow} >
                    <Text> {disc['title']} </Text>
                </TouchableOpacity>
            </View>
        )
    }

    searchItem(value) {
        this.setState({
            search: value,
            dataProvider: this.state.dataProvider.cloneWithRows(
                this.state.stock_list.filter(
                    x => x.name && x.name.indexOf(value) > -1
                )
            )
        })
    }

    onFocus() {
        this.setState({visibleItems:true})
        console.log('onFOcus')
    }

    onBlur() {
        this.setState({focus:false})
        console.log('onBlur')
    }

    onCancel() {
        this.setState({visibleItems:false})
        alert('onCancel')
        console.log('onCancel')
    }

    onClear() {
        this.setState({visibleItems:false})
        alert('onClear')
        console.log('onCancel')
    }

    onFocus2() {
        this.setState({visibleDiscs:true})
        console.log('onFOcus')
    }

    onBlur2() {
        this.setState({focus:false})
        console.log('onBlur')
    }

    onCancel2() {
        this.setState({visibleDiscs:false})
        alert('onCancel')
        console.log('onCancel')
    }

    onClear2() {
        this.setState({visibleDiscs:false})
        alert('onClear')
        console.log('onCancel')
    }

/*
https://github.com/toystars/react-native-multiple-select
*/
    render() {
        if (this.props.stock_list.length <= 0) {
            return <></>
        }
/*
const someMethod = 'someMethod'
return  ( <>
<SearchBar
  onChangeText={someMethod}
  onClearText={someMethod}
 showLoading
  platform="ios"
  cancelButtonTitle="Cancel"
  placeholder='Type Here...' />

<SearchBar
  onChangeText={someMethod}
  onClearText={someMethod}
        // noIcon={true}
        icon = {{type: 'material-community', color: '#86939e', name: 'share' }}
        clearIcon = {{type: 'material-community', color: '#86939e', name: 'share' }}
  placeholder='Type Here...' />

<SearchBar
  round
inputStyle={{backgroundColor: 'white'}}
    containerStyle={{backgroundColor: 'white', borderWidth: 1, borderRadius: 5}}
  onChangeText={someMethod}
  onClearText={someMethod}
  placeholder='Type Here...' />

<SearchBar
  lightTheme
  onChangeText={someMethod}
  onClearText={someMethod}
  placeholder='Type Here...' />

<SearchBar
  lightTheme
  onChangeText={someMethod}
  onClearText={someMethod}
  icon={{ type: 'font-awesome', name: 'search' }}
  placeholder='Type Here...' />
<SearchBar
  value="The boy"
  platform="ios"
  clearIcon={{
    iconStyle: { margin: 10 },
    containerStyle: { margin: -10 },
  }}
/>
<SearchBar
  value="The boy"
  platform="ios"
icon = {{name:'cached'}}
/>
<SearchBar
lightTheme
icon = {"share-alt", "red"}
inputStyle={{margin: 0, padding:3, flex:1}}
containerStyle={{flex:1, height:undefined}}
onChangeText={() => {}}
placeholder='ABC' />
</>
)
*/

        return (
            <>
                <Text> 회사명 </Text>
                <SearchBar
                    placeholder="Search"
                    onChangeText={this.searchItem}
                    value={this.state.search}
                    onFocus={this.onFocus}
                    platform='ios'
                    onBlur={this.onBlur}
                    onCancel={this.onCancel}
                    onClear={this.onClear}
                />
            <View style={styles.container} >
                {this.state.visibleItems && 
                <RecyclerListView
                        layoutProvider={this._layoutProvider}
                        dataProvider={this.state.dataProvider}
                        rowRenderer={this._rowRenderer}
                        extendedState={this.state.extendedState}
                        style={{ transform: [{ scaleY: 1 }] }}
                        externalScrollView={ScrollViewWithHeader}
                />
                }
                <Text> 공시유형 </Text>
                <RecyclerListView
                        layoutProvider={this._layoutProvider2}
                        dataProvider={this.state.dataProvider2}
                        rowRenderer={this._rowRenderer2}
                        extendedState={this.state.extendedState2}
                        style={{ transform: [{ scaleY: 1 }] }}
                />
                <Text> 등록할 키워드 </Text>
            </View>
            </>
        )
        return (
            <View>
                <Text> 회사명 </Text>
                <Text> 공시유형 </Text>
                <Text> 등록할 키워드 </Text>
                <TextInput
                    style={{height: 40}}
                    placeholder="Type here to add a new keyword !"
                    onChangeText={(text) => this.setState({text})}
                    value={this.state.text}
                />
                <Button title="등록" onPress={ () => this.handlePress()} />
            </View>
        )
    }
}

const styles = StyleSheet.create({
    container: {
        backgroundColor: '#fff',
        justifyContent: 'center',
        height:500
    },
    flexRow: {
        flex:1,
        flexDirection: 'row',
        alignItems:'flex-start',
    }
})

export default AddWatchListComponent;

/*
<Button title="등록" onPress={ () => this.props.navigation.navigate('Home')} />
const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: Constants.statusBarHeight,
  },
  item: {
    backgroundColor: '#f9c2ff',
    padding: 20,
    marginVertical: 8,
    marginHorizontal: 16,
  },
  title: {
    fontSize: 32,
  },
});
*/
