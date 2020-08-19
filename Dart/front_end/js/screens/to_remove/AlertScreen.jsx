import React from 'react';
import AlertContainer from '../containers/AlertContainer';

export class AlertScreen extends React.Component {
    constructor(props) {
        super(props)
        this.handlePress = this.handlePress.bind(this)
    }

    handlePress(watch_id) {
        console.log('AlertScreen', watch_id, this.props.navigation)
        this.props.navigation.navigate('AlertRoom', {
            'watch_id': watch_id,
        })
    }

    componentDidMount() {
        console.log('AlertScreen componentDidMount')
    }

    render () {
        console.log('AlertScreen render')
        return (
            <AlertContainer handlePress={this.handlePress}/>
        )
    }
}

export default AlertScreen
