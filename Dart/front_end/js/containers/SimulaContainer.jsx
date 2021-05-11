import React from 'react';
import { Text } from 'react-native'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestSimula, requestDeleteSimula } from '../actions/SimulaAction';
import SimulaComponent from '../components/SimulaComponent';
import { db_create_table, db_drop_table } from '../device/db';

export class Connected extends React.Component {
    constructor(props) {
        super(props)

        this.handleDelete = this.handleDelete.bind(this)
        this.handlePress = this.handlePress.bind(this)
        this.handleNewSimula = this.handleNewSimula.bind(this)
    }

    handlePress(simula) {
        const {db } = this.props
        //this.props.handlePress(simula)
        let tables = db_drop_table(db)
        Promise.all(tables)
        let tables = db_create_table(db)
        Promise.all(tables)

    }

    handleDelete(simula) {
        const {os, db, dbName, email, token, cntry } = this.props
        this.props.requestDeleteSimula(os, db, email, token, cntry, simula)
    }

    componentDidMount() {
        const {os, db, dbName, email, token, cntry } = this.props

        this.props.requestSimula(os, db, email, token, cntry);
    }

    handleNewSimula(newSimula) {
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
                os={this.props.os}
                simulas = {this.props.simulas}
                handlePress={this.handlePress}
                handleDelete={this.handleDelete}
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
        requestDeleteSimula: bindActionCreators(requestDeleteSimula, dispatch),
    };
}

const SimulaContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default SimulaContainer;
