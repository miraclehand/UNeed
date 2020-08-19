import React from 'react';
import AlertRoomContainer from '../containers/AlertRoomContainer';

export class AlertRoomScreen extends React.Component {
    constructor(props) {
        super(props)
    }

    render () {
        const { watch_id } = this.props.route.params
        return (
            <AlertRoomContainer watch_id ={watch_id} />
        )
    }
}

export default AlertRoomScreen
