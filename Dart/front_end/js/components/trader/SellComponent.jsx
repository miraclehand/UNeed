import React from 'react';
import { StyleSheet, View } from 'react-native';
import OrderComponent from './OrderComponent';
import LeftComponent from './LeftComponent';

const left_columns =
[
    "종목코드",
    "종목명",
    "수량",
    "단가",
    "현재가",
    "평가금액",
    "손익금액",
    "수익률",
]

class SellComponent extends React.Component {
    constructor(props) {
        super(props);

        this.handlePress  = this.handlePress.bind(this)
        this.handleQuery  = this.handleQuery.bind(this)
        this.handleSelect = this.handleSelect.bind(this)
        this.handleSell   = this.handleSell.bind(this)

        this.state = {
            pos: [],
            code: '',
            name: '',
            qty: '',
            price: '',
        }
    }

    handlePress(order) {
        this.setState({order:order})
    }

    handleQuery() {
        const { email, token } = this.props

        this.props.requestBalance(email, token)
    }

    handleSell(code, qty, price, ordno) {
        this.props.requestSell(code, qty, price)
    }

    componentDidUpdate(prevProps) {
        const { position } = this.props

        if (prevProps.position === position) {
            return
        }
        const pos = position.map((item, index) => {
            return ([
                item.code,
                item.name,
                item.qty,
                item.org_uv,
                item.curr,
                item.est_amt,
                item.profit,
            ])
        })
        this.setState({ pos: pos })
    }

    handleSelect(row) {
        this.setState({code:row[0], name:row[1], qty:row[2], price:row[4]})
    }

    render() {
        return (
            <View style={styles.container} >
                <View style={{width: '55%', height: '100%' }}>
                    <LeftComponent
                        columns = {left_columns}
                        rows = {this.state.pos}
                        handleQuery = {this.handleQuery}
                        handleSelect = {this.handleSelect}
                    />
                </View>
                <View style={{width: '45%', height: '100%'}}>
                    <OrderComponent
                        {...this.props}
                        handleOrder = {this.handleSell}
                        requestCompany = {this.props.requestCompany}
                        order='매도'
                        code={this.state.code}
                        name={this.state.name}
                        qty={this.state.qty}
                        price={this.state.price}
                    />
                </View>
            </View>
        )
    }
}


const styles = StyleSheet.create({
    container: {
        flex: 1,
  /*      backgroundColor: '#6495ed', */
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'row',
    },
});
export default SellComponent;

