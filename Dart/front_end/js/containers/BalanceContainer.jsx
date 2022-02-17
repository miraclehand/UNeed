import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import BalanceComponent from '../components/BalanceComponent';
import { requestBalance } from '../actions/HTSAction';

export class Connected extends React.Component {
    constructor(props) {
        super(props)

        this.handlePress = this.handlePress.bind(this)
    }

    componentDidMount() {
    }

    handlePress() {
        const { email, token } = this.props
        this.props.requestBalance(email, token)
    }

    render() {
        return (
            <BalanceComponent
                est_acc = {this.props.est_acc}
                position = {this.props.position}
                handlePress = {this.handlePress}
            />
        )
   }
}

function mapStateToProps (state) {
    return {
        email: state.userReducer.email,
        token: state.userReducer.token,
        est_acc: state.balanceReducer.est_acc,
        position: state.balanceReducer.position,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestBalance:bindActionCreators(requestBalance, dispatch),
    };
}

const BalanceContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default BalanceContainer;
