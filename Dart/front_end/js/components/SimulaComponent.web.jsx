import React from 'react';
import { Text, Platform, StyleSheet, View, Dimensions, TouchableOpacity, TouchableHighlight } from 'react-native';
import * as Font from 'expo-font';
import { ListItem, Button } from 'react-native-elements'
import { RecyclerListView, DataProvider, LayoutProvider } from "recyclerlistview";
let Modal;
const SCREEN_WIDTH = Dimensions.get("window").width;
const SCREEN_HEIGHT = Dimensions.get("window").height;

export default class SimulaComponent extends React.Component {
    constructor(props) {
        super(props);

        this.handlePress = this.handlePress.bind(this)
        this.handleLongPress = this.handleLongPress.bind(this)
        this.onButtonPress = this.onButtonPress.bind(this)
        this.onButtonPressDelete = this.onButtonPressDelete.bind(this)
        this._rowRenderer = this._rowRenderer.bind(this);

        this.modalHeader = this.modalHeader.bind(this)
        this.modalBody   = this.modalBody.bind(this)
        this.modalContainer= this.modalContainer.bind(this)
        this.modal = this.modal.bind(this)

        if (this.props.os === 'web') {
            Modal = require('./WebModal').default;
        } else {
            Modal = require('react-native').Modal;
        }

        let height = 61
        if (SCREEN_HEIGHT > 900) {
            height = 67
        }
        if (SCREEN_HEIGHT > 950) {
            height = 73
        }

        this._layoutProvider = new LayoutProvider(
            index => {
                return 0;
            },
            (type, dim) => {
                dim.width = SCREEN_WIDTH;
                dim.height = height;
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

modalHeader() {
    return (
        <View style={styles.modalHeader}>
            <Text style={styles.title}> {this.state.simula.name} </Text>
            <View style={styles.divider} />
        </View>
    )
}

onButtonPress() {
    console.log('onButtonPress')
}

onButtonPressDelete() {
    const simulas = this.props.simulas.filter(simula =>simula !== this.state.simula)
    const dataProvider = this.state.dataProvider.cloneWithRows(simulas)

    this.props.handleDelete(this.state.simula)
    this.setState({dataProvider, modalVisible:false});
}

modalBody() {
    return (
        <View style={styles.modalBody}>
            <TouchableOpacity onPress={this.onButtonPress}>
                <Text style={styles.detail}>Add to Favorites</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={this.onButtonPress}>
                <Text style={styles.detail}>Edit name</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={this.onButtonPressDelete}>
                <Text style={styles.detail}>Delete</Text>
            </TouchableOpacity>
        </View>
    )
}

modalContainer() {
    return (
    <View style={styles.modalContainer}>
      {this.modalHeader()}
      {this.modalBody()}
    </View>
    )
}

modal () {
    if (!this.state.modalVisible) {
        return <></>
    }

    return (
    <Modal
      transparent={true}
        animationType="slide"
      visible={this.state.modalVisible}
      onRequestClose={() => {
        Alert.alert('Modal has been closed.');
      }}>
      <View style={styles.modal}>
        <View>
          {this.modalContainer()}
        </View>
      </View>
    </Modal>
    )
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
        const title = simula.name
        const subtitle = simula.std_disc.report_nm+' ['+simula.stock_names+']'
        return (
            <ListItem
                key={index}
                bottomDivider
                onPress = {() => this.handlePress(simula)}
                onLongPress = {() => this.handleLongPress(simula)}
                leftAvatar={{ source: { uri: avatar_url } }}
            >
                <ListItem.Content>
                    <ListItem.Title> {title} </ListItem.Title>
                    <ListItem.Subtitle> {subtitle} </ListItem.Subtitle>
                </ListItem.Content>
            </ListItem>

        )
    }


    render() {
        return (
            <>
                <TouchableOpacity
                    style={{ flex:1 }}
                    onPress={() => {
                    this.setState({modalVisible:false});
                }}>
                    {this.modal()}
                    {this.state.dataProvider._size > 0 &&
                    <RecyclerListView
                        layoutProvider={this._layoutProvider}
                        dataProvider={this.state.dataProvider}
                        rowRenderer={this._rowRenderer}
                        extendedState={this.state.extendedState}
                        style={{ flex:1 }}
                    />
                    }
                </TouchableOpacity>
            </>
        )
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#f5fcff"
  },
  modal:{
    backgroundColor:"#00000099",
    flex:1,
    alignItems: 'center',
    justifyContent: 'center',
    width:"100%",
  },
  modalContainer:{
    backgroundColor:"#f9fafb",
    borderRadius:5,
  },
  modalHeader:{
  },
  modalBody:{
    backgroundColor:"#fff",
    paddingVertical:20,
    paddingHorizontal:10,
  },
 title:{
    fontWeight:"bold",
    fontSize:20,
    padding:15,
    color:"#000"
  },
  detail: {
    fontSize:15,
    padding:15,
    color:"#000"
  },
  divider:{
    width:"100%",
    height:1,
    backgroundColor:"lightgray"
  },

});
