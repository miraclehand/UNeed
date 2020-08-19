import React from 'react';
import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
    alert: {
        position: 'absolute',
        backgroundColor: '#fff',
        top: '30%',
        left: '30%',
        right: '30%',
        padding: '15px',
        border: '2px solid #444',
    },
    alert_back: {
        position: 'absolute',
        backgroundColor: 'rgba(0, 0, 0, 0.15)',
        top: '0px',
        left: '0px',
        bottom: '0px',
        right: '0px',
    },
});


class AlertComponent extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const { component } = this.props;
        const { alert_back, alert } = this.props.classes;

        return (
            <div className={alert_back}>
                <div className={alert}>
                    {component}
                </div>
            </div>
        );
    }
}

export default withStyles(styles)(AlertComponent);
