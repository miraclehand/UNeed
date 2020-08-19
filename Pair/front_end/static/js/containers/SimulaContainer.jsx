import React from 'react';
import Button from '@material-ui/core/Button';
import SaveIcon from '@material-ui/icons/Save';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestProgress, requestStopProgress} from '../actions/ProgressAction';
import { requestSimula, requestPostSimula } from '../actions/SimulaAction';
import ProgressComponent from '../components/ProgressComponent'
import StrainerContainer from '../containers/StrainerContainer'

class Connected extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            seconds: 0,
            component : '',
        }

        this.handleSubmit        = this.handleSubmit.bind(this)
        this.handleComponent     = this.handleComponent.bind(this)
        this.handleSaveStrainer  = this.handleSaveStrainer.bind(this)
        this.handleStopProgress  = this.handleStopProgress.bind(this)
        this.timerSeconds        = this.timerSeconds.bind(this)
        this.timerProgress       = this.timerProgress.bind(this)
        this.startTimer          = this.startTimer.bind(this)
        this.finishTimer         = this.finishTimer.bind(this)
    }

    timerSeconds() {
        this.setState({seconds:this.state.seconds+1})
    }

    timerProgress() {
        const { username, token, cntry, seconds, progress } = this.props
        const { requestProgress } = this.props

        requestProgress(username, token, cntry)
        
        if (seconds > 0 && this.state.seconds < 5) {
            this.setState({seconds:seconds})
        }

        if (progress == 100) {
            this.finishTimer()
        }
    }

    startTimer() {
        this.state.seconds = 1

        this.interval_seconds = setInterval(() => {
            this.timerSeconds()
        }, 1000);

        this.interval_progress = setInterval(() => {
            this.timerProgress()
        }, 3000);
    }

    finishTimer() {
        clearInterval(this.interval_seconds);
        clearInterval(this.interval_progress);
    }

    handleSubmit(e) {
        e.preventDefault();

        const { username, token, cntry } = this.props
        const { requestPostSimula } = this.props
        const { strainer } = this.state.component.state

        this.finishTimer()
        this.startTimer()
        requestPostSimula(username, token, cntry, strainer)
    }

    handleComponent(component) {
        this.state.component = component
        this.props.handleComponent(component)
    }

    handleSaveStrainer(e) {
        const { strainer } = this.state.component.state
        this.state.component.handleSaveStrainer(strainer)
    }

    handleStopProgress(e) {
        const { username, token, cntry } = this.props
        const { requestStopProgress } = this.props

        requestStopProgress(username, token, cntry)

        this.finishTimer()
    }

    componentDidMount() {
        const { seconds, username, token, cntry } = this.props
        const { requestSimula } = this.props

        requestSimula(username, token, cntry)
        this.timerProgress()
        this.startTimer()
    }

    componentWillUnmount() {
        this.finishTimer()
    }

    render () {
        const { handleComponent, handleSaveStrainer, handleStopProgress } = this
        const { handleSubmit } = this
        const { seconds } = this.state
        const { progress } = this.props

        return (
            <form onSubmit={ handleSubmit }>
                <ProgressComponent
                    seconds = {seconds}
                    progress = {progress}
                    handleStopProgress={handleStopProgress}
                />
                <StrainerContainer
                    handleComponent={handleComponent}
                />
                <br/>
                <Button
                    variant="contained"
                    color="secondary"
                    onClick={handleSaveStrainer}
                    startIcon={<SaveIcon />}
                >
                    Save
                </Button>
                &nbsp;&nbsp;&nbsp;&nbsp;
                <Button variant='contained' color='primary' type='submit'>
                    Simula
                </Button>
            </form>
        )
    }
};

function mapStateToProps (state) {
    return {
        cntry: state.baseReducer.cntry,
        username: state.authReducer.username,
        token: state.authReducer.token,
        seconds: state.strategyReducer.seconds,
        progress: state.strategyReducer.progress,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        requestProgress: bindActionCreators(requestProgress, dispatch),
        requestStopProgress: bindActionCreators(requestStopProgress, dispatch),
        requestSimula: bindActionCreators(requestSimula, dispatch),
        requestPostSimula: bindActionCreators(requestPostSimula, dispatch),
    };
}

const SimulaContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);

export default SimulaContainer;
