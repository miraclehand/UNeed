import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { setSimula } from '../actions/SimulaAction';
import StatsSimulaComponent from '../components/StatsSimulaComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)
    }
/*
    componentDidMount() {
        let stock_codes = ''
        if (!this.props.simula.stats) {
            return
        }
        this.props.simula.stats.map(stats => {
            if (stock_codes.indexOf(stats.corp.stock_code) > -1) {
                return
            }
            this.props.requestCandle(stats.corp.stock_code)
            stock_codes = stock_codes + ' ' + stats.corp.stock_code
        })
    }

    findLog(candle, rcept_dt, n, ymd, cnt) {
        if (cnt > 15) {
            return 0
        }
        const date = dayjs(rcept_dt).add(n, ymd).format('YYYYMMDD')
        if (date in candle) {
            return candle[date]['log']
        }
        return this.findLog(candle, dayjs(date).add(-1, 'day'), n, ymd, cnt + 1)
    }

    componentWillReceiveProps(nextProps)
    {
        if(this.props.candleState === nextProps.candleState) {
            return
        }

        let simula = this.props.simula
        
        simula.stats.map(stats => {
            if(!(stats.corp.stock_code in nextProps.candleState)) {
                return
            }
            const candle  = nextProps.candleState[stats.corp.stock_code]
            const logBf30 = this.findLog(candle, stats.disc.rcept_dt, -1, 'month', 0)
            const logBf7  = this.findLog(candle, stats.disc.rcept_dt, -7, 'day',   0)
            const logD    = this.findLog(candle, stats.disc.rcept_dt,  0, 'month', 0)
            const logAf7  = this.findLog(candle, stats.disc.rcept_dt,  7, 'day',   0)
            const logAf30 = this.findLog(candle, stats.disc.rcept_dt,  1, 'month', 0)

            stats.prrtBf30 = '-'
            stats.prrtBf7  = '-'
            stats.prrtD    = '-'
            stats.prrtAf7  = '-'
            stats.prrtAf30 = '-'
            if (logBf30 > 0) stats.prrtBf30 = (logD - logBf30)/ logBf30* 100
            if (logBf7  > 0) stats.prrtBf7  = (logD - logBf7) / logBf7 * 100
            if (logD    > 0) stats.prrtAf7  = (logAf7  - logD)/ logD * 100
            if (logD    > 0) stats.prrtAf30 = (logAf30 - logD)/ logD * 100
            
            console.log('###', stats.corp.stock_code, stats.prrtBf30, stats.prrtBf7, stats.prrtD, stats.prrtAf7, stats.prrtAf30)
        })

        const index = 0
        this.props.setSimula(index, simula)
    }
    */

    render() {
        //console.log(this.props.candleState)
        return (
            <StatsSimulaComponent
                simula = {this.props.simula}
                candleState = {this.props.candleState }
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
        candleState: state.candleReducer,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        setSimula: bindActionCreators(setSimula, dispatch),
    };
}

const StatsSimulaContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default StatsSimulaContainer;
