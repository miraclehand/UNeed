import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import green from '@material-ui/core/colors/green';
import IconButton from '@material-ui/core/IconButton';
import SwapVertIcon from '@material-ui/icons/SwapVert';
import CircularProgress from '@material-ui/core/CircularProgress';
import VirtualizedSelect from 'react-virtualized-select';
import {MuiPickersUtilsProvider,KeyboardDatePicker} from '@material-ui/pickers';
import dayjs from 'dayjs';
import DayjsUtils from '@date-io/dayjs';
import 'dayjs/locale/ko';
import '../../css/BaseStyle.css';


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

class ChartFormComponent extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            stock1: '',
            stock2: '',
            date1: dayjs().add(-2,'year').format('YYYY-MM-DD'),
            date2: dayjs().format('YYYY-MM-DD'),
        }
        this.handleChangeDate = this.handleChangeDate.bind(this);
        this.handleChangeStock = this.handleChangeStock.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleOnClickExchange = this.handleOnClickExchange.bind(this);
    }

    handleChangeDate(id, selectValue) {
        this.setState({[id]:selectValue})
    }

    handleChangeStock(id, selectValue) {
        this.setState({[id]:selectValue})
    }

    handleOnClickExchange() {
        const stock1 = this.state.stock1
        const stock2 = this.state.stock2

        this.setState({stock1:stock2})
        this.setState({stock2:stock1})
    }

    handleSubmit(e) {
        e.preventDefault();

        const { stock1, stock2 } = this.state;
        const date1 = dayjs(this.state.date1).format('YYYY-MM-DD')
        const date2 = dayjs(this.state.date2).format('YYYY-MM-DD')

        this.props.handleSubmit(date1, date2, stock1.code, stock2.code)
    }

    componentDidMount() {
    }

    render() {
        const { stocks } = this.props;
        const { wrapper, progress } = this.props.classes;
        const { date1, date2, stock1, stock2 } = this.state;
        const { handleChangeStock, handleChangeDate, handleSubmit } = this;
        const { handleOnClickExchange } = this
        const enabled = stocks.length == 0 ? false : true

        return (
            <form onSubmit={ handleSubmit }>
                <MuiPickersUtilsProvider utils={DayjsUtils} locale='ko'>
                    <div className='margin-box1'>
                        <KeyboardDatePicker
                            variant='inline'
                            autoOk
                            format='YYYY-MM-DD'
                            label='Date1'
                            value={date1}
                            onChange={(e) => handleChangeDate('date1', e)}
                        />
                        &nbsp;
                        <KeyboardDatePicker
                            variant='inline'
                            autoOk
                            format='YYYY-MM-DD'
                            label='Date2'
                            value={date2}
                            onChange={(e) => handleChangeDate('date2', e)}
                        />
                    </div>
                    <div className='margin-box1'>
                    </div>
                </MuiPickersUtilsProvider>
                <br/>
                <div className={wrapper}>
                    <VirtualizedSelect
                        labelKey='label'
                        ValueKey='code'
                        disabled={!enabled}
                        options={stocks}
                        value={stock1}
                        onChange={(value) => handleChangeStock('stock1',value)}
                    />
                    {!enabled && <CircularProgress size={24} className={progress}/>}
                </div>
                <div className={wrapper}>
                    <VirtualizedSelect
                        labelKey='label'
                        ValueKey='code'
                        disabled={!enabled}
                        options={stocks}
                        value={stock2}
                        onChange={(value) => handleChangeStock('stock2',value)}
                    />
                    {!enabled && <CircularProgress size={24} className={progress}/>}
                </div>
                <Button variant='contained' color='primary' type='submit'>
                    SUBMIT
                </Button>
                <IconButton onClick={handleOnClickExchange}>
                    <SwapVertIcon fontSize="large" />
                </IconButton>
            </form>
        );
    }
}

export default withStyles(styles)(ChartFormComponent);
