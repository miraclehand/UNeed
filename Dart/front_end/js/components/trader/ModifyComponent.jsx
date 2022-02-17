import React from 'react';
import { StyleSheet, View } from 'react-native';
import OrderComponent from './OrderComponent';
import LeftComponent from './LeftComponent';

const left_columns =
[
    "주문번호",
    "종목코드",
    "종목명",
    "매매구분",
    "주문수량",
    "주문금액",
    "체결수량",
    "체결금액",
]

class ModifyComponent extends React.Component {
    constructor(props) {
        super(props);

        this.handlePress  = this.handlePress.bind(this)
        this.handleQuery  = this.handleQuery.bind(this)
        this.handleSelect = this.handleSelect.bind(this)
        this.handleModify = this.handleModify.bind(this)

        this.state = {
            sel_stock: '',
            value: '',
            code:'',
            name:'',
            qty:'',
            price:'',
            ordno:'',
            orders:{},
        };
    }

    componentDidUpdate(prevProps) {
        const { orders } = this.props

        if (prevProps.orders === orders) {
            return
        }
        const my_orders = orders.map((item, index) => {
            return ([
                item.ordno,
                item.expcode,
                item.expname,
                item.medosu,
                item.qty,
                item.price,
                item.cheqty,
                item.cheprice,
            ])
        })
        this.setState({ orders: my_orders })
    }

    handlePress(order) {
        this.setState({order:order})
    }

    handleQuery() {
        const { email, token } = this.props

        this.props.requestOrders(email, token, '2')
    }

    handleSelect(row) {
        this.setState({code:row[1], name:row[2], qty:row[4], price:row[5], ordno:row[0]})
    }

    handleModify(code, qty, price, ordno) {
        this.props.requestModify(code, qty, price, ordno)
    }

    render() {
        return (
            <View style={styles.container} >
                <View style={{width: '55%', height: '100%' }}>
                    <LeftComponent
                        {...this.props}
                        columns = {left_columns}
                        rows = {this.state.orders}
                        handleQuery = {this.handleQuery}
                        handleSelect = {this.handleSelect}
                    />
                </View>
                <View style={{width: '45%', height: '100%'}}>
                    <OrderComponent
                        {...this.props}
                        {...this.state}
                        handleOrder = {this.handleModify}
                        code={this.state.code}
                        name={this.state.name}
                        qty={this.state.qty}
                        price={this.state.price}
                        ordno={this.state.ordno}
                        order='정정'/>
                </View>
            </View>
        )
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f5deb3',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'row',
    },
});
export default ModifyComponent;

