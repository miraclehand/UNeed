import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { popup_close } from '../actions/PopupAction';
import PopupComponent from '../components/PopupComponent'

class Connected extends React.Component {
    constructor(props) {
        super(props)
    }

    render () {
        const { open, title, content, popup_close } = this.props
        const { handleClose } = this

        return <PopupComponent
                   open={open}
                   title={title}
                   content={content}
                   handleClose={popup_close}
               />
    }
};

function mapStateToProps (state) {
    return {
        open: state.popupReducer.open,
        title: state.popupReducer.title,
        content: state.popupReducer.content,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        popup_close: bindActionCreators(popup_close, dispatch),
    };
}

const PopupContainer = connect(mapStateToProps,mapDispatchToProps)(Connected);

export default PopupContainer;
