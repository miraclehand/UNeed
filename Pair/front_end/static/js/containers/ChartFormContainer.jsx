import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestListStock } from '../actions/ListAction';
import { requestChart, clearChart } from '../actions/ChartAction';
import ChartFormComponent from '../components/ChartFormComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    componentDidMount() {
        this.props.requestListStock(this.props.cntry);
    }

    handleSubmit(date1, date2, stock1, stock2) {
        const { username, token, cntry, clearChart, requestChart } = this.props

        clearChart();
        requestChart(username, token, cntry, date1, date2, stock1, stock2);
    }

    render() {
        const { stocks } = this.props
        const { handleSubmit } = this

        return <ChartFormComponent stocks={stocks} handleSubmit={handleSubmit} />
    }
}

function mapStateToProps (state) {
    return {
        stocks: state.stockReducer.stocks,
        username: state.authReducer.username,
        token: state.authReducer.token,
        cntry: state.baseReducer.cntry,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestListStock: bindActionCreators(requestListStock, dispatch),
        requestChart: bindActionCreators(requestChart, dispatch),
        clearChart: bindActionCreators(clearChart, dispatch),
    };
}

const ChartFormContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default ChartFormContainer;

