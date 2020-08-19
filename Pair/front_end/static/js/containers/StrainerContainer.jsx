import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestPostStrainer, requestDeleteStrainer } from '../actions/StrainerAction';
import StrainerComponent from '../components/StrainerComponent'

class Connected extends React.Component {
    constructor(props) {
        super(props)

        this.handleSaveStrainer   = this.handleSaveStrainer.bind(this)
        this.handleDeleteStrainer = this.handleDeleteStrainer.bind(this)
    }

    handleSaveStrainer(strainer) {
        const { username, token, cntry } = this.props
        this.props.requestPostStrainer(username, token, cntry, strainer)
    }

    handleDeleteStrainer(strainer) {
        const { username, token, cntry } = this.props
        this.props.requestDeleteStrainer(username, token, cntry, strainer)
    }

    render () {
        const { handleSaveStrainer, handleDeleteStrainer } = this

        return (
        <>
            <StrainerComponent
                handleSaveStrainer={handleSaveStrainer}
                handleDeleteStrainer={handleDeleteStrainer}
                handleComponent={this.props.handleComponent}
            />
        </>
        )
    }
};

function mapStateToProps (state) {
    return {
        username: state.authReducer.username,
        token: state.authReducer.token,
        cntry: state.baseReducer.cntry,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestPostStrainer: bindActionCreators(requestPostStrainer, dispatch),
        requestDeleteStrainer: bindActionCreators(requestDeleteStrainer, dispatch),
    };
}

const StrainerContainer = connect(mapStateToProps,mapDispatchToProps)(Connected);

export default StrainerContainer;
