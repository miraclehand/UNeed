import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestCandle } from '../actions/CandleAction';
import  CandleChartComponent  from '../components/CandleChartComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)
    }

    componentDidMount() {
        const {stock_code, email, token, cntry } = this.props
        const date1 = '20190101'
        const date2 = '20300320'

        this.props.requestCandle(email, token, cntry, stock_code, date1, date2);
    }

    render() {
        const { options, ohlcvs } = this.props
        console.log('CandleChartContainer2' )

        return (
            <CandleChartComponent
                options={options}
                ohlcvs={ohlcvs}
                handlePress={this.handlePress}
            />
        )
   }
}

function mapStateToProps (state) {
    return {
        email: state.userReducer.email,
        cntry: state.baseReducer.cntry,
        options: state.candleReducer.options,
        ohlcvs: state.candleReducer.ohlcvs,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestCandle : bindActionCreators(requestCandle,  dispatch),
    };
}

const ChartContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default ChartContainer;
