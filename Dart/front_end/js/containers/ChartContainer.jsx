import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestCandle } from '../actions/CandleAction';
import  ChartComponent  from '../components/ChartComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)
    }

    componentDidMount() {
        const {email, token, cntry } = this.props
        const code  = '005930'
        const date1 = '20190101'
        const date2 = '20300320'

        this.props.requestCandle(email, token, cntry, code, date1, date2);
    }

    render() {
        const { options, ohlcvs } = this.props

        return (
            <ChartComponent 
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
