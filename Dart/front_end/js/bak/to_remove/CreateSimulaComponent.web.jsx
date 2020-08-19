import React from 'react';
import { Text, TextInput, Platform, StyleSheet, View, Dimensions } from 'react-native';
import * as Font from 'expo-font';
import { Button } from 'react-native-elements'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import SearchStockComponent from './SearchStockComponent'

export default class CreateSimulaComponent extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            value1: new Date(),
            value2: new Date(),
        };
    }

    showDatePicker() {
        this.setState({isDatePickerVisible:true})
    }

    hideDatePicker() {
        this.setState({isDatePickerVisible:false})
    }

    handleConfirm(date) {
        console.warn("A date has been picked: ", date);
        this.hideDatePicker();
    };

    render() {
        return (
            <>
                <TextInput
                    style={styles.input}
                    placeholder='Type Simula Name'
                    underlineColorAndroid='transparent'
                    autoCapitalize='none'
                    onChangeText={this.props.handleSimulaName}
                />
                <DatePicker
                    dateFormat='yyyy/MM/dd'
                    selected={this.state.value1}
                    onChange={this.handleSimulaSDate }
                />
                <DatePicker
                    dateFormat='yyyy/MM/dd'
                    selected={this.state.value2}
                    onChange={this.handleSimulaEDate }
                />
                <SearchStockComponent
                    list_stock     = {this.props.list_stock}
                    selectedStocks = {this.props.simulaStocks}
                    handleSelectStocks = {this.props.handleSimulaStocks}
                />
            </>
        )
        /*
            시뮬레이션명
            기간
            회사명
            공시
            기재정정미포함
        */
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#f5fcff"
    },
    input: {
        margin: 15,
        height: 40,
        borderColor: "#7a42f4",
        borderWidth: 1
    },
});
