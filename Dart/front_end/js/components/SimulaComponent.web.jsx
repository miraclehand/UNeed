import React from 'react';
import { Text, Platform, StyleSheet, View, Dimensions } from 'react-native';
import * as Font from 'expo-font';
import { ListItem, Button } from 'react-native-elements'
import { RecyclerListView, DataProvider, LayoutProvider } from "recyclerlistview";

const SCREEN_WIDTH = Dimensions.get("window").width;

export default class SimulaComponent extends React.Component {
    constructor(props) {
        super(props);

        this.handlePress = this.handlePress.bind(this)
        this.handleLongPress = this.handleLongPress.bind(this)

        this._layoutProvider = new LayoutProvider(
            index => {
                return 0;
            },
            (type, dim) => {
                dim.width = SCREEN_WIDTH;
                dim.height = 73;
            }
        );

        this._rowRenderer = this._rowRenderer.bind(this);
        const dataProvider = new DataProvider((r1, r2) => { return r1 !== r2; })

        this.state = {
            modalVisible: false,
            simula: {},
            dataProvider: dataProvider.cloneWithRows(this.props.simulas),
        };
    }

    handlePress(simula) {
        this.props.handlePress(simula)
    }

    handleLongPress(simula) {
        this.setState({modalVisible:true, simula})
    }

    componentDidUpdate(prevProps) {
        const { simulas } = this.props

        if (prevProps.simulas === simulas) {
            return
        }
        const dataProvider = this.state.dataProvider.cloneWithRows(simulas)

        this.setState({ dataProvider })
    }

    _rowRenderer(type, simula, index, extendedState) {
        const avatar_url =  'https://s3.amazonaws.com/uifaces/faces/twitter/ladylexy/128.jpg'
        return (
            <ListItem
                key={index}
                leftAvatar={{ source: { uri: avatar_url } }}
                title={simula.name}
                subtitle={simula.std_disc.report_nm+' ['+simula.stock_names+']'}
                bottomDivider
                onPress = {() => this.handlePress(simula)}
                onLongPress = {() => this.handleLongPress(simula)}
            />
        )
    }


    render() {
        return (
            <RecyclerListView
                layoutProvider={this._layoutProvider}
                dataProvider={this.state.dataProvider}
                rowRenderer={this._rowRenderer}
                style={{ flex:1 }}
            />
        )
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#f5fcff"
  }
});
