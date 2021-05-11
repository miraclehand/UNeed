import React from 'react';
import { Platform } from "react-native";
import { SafeAreaView, ScrollView, StyleSheet, Button, Dimensions } from 'react-native'
import { RecyclerListView, DataProvider, LayoutProvider } from "recyclerlistview";
import Constants from 'expo-constants';
import {TouchableOpacity, Text, TouchableHighlight, View, Alert } from 'react-native';
import { ListItem } from 'react-native-elements'
let Modal;

const SCREEN_WIDTH = Dimensions.get("window").width;

class WatchComponent extends React.Component {
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

        this._layoutProvider = new LayoutProvider(
            index => {
                return 0;
            },
            (type, dim) => {
                dim.width = SCREEN_WIDTH;
                dim.height = 73;
            }
        );
        const dataProvider = new DataProvider((r1, r2) => { return r1 !== r2; })

        this.state = {
            modalVisible: false,
            dataProvider: dataProvider.cloneWithRows(this.props.watchs),
        }
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
    }

    componentDidMount() {
    }

    handlePress() {
        console.log('handlePress2')
    }
    handleLongPress(watch) {
        this.setState({modalVisible:true, watch:watch})
    }
    onButtonPressDelete() {
    /*
        this.props.handleDeleteWatch()
        */
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

onButtonPressDelete() {
    const watchs = this.props.watchs.filter(watch =>watch !== this.state.watch)
    const dataProvider = this.state.dataProvider.cloneWithRows(watchs)

    this.props.handleDelete(this.state.watch)
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
                <TouchableOpacity
                    style={{ flex:1 }}
                    onPress={() => {
                    this.setState({modalVisible:false});
                }}>
                    {this.modal()}
                    <RecyclerListView
                        layoutProvider={this._layoutProvider}
                        dataProvider={this.state.dataProvider}
                        rowRenderer={this._rowRenderer}
                        extendedState={this.state.extendedState}
                        style={{ flex:1 }}
                    />
                </TouchableOpacity>
            </>
        )

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
  }
});
export default WatchComponent;

