import React from 'react'; import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { Text, TextInput, Button } from 'react-native';
import { requestChatRoom, requestDeleteChatRoom } from '../actions/ChatRoomAction';
import ChatRoomComponent from '../components/ChatRoomComponent';

export class Connected extends React.Component {
    constructor(props) {
        super(props)
        this.handlePress = this.handlePress.bind(this)
        this.handleDelete = this.handleDelete.bind(this)
    }

    handlePress(watch_id) {
        this.props.handlePress(watch_id)
    }

    handleDelete(room) {
        const {os, db, email, token, cntry } = this.props

        this.props.requestDeleteChatRoom(os, db, email, token, cntry, room)
    }

    componentDidMount() {
        const { os, db, email, token, cntry, rooms } = this.props

        if (rooms.length === 0) {
            this.props.requestChatRoom(os, db, email, token, cntry);
        }
    }

    render() {
        return (
                <ChatRoomComponent
                    os = {this.props.os}
                    rooms = {this.props.rooms}
                    watchs={this.props.watchs}
                    handlePress={this.handlePress}
                    handleDelete={this.handleDelete}
                />
        )
   }
}

function mapStateToProps (state) {
    return {
        os: state.baseReducer.os,
        db: state.dbReducer.db,
        email: state.userReducer.email,
        cntry: state.baseReducer.cntry,
        rooms: state.chatRoomReducer.rooms,
        watchs: state.watchReducer.watchs,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestChatRoom : bindActionCreators(requestChatRoom, dispatch),
        requestDeleteChatRoom : bindActionCreators(requestDeleteChatRoom, dispatch),
    };
}

const ChatRoomContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default ChatRoomContainer;

