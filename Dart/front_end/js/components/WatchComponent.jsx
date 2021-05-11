import React from 'react';
import { StyleSheet, Button, Dimensions } from 'react-native'
import { RecyclerListView, DataProvider,LayoutProvider } from 'recyclerlistview'
import Constants from 'expo-constants';
import {TouchableOpacity, Text, TouchableHighlight, View, Alert } from 'react-native';
import { ListItem } from 'react-native-elements'

let Modal;

const SCREEN_WIDTH = Dimensions.get("window").width;
const SCREEN_HEIGHT = Dimensions.get("window").height;

class WatchComponent extends React.Component {
    constructor(props) {
        super(props);

        this.handlePress = this.handlePress.bind(this)
        this.handleLongPress = this.handleLongPress.bind(this)
        this.onButtonPress = this.onButtonPress.bind(this)
        this.onButtonPressDelete = this.onButtonPressDelete.bind(this)
        this.onButtonPressGoChat = this.onButtonPressGoChat.bind(this)
        this.onButtonPressClose  = this.onButtonPressClose.bind(this)
        this._rowRenderer = this._rowRenderer.bind(this);

        this.modalHeader = this.modalHeader.bind(this)
        this.modalBody   = this.modalBody.bind(this)
        this.modalContainer= this.modalContainer.bind(this)
        this.modal = this.modal.bind(this)
        this.onLayout = this.onLayout.bind(this)

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
        const dataProvider = new DataProvider((r1, r2) => { return r1 !== r2; })

        this.state = {
            modalVisible: false,
            dataProvider: dataProvider.cloneWithRows(this.props.watchs),
            dimensions: undefined,
        }
    }

    onLayout(event) {
        if (this.state.dimensions) return // layout was already called
        let {width, height} = event.nativeEvent.layout
        //console.log(width, height)
        this.setState({dimensions: {width, height}})
    }

    componentDidUpdate(prevProps) {
        const { watchs } = this.props

        if (prevProps.watchs === watchs) {
            return
        }
        const dataProvider = this.state.dataProvider.cloneWithRows(watchs)
        this.setState({ dataProvider })
    }

    _rowRenderer(type, watch, index, extendedState) {
        const title = watch.name
        const subtitle = watch.std_disc.report_nm +' [' + watch.stock_names +']'
        //console.log(this.list_item)

        return (
            <ListItem
                key={index}
                bottomDivider
                style = {{ flex : 1 }}
                onPress = {() => this.handlePress(watch)}
                onLongPress = {() => this.handleLongPress(watch)}
                onLayout={this.onLayout}
            >
                <ListItem.Content>
                    <ListItem.Title> {title} </ListItem.Title>
                    <ListItem.Subtitle> {subtitle} </ListItem.Subtitle>
                </ListItem.Content>
            </ListItem>
        )
    /*
        const avatar_url =  'https://s3.amazonaws.com/uifaces/faces/twitter/ladylexy/128.jpg'

        return (
            <ListItem
                key={index}
                leftAvatar={{ source: { uri: avatar_url } }}
                title={watch.name}
                subtitle={watch.std_disc.report_nm+' ['+watch.stock_names+']'}
                bottomDivider
                onPress = {this.handlePress}
                onLongPress = {() => this.handleLongPress(watch)}
            />
        )
        */
    }

    componentDidMount() {
    }

    handlePress(watch) {
        console.log('handlePress2', watch)
    }
    handleLongPress(watch) {
        this.setState({modalVisible:true, watch:watch})
    }

modalHeader() {
    return (
        <View style={styles.modalHeader}>
            <Text style={styles.title}> {this.state.watch.name} </Text>
            <View style={styles.divider} />
        </View>
    )
}

onButtonPress() {
    console.log('onButtonPress')
}

onButtonPressGoChat() {
    const watch_id = this.state.watch.id
    const { rooms, navigation } = this.props

    const room = rooms.filter(room => room.watch_id === watch_id)
    console.log(room,watch_id)

    if (room.length > 0) {
        navigation.current.navigate('Chat', { 'watch_id': watch_id })
    } else {
        navigation.current.navigate('ChatRoom', {})
    }
    this.setState({modalVisible:false});
}

onButtonPressDelete() {
    const watchs = this.props.watchs.filter(watch =>watch !== this.state.watch)
    const dataProvider = this.state.dataProvider.cloneWithRows(watchs)

    this.props.handleDelete(this.state.watch)
    this.setState({dataProvider, modalVisible:false});
}

onButtonPressClose() {
    this.setState({modalVisible:false});
}
modalBody() {
    return (
        <View style={styles.modalBody}>
            <TouchableOpacity onPress={this.onButtonPressGoChat}>
                <Text style={styles.detail}>Go Chat</Text>
            </TouchableOpacity>
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
/*
    console.log(this.state.modalVisible)
 return (
    <View style={styles.container}>
      
      {this.modal()}

      <TouchableOpacity
        onPress={() => {
          this.setState({modalVisible:true});
        }}>
        <Text>Show Modal</Text>
      </TouchableOpacity>
    </View>
  );

return (
    <View style={{ marginTop: 22 }}>
      <Modal
        animationType="slide"
        transparent={false}
        visible={this.state.modalVisible}
        onRequestClose={() => {
          Alert.alert('Modal has been closed.');
        }}>
        <View style={{ marginTop: 22 }}>
          <View>
            <Text>Hello World!</Text>

            <TouchableHighlight
              onPress={() => {
                this.setState({modalVisible:!this.state.modalVisible})
              }}>
              <Text>Hide Modal</Text>
            </TouchableHighlight>
          </View>
        </View>
      </Modal>

      <TouchableHighlight
        onPress={() => {
          this.setState({modalVisible:true})
        }}>
        <Text>Show Modal</Text>
      </TouchableHighlight>
    </View>
  );

*/


        const { watchs } = this.props
        const avatar_url =  'https://s3.amazonaws.com/uifaces/faces/twitter/ladylexy/128.jpg'

        return (
            <>
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
            </>
        )

        /*
        return (
            <TouchableOpacity
                onPress={() => {
                this.setState({modalVisible:false});
            }}>
                {this.modal()}
                <ScrollView>
                    { watchs.map((w, i) => {
                        if (!w) {
                            return <></>
                        }
                        return (
                          <ListItem
                              key={i}
                              leftAvatar={{ source: { uri: avatar_url } }}
                              title={w.name}
                              subtitle={w.std_disc.report_nm+' ['+w.stock_names+']'}
                              bottomDivider
                              onPress = {this.handlePress}
                              onLongPress = {() => this.handleLongPress(w)}
                          />
                        )
                    })}
                </ScrollView>
            </TouchableOpacity>
        )
        */
    }
    
}

/*
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
  }
});
export default WatchComponent;

