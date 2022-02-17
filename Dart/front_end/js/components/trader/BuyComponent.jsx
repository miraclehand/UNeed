import React from 'react';
import { StyleSheet, View } from 'react-native';
import OrderComponent from './OrderComponent';
import LeftComponent from './LeftComponent';

const left_columns =
[
    "종목명",
    "현재가",
    "추정EPS",
    "추정PER",
    "배당수익률",
    "투자의견",
    "PER",
]

class BuyComponent extends React.Component {
    constructor(props) {
        super(props);

        this.handleBuy = this.handleBuy.bind(this)
        this.handleQuery = this.handleQuery.bind(this)

        this.state = {
            code:'',
            name:'',
            qty:'',
            price:'',
            left_company:[],
        };
    }

   componentDidUpdate(prevProps) {
        const { company } = this.props

        if (prevProps.company === company) {
            return
        }
        const left_company = [
            company.name,
            company.close,
            company.cns_eps,
            company.cns_per,
            company.dividend,
            company.invt_opinion,
            company.per,
        ]
        this.setState({ left_company, price:company.close })
    }

    handleQuery() {
        this.props.requestCompany(this.state.code)
    }

    handleBuy(code, qty, price, ordno) {
        this.props.requestBuy(code, qty, price)
    }

    render() {
        return (
            <View style={styles.container} >
                <View style={{width: '55%', height: '100%' }}>
                    <LeftComponent
                        columns = {left_columns}
                        rows = {[this.state.left_company]}
                        handleQuery = {this.handleQuery}
                    />
                </View>
                <View style={{width: '45%', height: '100%'}}>
                    <OrderComponent
                        {...this.props}
                        {...this.state}
                        handleOrder = {this.handleBuy}
                        code={this.state.code}
                        name={this.state.name}
                        qty={this.state.qty}
                        price={this.state.price}
                        order='매수'
                    />
                </View>
            </View>
        )
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    /*    backgroundColor: '#dc143c', */
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'row',
    },
});
export default BuyComponent;

