import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import ChartComponent from '../components/ChartComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        const { companies, charts } = this.props
        
        return <ChartComponent companies={companies} charts={charts} />
    }
}

function mapStateToProps (state) {
    return {
        charts: state.chartReducer.charts,
        companies: state.chartReducer.companies,
    };
};

const ChartContainer = connect(mapStateToProps, null)(Connected);
export default ChartContainer;
