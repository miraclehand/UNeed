import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestStocks } from '../actions/ServerPoolAction';
import { setUnitName, setUnitStocks } from '../actions/UnitAction';
import CreateUnitComponent from '../components/CreateUnitComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)

        this.handleUnitName   = this.handleUnitName.bind(this)
        this.handleUnitStocks = this.handleUnitStocks.bind(this)
    }

    componentDidMount() {
        const { os, db, email, token, cntry } = this.props
        const { server_updated, updated, updated_db } = this.props

        if (this.props.stocks.length === 0) {
            this.props.requestStocks(os, db, cntry)
        }
    }

    handleUnitName(name) {
        this.props.setUnitName(name)
    }

    handleUnitStocks(stocks) {
        this.props.setUnitStocks(stocks)
    }

    render() {
        return (
            <CreateUnitComponent 
                watch
                stocks={this.props.stocks}
                unitStocks={this.props.unitStocks}
                handleUnitName   = {this.handleUnitName}
                handleUnitStocks = {this.handleUnitStocks}
            />
        )
   }
}

function mapStateToProps (state) {
    return {
        email: state.userReducer.email,
        cntry: state.baseReducer.cntry,
        os: state.baseReducer.os,
        db: state.dbReducer.db,
        stocks: state.dbReducer.stocks,
        unitStocks: state.unitReducer.stocks
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestStocks:bindActionCreators(requestStocks,dispatch),
        setUnitName  : bindActionCreators(setUnitName, dispatch),
        setUnitStocks: bindActionCreators(setUnitStocks, dispatch),

    };
}

const CreateWatchContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default CreateWatchContainer;
