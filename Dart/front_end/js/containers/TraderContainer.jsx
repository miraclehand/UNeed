import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import TraderComponent from '../components/TraderComponent';
import { requestOrders, requestBuy, requestSell, requestModify, requestCancel, requestBalance } from '../actions/HTSAction';
import { requestStocks } from '../actions/ServerPoolAction';
import { requestCompany } from '../actions/CompanyAction';


export class Connected extends React.Component {
    constructor(props) {
        super(props)
        this.requestCompany = this.requestCompany.bind(this)
    }

    componentDidMount() {
        const { os, db, email, token, cntry, stocks } = this.props

        if (stocks.length === 0) {
            this.props.requestStocks(os, db, cntry)
        }
    }

    requestCompany(code) {
        const { email, token, cntry } = this.props
        if (code === '') {
            return
        }
        this.props.requestCompany(email, token, cntry, code)
    }

    render() {
        return (
            <TraderComponent
                email    = {this.props.email}
                token    = {this.props.token}
                stocks   = {this.props.stocks}
                company  = {this.props.company}
                orders   = {this.props.orders}
                position = {this.props.position}
                requestCompany  = {this.requestCompany}
                requestOrders   = {this.props.requestOrders}
                requestBuy  = {this.props.requestBuy}
                requestSell = {this.props.requestSell}
                requestModify = {this.props.requestModify}
                requestCancel = {this.props.requestCancel}
                requestBalance = {this.props.requestBalance}
            />
        )
   }
}

function mapStateToProps (state) {
    return {
        os: state.baseReducer.os,
        db: state.dbReducer.db,
        cntry: state.baseReducer.cntry,
        email: state.userReducer.email,
        token: state.userReducer.token,
        est_acc: state.balanceReducer.est_acc,
        position: state.balanceReducer.position,
        stocks: state.dbReducer.stocks,
        company: state.companyReducer.company,
        orders: state.ordersReducer.orders,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestOrders:bindActionCreators(requestOrders, dispatch),
        requestBuy:bindActionCreators(requestBuy, dispatch),
        requestSell:bindActionCreators(requestSell, dispatch),
        requestModify:bindActionCreators(requestModify, dispatch),
        requestCancel:bindActionCreators(requestCancel, dispatch),
        requestStocks:bindActionCreators(requestStocks, dispatch),
        requestCompany:bindActionCreators(requestCompany, dispatch),
        requestBalance:bindActionCreators(requestBalance, dispatch),
    };
}

const TraderContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default TraderContainer;
