import React, { Component } from "react";
import {StyleSheet, Text, View, Dimensions, TouchableHighlight, TouchableOpacity} from 'react-native';
import TextAvatar from 'react-native-text-avatar';

import * as WebBrowser from 'expo-web-browser';

const SCREEN_WIDTH = Dimensions.get("window").width;

class BubbleComponent extends React.Component {
    constructor(args) {
        super(args);
        this.handleStockLink = this.handleStockLink.bind(this)
        this.handleDiscLink = this.handleDiscLink.bind(this)
    }

    handleStockLink(stock_code) {
        const url = 'http://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A' + stock_code + '&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=&strResearchYN='

        WebBrowser.openBrowserAsync(url)
    }

    handleDiscLink(url) {
        WebBrowser.openBrowserAsync(url)
    }

    render() {
        return (
            <View style={styles.container}>
                <View style={styles.flexRow} >
                    <TouchableOpacity onPress={() => this.handleStockLink(this.props.chat.stock_code)}>
                        <TextAvatar
                            backgroundColor={'#ffff00'}
                            textColor={'#0000ff'}
                            size={60}
                            type={'circle'} // optional
                        >
                            {this.props.chat.corp_name}
                        </TextAvatar>
                    </TouchableOpacity>
                    <View style = {styles.flexColumn} >
                        <TouchableOpacity onPress={() => this.handleStockLink(this.props.chat.stock_code)}>
                            <Text style= {styles.wrap}>
                                [{this.props.chat.corp_name}]
                            </Text>
                        </TouchableOpacity>
                        <TouchableOpacity onPress={() => this.handleDiscLink(this.props.chat.url)}>
                            <Text style= {styles.wrap}>
                                {this.props.chat.report_nm}
                            </Text>
                        </TouchableOpacity>
                        <View style={styles.talkBubble}>
                            <View style={styles.talkBubbleSquare}>
                                <Text> {this.props.chat.content} </Text>
                            </View>
                            <View style={styles.talkBubbleTriangle} />
                            <Text style= {styles.wrap}>
                                {this.props.chat.rcept_dt} {this.props.chat.reg_time}
                            </Text>
                        </View>
                    </View>
                </View>
            </View>
        )
        return (
            <View style={styles.container}>
                <View style={styles.flexRow} >
                    <TextAvatar
                        backgroundColor={'#ffff00'}
                        textColor={'#0000ff'}
                        size={60}
                        type={'circle'} // optional
                    >
                        {this.props.chat.corp_name}
                    </TextAvatar>
                    <View style = {styles.flexColumn} >
                        <TouchableOpacity onPress={() => this.handleStockLink(this.props.chat.stock_code)}>
                            <Text style= {styles.wrap}>
                                [{this.props.chat.corp_name}]
                            </Text>
                        </TouchableOpacity>
                        <TouchableOpacity onPress={() => this.handleDiscLink(this.props.chat.url)}>
                            <Text style= {styles.wrap}>
                                {this.props.chat.report_nm}
                            </Text>
                        </TouchableOpacity>
                        <View style={styles.talkBubble}>
                            <View style={styles.talkBubbleSquare}>
                                <Text> {this.props.chat.content} </Text>
                            </View>
                            <View style={styles.talkBubbleTriangle} />
                            <Text style= {styles.wrap}>
                                {this.props.chat.rcept_dt} {this.props.chat.reg_time}
                            </Text>
                        </View>
                    </View>
                </View>
            </View>
        )
        /* return <View {...this.props} > */
        return (
            <View style={styles.container}>
                <View style={styles.flexRow} >
                    <TextAvatar
                        backgroundColor={'#ffff00'}
                        textColor={'#0000ff'}
                        size={60}
                        type={'circle'} // optional
                    >
                        {this.props.data.user.name}
                    </TextAvatar>
                    <View style={styles.talkBubble}>
                        <Text>
                            {this.props.data.user.name} 
                            {this.props.data.tick}원 
                            {this.props.data.reg_time}
                        </Text>
                        <View style={styles.talkBubbleSquare}>
                            <Text>Cell Id: [{this.props.data._id} ]
                                    {this.props.data.text}
                                    {this.props.data.content}
                                    {this.props.data.tick}
                                    {this.props.data.reg_time}
                                    {this.props.data.text}
                                    {this.props.data.text}
                                    {this.props.data.text}
                                    {this.props.data.text}
                                    {this.props.data.text}
                                    {this.props.data.text}
                                    {this.props.data.text}
                                    {this.props.data.text}
                                    {this.props.data.text}
                                    {this.props.data.text}
                                    {this.props.data.text}
                                    {this.props.data.text}
                                    {this.props.data.text}
                                    {this.props.data.text}
                                    {this.props.data.text}
                                    {this.props.data.text}
                            </Text>
                        </View>
                        <View style={styles.talkBubbleTriangle} />
                    </View>
                </View>
            </View>
        )
    }
}

const styles = {
    container: {
        justifyContent: "space-around",
        alignItems: 'flex-start',
        flex: 1,
        backgroundColor: 'transparent',
        transform: [ {scaleY :-1}, ],
        marginTop: 10,
        marginBottom: 10,
        marginLeft: 10,
        marginRight: 10,
        minWidth: SCREEN_WIDTH - (50),
        maxWidth: SCREEN_WIDTH - (50),
    },
    text: {
        color: '#2175FF'
    },
    toggleButton: {
        width: 100,
        height: 100,
        borderRadius: 50,
        margin: 10,
        justifyContent: 'space-around',
        alignItems: 'center',
        backgroundColor: '#2175FF',
        alignSelf: 'center'
    },
    textContainer: {
        flexDirection: 'column',
        justifyContent: 'space-around',
        height: 100,
        paddingLeft: 25,
        paddingRight: 25,
        borderRadius: 10,
        borderColor: '#FFFFFF',
        borderWidth: 5,
        backgroundColor: '#F0F0F0',
    },
    indicatorText: {
        textAlign: 'center',
        marginTop: 100
    },
    listItem: {
        flexDirection: 'row',
        margin: 10,
    },
    body: {
        marginLeft: 10,
        marginRight: 10,
        maxWidth: SCREEN_WIDTH - (80 + 10 + 20),
    },
    flexRow: {
        flex:1,
        flexDirection: 'row',
    },
    flexColumn: {
        flex:1,
        flexDirection: 'column',
    },
    flexBottom: {
        flex:1,
        flexDirection: 'column-reverse',
        backgroundColor: '#2175FF',
    },
talkBubble: {
    backgroundColor: 'transparent',
    marginLeft: 30,
  },
  talkBubbleSquare: {
    flex:1,
    backgroundColor: "lightblue",
    borderRadius: 10,
    flexDirection: 'column-reverse',
    paddingTop: 10,
    paddingLeft: 10,
    paddingRight: 10,
    paddingBottom: 10,
  },
  talkBubbleTriangle: {
    position: 'absolute',
    left: -26,
    top: 7,
    width: 0,
    height: 0,
    borderTopColor: 'transparent',
    borderTopWidth: 13,
    borderRightWidth: 26,
    borderRightColor: "lightblue",
    borderBottomWidth: 13,
    borderBottomColor: 'transparent'
  },

};

export default BubbleComponent;

