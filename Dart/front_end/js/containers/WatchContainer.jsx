import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestWatch, requestDeleteWatch } from '../actions/WatchAction';
import WatchComponent from '../components/WatchComponent';
import { Text, Button } from 'react-native';
import { signOutAsync, getCachedUserAsync } from '../init/InitUser';
import { setUser } from '../actions/UserAction';
import { requestCandle } from '../actions/CandleAction';

export class Connected extends React.Component {
    constructor(props) {
        super(props)

        this.handlePress  = this.handlePress.bind(this)
        this.handleDelete = this.handleDelete.bind(this)
    }

    componentDidMount() {
        const {os, db, dbName, email, token, cntry } = this.props

        //this.props.requestWatch(os, db, email, token, cntry);
        this.props.requestWatch(os, db, email, token, cntry);
        //this.props.requestCandle('005930')
        //this.props.requestCandle('000660')
    }

    handlePress() {
        (async () => {
            await signOutAsync(this.props.authState);
            const user = await getCachedUserAsync()
            this.props.setUser(user);
        }
        )()
    }

    handleDelete(watch) {
        const {os, db, dbName, email, token, cntry } = this.props

        this.props.requestDeleteWatch(os, db, email, token, cntry, watch);
    }

    render() {
        const { os, watchs } = this.props

        return (
            <>
                <WatchComponent os={os} watchs={watchs} handleDelete={this.handleDelete} />
                <Button title='SignOut' onPress={this.handlePress} />
            </>
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
        watchs: state.watchReducer.watchs,
        candleState: state.candleReducer,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        setUser      : bindActionCreators(setUser, dispatch),
        requestWatch : bindActionCreators(requestWatch,  dispatch),
        requestDeleteWatch: bindActionCreators(requestDeleteWatch, dispatch),
        requestCandle: bindActionCreators(requestCandle, dispatch),
    };
}

const WatchContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default WatchContainer;
