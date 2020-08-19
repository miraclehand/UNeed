import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestListStdDisc } from '../actions/ListAction';
import { setUnitStdDisc, setUnitDetail } from '../actions/UnitAction';
import SetupUnitComponent from '../components/SetupUnitComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)

        this.handleUnitStdDisc = this.handleUnitStdDisc.bind(this)
        this.handleUnitDetail  = this.handleUnitDetail.bind(this)
    }

    componentDidMount() {
        if (this.props.list_std_disc.length === 0) {
            this.props.requestListStdDisc(this.props.cntry);
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
                list_std_disc={this.props.list_std_disc}
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
        list_std_disc: state.listReducer.list_std_disc,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestListStdDisc :bindActionCreators(requestListStdDisc,dispatch),
        setUnitStdDisc: bindActionCreators(setUnitStdDisc,dispatch),
        setUnitDetail : bindActionCreators(setUnitDetail,dispatch),
    };
}

const SetupSimulaContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default SetupSimulaContainer;
