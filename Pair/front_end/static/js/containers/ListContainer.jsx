import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestPickedPair } from '../actions/PairAction';
import { requestSimula } from '../actions/SimulaAction';
import { requestStrainer } from '../actions/StrainerAction';
import ListComponent from '../components/ListComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)
    }

    componentDidMount() {
        const { username, token, cntry } = this.props

        if (this.props.target == 'PickedPair') {
            this.props.requestPickedPair('kr');
            this.props.requestPickedPair('us');
        }
        else if (this.props.target == 'Simula') {
            this.props.requestSimula(username, token, cntry);
        }
        else if (this.props.target == 'Strainer') {
            this.props.requestStrainer(username, token, cntry);
        }
    }

    render() {
        const { target, picked_pairs, simulas, strainers } = this.props
        const { handleListItemClick } = this
        const labels = ['KOREA', 'AMERICA', 'CHINA', 'JAPAN']

        let list_type
        let lists
        if (target == 'PickedPair') {
            list_type = 'File'
            lists = picked_pairs
        }
        else if (target == 'Simula') {
            list_type = 'File'
            lists = simulas
        }
        else if (target == 'Strainer') {
            list_type = 'Object'
            lists = strainers
        }

        return <ListComponent
                    list_type ={list_type}
                    labels={labels}
                    lists={lists}
                    handleListItemClick  ={this.props.handleListItemClick}
                    handleListItemRemove ={this.props.handleListItemRemove}
               />
    }
}

function mapStateToProps (state) {
    return {
        username: state.authReducer.username,
        token: state.authReducer.token,
        cntry: state.baseReducer.cntry,
        node_pairs: state.pairReducer.node_pairs,
        picked_pairs: state.pairReducer.picked_pairs,
        simulas: state.simulaReducer.simulas,
        strainers: state.strainerReducer.strainers,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestPickedPair: bindActionCreators(requestPickedPair, dispatch),
        requestSimula: bindActionCreators(requestSimula, dispatch),
        requestStrainer: bindActionCreators(requestStrainer, dispatch),
    };
}

const ListFileContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default ListFileContainer;
