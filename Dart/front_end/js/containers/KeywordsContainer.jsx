import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestKeywords } from '../actions/KeywordsAction';
import KeywordsComponent from '../components/KeywordsComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)
    }

    componentDidMount() {
        const {email, token, cntry } = this.props

        this.props.requestKeywords(email, token, cntry);
    }

    render() {
        const { keywords } = this.props

        return <KeywordsComponent keywords={keywords} />
   }
}

function mapStateToProps (state) {
    return {
        email: state.userReducer.email,
        cntry: state.baseReducer.cntry,
        keywords: state.keywordsReducer.keywords,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestKeywords : bindActionCreators(requestKeywords,  dispatch),
    };
}

const KeywordsContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default KeywordsContainer;
