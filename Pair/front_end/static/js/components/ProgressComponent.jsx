import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import green from '@material-ui/core/colors/green';
import LinearProgress from '@material-ui/core/LinearProgress';
import IconButton from '@material-ui/core/IconButton';
import HighlightOffOutlinedIcon from '@material-ui/icons/HighlightOffOutlined';

const styles = theme => ({
    wrapper: {
        margin: theme.spacing.unit,
        position: 'relative',
    },
    progress: {
        color: green[500],
        position: 'absolute',
        top: '50%',
        left: '50%',
        marginTop: -12,
        marginLeft: -12,
    },
});

class ProgressComponent extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const { seconds, progress, handleStopProgress } = this.props;
        const variant = progress == 100 ? 'determinate' : 'indeterminate'

        return (
            <div>
                <LinearProgress variant="determinate" value={progress} />
                <br/>
                <LinearProgress variant={variant} color="secondary" />
                <br/>
                {seconds > 5 &&
                    <div>
                        {seconds}초
                        <IconButton onClick={handleStopProgress}>
                            <HighlightOffOutlinedIcon fontSize="large" />
                        </IconButton>
                    </div>
                }
            </div>
        );
    }
}

export default withStyles(styles)(ProgressComponent);
