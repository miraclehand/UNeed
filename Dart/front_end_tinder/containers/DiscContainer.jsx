import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestDiscs, requestDiscDetail } from '../actions/DiscAction';
import DiscComponent from '../components/DiscComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)
    }

    componentDidMount() {
        const {username, token, cntry } = this.props

        this.props.requestDiscs(username, token, cntry, '', '');
    }

    render() {
        const { discs } = this.props

        return <DiscComponent discs={discs} />
   }
}

function mapStateToProps (state) {
    return {
        username: state.authReducer.username,
        token: state.authReducer.token,
        cntry: state.baseReducer.cntry,
        discs: state.discReducer.discs,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestDiscs: bindActionCreators(requestDiscs, dispatch),
        requestDiscDetail: bindActionCreators(requestDiscDetail, dispatch),
    };
}

const DiscContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default DiscContainer;

