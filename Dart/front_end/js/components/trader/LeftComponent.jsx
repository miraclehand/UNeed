import React from 'react';
import { RecyclerListView, DataProvider, LayoutProvider } from 'recyclerlistview';
import { Button } from 'react-native-elements'

import { TouchableOpacity, CheckBox, StyleSheet, Text, View, TextInput, Dimensions } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const SCREEN_WIDTH = Dimensions.get("window").width;

class LeftComponent extends React.Component {
    constructor(props) {
        super(props);

        this.genTableHeader = this.genTableHeader.bind(this);
        this.genTableBody = this.genTableBody.bind(this);
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

    _rowRenderer(type, row, index, extendedState) {
        return (
            <TouchableOpacity
                key={index}
                style={styles.tableRow}
                onPress={() => this.props.handleSelect(row) }
            >
                {row.map( (column) => {
                    return (
                        <Text style={styles.columnRowTxt0}>{column}</Text>
                    )}
                )}
            </TouchableOpacity>
        )
    }

    genTableHeader() {
        const { columns } = this.props
                    
        return (
            <View style={styles.tableHeader}>
                {columns.map((column, index) => {
                    return (
                        <TouchableOpacity
                            key={index}
                            style={styles.columnHeader0}
                        >
                            <Text style={styles.columnHeaderTxt}>{column + " "}
                            </Text>
                        </TouchableOpacity>
                    )
                })}
            </View>
        )
    }

    genTableBody() {
        return (
            <View style= {{flex:1}}>
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
        )
    }
    render() {
        return (
            <View style={styles.container} >
                <View style={{width: '100%', height: '70%' }}>
                    { this.genTableHeader() }
                    { this.genTableBody() }
                </View>
                <View style={{width: '100%', height: '30%' }}>
                    <Button
                        titleStyle={{marginLeft:5}}
                        type = "clear"
                        title = '조회'
                        onPress = { this.props.handleQuery }
                        iconContainerStyle={{ marginLeft:50}}
                    />
                </View>
            </View>
        )
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
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
    columnHeaderTxt: {
        color: "white",
        fontWeight: "bold",
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
});
export default LeftComponent;
