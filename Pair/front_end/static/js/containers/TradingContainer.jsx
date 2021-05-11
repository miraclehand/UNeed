import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestTick } from '../actions/TickAction';
import { requestListStock } from '../actions/ListAction';
import { requestEntries, requestOpenEntry, requestCloseEntry } from '../actions/TradingAction';
import TradingComponent from '../components/TradingComponent'

class Connected extends React.Component {
    constructor(props) {
        super(props)

        this.handleOpenEntry  = this.handleOpenEntry.bind(this)
        this.handleCloseEntry = this.handleCloseEntry.bind(this)
        this.timerTick = this.timerTick.bind(this)
    }
    
    handleOpenEntry(basket1, basket2) {
        const { username, token, cntry } = this.props

        this.props.requestOpenEntry(username, token, cntry, basket1, basket2)
    }

    handleCloseEntry(cntry, entry_id) {
        const { username, token } = this.props

        this.props.requestCloseEntry(username, token, cntry, entry_id)
    }

    timerTick() {
        const { entries, requestTick } = this.props

        if (entries && entries.length > 0) {
            entries.map(entry => {
                requestTick(entry.cntry1, entry.code1);
                requestTick(entry.cntry2, entry.code2);
            })
        }
    }
    
    componentDidMount() {
        const { username, token, cntry, stocks } = this.props
        const { requestListStock, requestEntries } = this.props

        if (stocks.length == 0) {
            requestListStock(cntry)
        }

        requestEntries(username, token, 'all')

        this.interval = setInterval(() => {
            this.timerTick()
        }, 3000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    render () {
        const { level, stocks, ticks, budget, entries } = this.props
        const { handleOpenEntry, handleCloseEntry } = this

        if (entries && entries.length > 0 && Object.keys(ticks).length == 0) {
            this.timerTick()
        }

        return <TradingComponent
                   level={level}
                   stocks={stocks}
                   ticks={ticks}
                   budget={budget}
                   entries={entries}
                   handleOpenEntry={handleOpenEntry}
                   handleCloseEntry={handleCloseEntry}
               />
    }
};

function mapStateToProps (state) {
    return {
        cntry: state.baseReducer.cntry,
        username: state.authReducer.username,
        token: state.authReducer.token,
        level: state.authReducer.level,
        ticks: state.tickReducer.ticks,
        stocks: state.stockReducer.stocks,
        budget: state.assetReducer.budget,
        entries: state.tradingReducer.entries,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestListStock: bindActionCreators(requestListStock, dispatch),
        requestTick: bindActionCreators(requestTick, dispatch),
        requestEntries: bindActionCreators(requestEntries, dispatch),
        requestOpenEntry: bindActionCreators(requestOpenEntry, dispatch),
        requestCloseEntry: bindActionCreators(requestCloseEntry, dispatch),
    };
}

const TradingContainer = connect(mapStateToProps,mapDispatchToProps)(Connected);

export default TradingContainer;
