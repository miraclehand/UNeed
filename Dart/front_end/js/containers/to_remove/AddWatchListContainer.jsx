import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestPostWatch } from '../actions/WatchAction';
import { requestListStock, requestListDisc } from '../actions/ListAction';
import AddWatchListComponent from '../components/AddWatchListComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)

        this.handleAddWatch = this.handleAddWatch.bind(this)
    }

    handleAddWatch(watch) {
        let exists = 0
        const {os, db, email, token, cntry, watchs } = this.props

        watchs && watchs.map((value, i) => {
            if (value.keyword == keyword) {
                exists = exists + 1
            }
        })
        if (exists > 0) {
            alert('이미 등록된 관심목록 입니다.')
            return;
        }

        this.props.requestPostWatch(os, db, email, token, cntry, keyword)
        alert('관심목록이 등록되었습니다.')
    }

    componentDidMount() {
        const {os, db, email, token, cntry } = this.props

        if (this.props.stocks.length === 0) {
            this.props.requestStockList(os, db, email, token, cntry)
        }
    }

    render() {
        return (
            <AddWatchListComponent 
                watchs={this.props.watchs}
                stocks={this.props.stocks}
                handleAddWatch={this.handleAddWatch}
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
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestPostWatch :bindActionCreators(requestPostWatch,dispatch),
        requestListStock :bindActionCreators(requestListStock,dispatch),
    };
}

const AddWatchListContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default AddWatchListContainer;
