import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { NavLink } from 'react-router-dom';
import Button from '@material-ui/core/Button';
import { requestListStock } from "../actions/ListAction";
import { signout } from "../actions/AuthAction";
import { changeCntry } from "../actions/BaseAction";
import { checkManager } from '../functions/auth';
import NavigationComponent from '../components/NavigationComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)

        this.handleCntry = this.handleCntry.bind(this)
        this.handleSignOut = this.handleSignOut.bind(this)
    }

    handleSignOut() {
        this.props.signout()
    }

    handleCntry() {
        const new_cntry = this.props.cntry == 'kr' ? 'us' : 'kr'

        this.props.changeCntry(new_cntry)
        this.props.requestListStock(new_cntry)
    }

    render () {
        const { cntry, level } = this.props
        const { handleCntry, handleSignOut } = this
        const manager = checkManager(level) ? true : false

        return (
            <NavigationComponent
                cntry={cntry}
                handleCntry={handleCntry}
                handleSignOut={handleSignOut}
            />
        )
    }
}

function mapStateToProps (state) {
    return {
        cntry: state.baseReducer.cntry,
        level: state.authReducer.level,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestListStock: bindActionCreators(requestListStock, dispatch),
        signout: bindActionCreators(signout, dispatch),
        changeCntry: bindActionCreators(changeCntry, dispatch),
    };
}

const NavigationContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default NavigationContainer;
