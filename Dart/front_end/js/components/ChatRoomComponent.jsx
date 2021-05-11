import React from 'react';
import { StyleSheet, Button, Dimensions } from 'react-native'
import { RecyclerListView, DataProvider,LayoutProvider } from 'recyclerlistview'
import Constants from 'expo-constants';
import {TouchableOpacity, Text, TouchableHighlight, View, Alert } from 'react-native';
import { ListItem } from 'react-native-elements'

let Modal;

const SCREEN_WIDTH = Dimensions.get("window").width;
const SCREEN_HEIGHT = Dimensions.get("window").height;

class ChatRoomComponent extends React.Component {
    constructor(props) {
        super(props);

        this.handlePress = this.handlePress.bind(this)
        this.handleLongPress = this.handleLongPress.bind(this)
        this.onButtonPress = this.onButtonPress.bind(this)
        this.onButtonPressDelete = this.onButtonPressDelete.bind(this)
        this.onButtonPressClose = this.onButtonPressClose.bind(this)
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
        if (SCREEN_HEIGHT > 1000) {
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
        const dataProvider = new DataProvider((r1, r2) => { return r1 !== r2; })

        this.state = {
            modalVisible: false,
            dataProvider: dataProvider.cloneWithRows(this.props.rooms),
        }
    }
    componentDidUpdate(prevProps) {
        console.log('componentDidUpdate')
        const { rooms } = this.props

        if (prevProps.rooms === rooms) {
            return
        }
        const dataProvider = this.state.dataProvider.cloneWithRows(rooms)
        this.setState({ dataProvider })
    }

    _rowRenderer(type, room, index, extendedState) {
        const title = room.watch_name
        const subtitle = room.last_label
        return (
            <ListItem
                key={index}
                bottomDivider
                style = {{ flex : 1 }}
                onPress = {() => this.handlePress(room)}
                onLongPress = {() => this.handleLongPress(room)}
            >
                <ListItem.Content>
                    <ListItem.Title> {title} </ListItem.Title>
                    <ListItem.Subtitle> {subtitle} </ListItem.Subtitle>
                </ListItem.Content>
                {room.badge > 0 &&
                <View style={[styles.badgeCycle, {right:20,width:24,top:30}] } >
                    <Text style={styles.badgeText}> {room.badge} </Text>
                </View>
                }
            </ListItem>
        )
    }


    componentDidMount() {
        console.log('componentDidMount')
    }

    handlePress(room) {
        this.props.handlePress(room.watch_id)
    }
    handleLongPress(room) {
        this.setState({modalVisible:true, room:room})
    }

modalHeader() {
    return (
        <View style={styles.modalHeader}>
            <Text style={styles.title}> {this.state.room.watch_name} </Text>
            <View style={styles.divider} />
        </View>
    )
}

onButtonPress() {
    console.log('onButtonPress')
}

onButtonPressDelete() {
    const rooms = this.props.rooms.filter(room =>room !== this.state.room)
    const dataProvider = this.state.dataProvider.cloneWithRows(rooms)

    this.props.handleDelete(this.state.room)
    this.setState({dataProvider, modalVisible:false});
}

onButtonPressClose() {
    this.setState({modalVisible:false});
}

modalBody() {
    return (
        <View style={styles.modalBody}>
            <TouchableOpacity onPress={this.onButtonPressDelete}>
                <Text style={styles.detail}>Delete</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={this.onButtonPressClose}>
                <Text style={styles.detail}>Close</Text>
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

    render() {

        const { rooms } = this.props
        const avatar_url =  'https://s3.amazonaws.com/uifaces/faces/twitter/ladylexy/128.jpg'

        console.log('render')
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
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  container2: {
    justifyContent: "space-around",
    alignItems: 'flex-start',
    flex: 1,
    backgroundColor: '#fff',
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
  modalBody:{
    backgroundColor:"#fff",
    paddingVertical:20,
    paddingHorizontal:10,
  },
  actions:{
    borderRadius:5,
    marginHorizontal:10,
    paddingVertical:10,
    paddingHorizontal:20
  },
  actionText:{
    color:"#fff"
  },
  button: {
    backgroundColor:"#fff",
  },
  flexRow: {
    flex:1,
    flexDirection: 'row',
  },
 badgeCycle: {
        position: 'absolute',
        right: -8,
        top: -8,
        backgroundColor: 'red',
        borderRadius: 6,
        width: 12,
        height: 13,
        justifyContent: 'center',
        alignItems: 'center',
    },
    badgeText: {
        color: 'white',
        fontSize: 10,
        fontWeight: 'bold',
    }

});
export default ChatRoomComponent;

