import React from 'react';
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

    handleUnitDetail(unitDetail) {
        this.props.setUnitDetail(unitDetail)
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
        unitStdDisc: state.unitReducer.std_disc,
        unitDetail: state.unitReducer.unitDetail,
        std_discs: state.dbReducer.std_discs,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestStdDiscs:bindActionCreators(requestStdDiscs,dispatch),
        setUnitStdDisc: bindActionCreators(setUnitStdDisc,dispatch),
        setUnitDetail : bindActionCreators(setUnitDetail,dispatch),
    };
}

const SetupSimulaContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default SetupSimulaContainer;
