import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestListStock } from '../actions/ListAction';
import { setUnitName, setUnitStocks } from '../actions/UnitAction';
import CreateUnitComponent from '../components/CreateUnitComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)

        this.handleUnitName   = this.handleUnitName.bind(this)
        this.handleUnitStocks = this.handleUnitStocks.bind(this)
    }

    componentDidMount() {
        if (this.props.list_stock.length === 0) {
            this.props.requestListStock(this.props.cntry);
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
                list_stock={this.props.list_stock}
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
        list_stock: state.listReducer.list_stock,
        unitStocks: state.unitReducer.stocks
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestListStock :bindActionCreators(requestListStock,dispatch),
        setUnitName  : bindActionCreators(setUnitName, dispatch),
        setUnitStocks: bindActionCreators(setUnitStocks, dispatch),

    };
}

const CreateWatchContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default CreateWatchContainer;
