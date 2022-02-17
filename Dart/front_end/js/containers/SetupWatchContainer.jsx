import React from 'react';
import { Text } from 'react-native';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestStdDiscs } from '../actions/ServerPoolAction';
import { setUnitStdDisc, setUnitDetail } from '../actions/UnitAction';
import SetupUnitComponent from '../components/SetupUnitComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)

        this.handleUnitStdDisc = this.handleUnitStdDisc.bind(this)
        this.handleUnitDetail  = this.handleUnitDetail.bind(this)
    }

    componentDidMount() {
        const { os, db, email, token, cntry, std_discs } = this.props

        if (std_discs.length === 0) {
            this.props.requestStdDiscs(os, db, cntry);
        }
    }

    handleUnitStdDisc(unitStdDisc) {
        this.props.setUnitStdDisc(unitStdDisc)
    }

    handleUnitDetail(vals, nums) {
        this.props.setUnitDetail({'vals':vals,'nums':nums})
    }

    render() {
        return (
            <SetupUnitComponent
                unitStdDisc={this.props.unitStdDisc}
                unitDetail={this.props.unitDetail}
                std_discs={this.props.std_discs}
                handleUnitStdDisc={this.handleUnitStdDisc}
                handleUnitDetail={this.handleUnitDetail}
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
        std_discs: state.dbReducer.std_discs,
        unitStdDisc: state.unitReducer.std_disc,
        unitDetail: state.unitReducer.unitDetail,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestStdDiscs:bindActionCreators(requestStdDiscs,dispatch),
        setUnitStdDisc:bindActionCreators(setUnitStdDisc,dispatch),
        setUnitDetail :bindActionCreators(setUnitDetail,dispatch),
    };
}

const SetupWatchContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default SetupWatchContainer;
