import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestSimula } from '../actions/SimulaAction';
import SimulaComponent from '../components/SimulaComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)

        this.handlePress  = this.handlePress.bind(this)
        this.handleSimula = this.handleSimula.bind(this)
    }

    handlePress(simula) {
        this.props.handlePress(simula)
    }

    componentDidMount() {
        const {os, db, dbName, email, token, cntry } = this.props

        this.props.requestSimula(os, db, email, token, cntry);
    }

    handleSimula(newSimula) {
        let exists = 0
        const {os, db, dbName, email, token, cntry, simulas } = this.props

        simulas && simulas.map((value, i) => {
            if (value.simula === newSimula) {
                exists = exists + 1
            }
        })
        if (exists > 0) {
            alert('이미 등록된 Simula 입니다.')
            return;
        }

        this.props.requestPostSimula(os, db, email, token, cntry, newSimula)
        alert('Simula가 등록되었습니다.')
    }

    render() {
        return (
            <SimulaComponent
                simulas = {this.props.simulas}
                handlePress={this.handlePress}
            />
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
        simulas: state.simulaReducer.simulas,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestSimula: bindActionCreators(requestSimula, dispatch),
    };
}

const SimulaContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default SimulaContainer;
