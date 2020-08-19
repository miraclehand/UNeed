import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestListStock } from '../actions/ListAction';
import { setUnitName, setUnitStocks, setUnitSDate, setUnitEDate } from '../actions/UnitAction';
import CreateUnitComponent from '../components/CreateUnitComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)

        this.handleUnitName   = this.handleUnitName.bind(this)
        this.handleUnitStocks = this.handleUnitStocks.bind(this)
        this.handleUnitSDate  = this.handleUnitSDate.bind(this)
        this.handleUnitEDate  = this.handleUnitEDate.bind(this)
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

    handleUnitSDate(s_date) {
        this.props.setUnitSDate(s_date)
    }

    handleUnitEDate(e_date) {
        this.props.setUnitEDate(e_date)
    }

    render() {
        return (
            <CreateUnitComponent
                simula
                list_stock   = {this.props.list_stock}
                unitSDate    = {this.props.unitSDate}
                unitEDate    = {this.props.unitEDate}
                unitStocks   = {this.props.unitStocks}
                handleUnitName   = {this.handleUnitName}
                handleUnitStocks = {this.handleUnitStocks}
                handleUnitSDate  = {this.handleUnitSDate}
                handleUnitEDate  = {this.handleUnitEDate}
            />
        )
   }
}

function mapStateToProps (state) {
    return {
        email: state.userReducer.email,
        authState: state.userReducer.authState,
        pushToken: state.userReducer.pushToken,
        os: state.baseReducer.os,
        db: state.dbReducer.db,
        dbName: state.dbReducer.dbName,
        cntry: state.baseReducer.cntry,
        list_stock: state.listReducer.list_stock,
        simulaStocks: state.simulaReducer.simula.stocks,
        simulas: state.simulaReducer.simulas,
        unitStocks: state.unitReducer.stocks,
        unitSDate: state.unitReducer.s_date,
        unitEDate: state.unitReducer.e_date,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestListStock: bindActionCreators(requestListStock, dispatch),
        setUnitName  : bindActionCreators(setUnitName, dispatch),
        setUnitStocks: bindActionCreators(setUnitStocks, dispatch),
        setUnitSDate : bindActionCreators(setUnitSDate, dispatch),
        setUnitEDate : bindActionCreators(setUnitEDate, dispatch),
    };
}

const CreateSimulaContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default CreateSimulaContainer;
