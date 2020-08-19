import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import purple from '@material-ui/core/colors/purple';
import {MuiPickersUtilsProvider,KeyboardDatePicker} from '@material-ui/pickers';
import dayjs from 'dayjs';
import DayjsUtils from '@date-io/dayjs';
import 'dayjs/locale/ko';

const styles = theme => ({
    container: {
        display: 'flex',
        flexWrap: 'wrap',
    },
    textField: {
        marginLeft: theme.spacing(1),
        marginRight: theme.spacing(1),
        width: 200,
    },
    dense: {
        marginTop: 19,
    },
    menu: {
        width: 200,
    },
    padding: {
        padding: theme.spacing(3,2),
    },
    entry_paper: {
        padding: theme.spacing(3,2),
    },
    exit_paper: {
        padding: theme.spacing(3,2),
        backgroundColor: purple[100],
    }
});

const stock_types = [
     { value: 1, label: '보통주', },
     { value: 2, label: '보통주+우선주', },
];

const stock_industries = [
    { value: 1, label: '같은산업', },
    { value: 2, label: '모든산업', },
];

const stock_except_industries = [
    { value: '제약', label: '제약제외', },
    { value: 'XXXX', label: '제외하지않음', },
];


class StrainerComponent extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            seconds: 0,
            strainer: {
                name: '',

                /* period */
                date1: dayjs().add(-2,'year').format('YYYY-MM-DD'),
                date2: dayjs().format('YYYY-MM-DD'),

                /******************* buy *******************/
                /* stock filter */
                close:2000,
                avg_v50: 2000,
                stock_type: 1,
                stock_ind: 1,
                stock_exc_ind: '제약',

                /* pair spread */
                density:0.5,
                place:0.05,
                coint:0.4,
                dist_yield:10,
                coint_std:0.5,
                hit0_cnt:0,
                cy5_cnt:0,
                cy10_cnt:0,
                cy15_cnt:0,
                cy20_cnt:0,

                /* pair null hypothesis test */
                ks_pvalue:0.1,
                adf_pvalue:0.05,
                coint_pvalue:0.05,

                /* sell */
                clear_yield: 20,
                loss_yield: -20,
                days: 30,
            },
        }

        this.handleChangeStrainer = this.handleChangeStrainer.bind(this)
        this.handleSaveStrainer   = this.handleSaveStrainer.bind(this)
        this.handleDeleteStrainer = this.handleDeleteStrainer.bind(this)
    }

    handleChangeStrainer(id, e) {
        const value = typeof e.target == 'object' ? e.target.value : dayjs(e).format('YYYY-MM-DD')
        const strainer = Object.assign({}, this.state.strainer, {[id]:value})

        this.setState({strainer:strainer})
    }

    handleSaveStrainer(strainer) {
        this.props.handleSaveStrainer(strainer)
    }
    
    handleDeleteStrainer(strainer) {
        this.props.handleDeleteStrainer(strainer)
    }

    componentDidMount() {
        this.props.handleComponent(this)
    }

    render() {
        const { classes } = this.props
        const { strainer } = this.state;
        const { handleChangeStrainer } = this;
        const { handleSaveStrainer } = this;

        return (
            <>
                <Paper className={classes.padding} >
                    <Typography variant='H5' component='H3'>
                        Strainer
                    </Typography>
                    <TextField
                        id='name'
                        label='name'
                        className={classes.textField}
                        value={strainer['name']}
                        onChange={(e) => handleChangeStrainer('name', e)}
                        helperText="name of strainer"
                        margin='normal'
                    />
                </Paper>
                <br/>
                <Paper className={classes.padding} >
                    <Typography variant='H5' component='H3'>
                        Period
                    </Typography>
                    <div>
                    <MuiPickersUtilsProvider utils={DayjsUtils} locale='ko'>
                    <KeyboardDatePicker
                        variant='inline'
                        autoOk
                        format='YYYY-MM-DD'
                        label='Date1'
                        value={strainer['date1']}
                        onChange={(e) => handleChangeStrainer('date1', e)}
                    />
                    &nbsp;
                    <KeyboardDatePicker
                        variant='inline'
                        autoOk
                        format='YYYY-MM-DD'
                        label='Date2'
                        value={strainer['date2']}
                        onChange={(e) => handleChangeStrainer('date2', e)}
                    />
                    </MuiPickersUtilsProvider>
                    </div>
                </Paper>
                <br/>
                <Paper className={classes.entry_paper} >
                    <Typography variant='H5' component='H3'>
                        Stock Filter
                    </Typography>
                    <TextField
                        id='close'
                        label='close'
                        className={classes.textField}
                        value={strainer['close']}
                        onChange={(e) => handleChangeStrainer('close', e)}
                        helperText="more than X"
                        margin='normal'
                    />
                    {/*
                    <TextField
                        id='avg_v50'
                        label='avg_v50'
                        className={classes.textField}
                        value={strainer['avg_v50']}
                        onChange={(e) => handleChangeStrainer('avg_v50', e)}
                        helperText="more than X"
                        margin='normal'
                    />
                    */}
                    <TextField
                        id="stock_type"
                        select
                        label="type of stocks"
                        className={classes.textField}
                        value={strainer['stock_type']}
                        onChange={(e) => handleChangeStrainer('stock_type', e)}
                        SelectProps={{
                          MenuProps: {
                            className: classes.menu,
                          },
                        }}
                        margin="normal"
                    >
                    {stock_types.map(option => (
                        <MenuItem key={option.value} value={option.value}>
                            {option.label}
                        </MenuItem>
                    ))}
                    </TextField>
                    <TextField
                        id="stock_ind"
                        select
                        label="industry of stocks"
                        className={classes.textField}
                        value={strainer['stock_ind']}
                        onChange={(e) => handleChangeStrainer('stock_ind', e)}
                        SelectProps={{
                          MenuProps: {
                            className: classes.menu,
                          },
                        }}
                        margin="normal"
                    >
                    {stock_industries.map(option => (
                        <MenuItem key={option.value} value={option.value}>
                            {option.label}
                        </MenuItem>
                    ))}
                    </TextField>
                    <TextField
                        id="stock_exc_ind"
                        select
                        label="except stock of industry"
                        className={classes.textField}
                        value={strainer['stock_exc_ind']}
                        onChange={(e)=>handleChangeStrainer('stock_exc_ind', e)}
                        SelectProps={{
                          MenuProps: {
                            className: classes.menu,
                          },
                        }}
                        margin="normal"
                    >
                    {stock_except_industries.map(option => (
                        <MenuItem key={option.value} value={option.value}>
                            {option.label}
                        </MenuItem>
                    ))}
                    </TextField>
                </Paper>
                <br/>
                <Paper className={classes.entry_paper} >
                    <Typography variant='H5' component='H3'>
                        Pair Spread
                    </Typography>
                    <TextField
                        id='density'
                        label='density'
                        className={classes.textField}
                        value={strainer['density']}
                        onChange={(e) => handleChangeStrainer('density', e)}
                        helperText="less than X"
                        margin='normal'
                    />
                    <TextField
                        id='place'
                        label='place'
                        className={classes.textField}
                        value={strainer['place']}
                        onChange={(e) => handleChangeStrainer('place', e)}
                        helperText="both ends of the range"
                        margin='normal'
                    />
                    <TextField
                        id='coint'
                        label='coint'
                        className={classes.textField}
                        value={strainer['coint']}
                        onChange={(e) => handleChangeStrainer('coint', e)}
                        helperText="both ends of the range"
                        margin='normal'
                    />
                    <TextField
                        id='coint_std'
                        label='std of coint'
                        className={classes.textField}
                        value={strainer['coint_std']}
                        onChange={(e) => handleChangeStrainer('coint_std', e)}
                        helperText="less than X"
                        margin='normal'
                    />
                    <TextField
                        id='hit0_cnt'
                        label='count of zero hits'
                        className={classes.textField}
                        value={strainer['hit0_cnt']}
                        onChange={(e) => handleChangeStrainer('hit0_cnt', e)}
                        helperText="more than X"
                        margin='normal'
                    />
                    <TextField
                        id='cy5_cnt'
                        label='count of cycles at 5 averages of both ends'
                        className={classes.textField}
                        value={strainer['cy5_cnt']}
                        onChange={(e) => handleChangeStrainer('cy5_cnt', e)}
                        helperText="more than X"
                        margin='normal'
                    />
                    <TextField
                        id='cy10_cnt'
                        label='count of cycles at 10 averages of both ends'
                        className={classes.textField}
                        value={strainer['cy10_cnt']}
                        onChange={(e) => handleChangeStrainer('cy10_cnt', e)}
                        helperText="more than X"
                        margin='normal'
                    />
                    <TextField
                        id='cy15_cnt'
                        label='count of cycles at 15 averages of both ends'
                        className={classes.textField}
                        value={strainer['cy15_cnt']}
                        onChange={(e) => handleChangeStrainer('cy15_cnt', e)}
                        helperText="more than X"
                        margin='normal'
                    />
                    <TextField
                        id='cy20_cnt'
                        label='count of cycles at 20 averages of both ends'
                        className={classes.textField}
                        value={strainer['cy20_cnt']}
                        onChange={(e) => handleChangeStrainer('cy20_cnt', e)}
                        helperText="more than X"
                        margin='normal'
                    />
                    {/********************************************
                    <TextField
                        id='dist_max_min'
                        label='distance of two vertices'
                        className={classes.textField}
                        value={strainer['dist_vertices']}
                        onChange={(e) => handleChangeStrainer('dist_vertices', e)}
                        helperText='distance between maximum and minimum value from zero in spread
                        margin='normal'
                    />
                    <TextField
                        id='dist_farthest'
                        label='distance of two vertices'
                        className={classes.textField}
                        value={strainer['dist_vertices']}
                        onChange={(e) => handleChangeStrainer('dist_vertices', e)}
                        helperText='distance between the farthest and current value in spread'
                        margin='normal'
                    />
                    ********************************************/}
                    <TextField
                        id='dist_yield'
                        label='distance of yield'
                        className={classes.textField}
                        value={strainer['dist_yield']}
                        onChange={(e) => handleChangeStrainer('dist_yield', e)}
                        helperText="both ends of the range"
                        margin='normal'
                    />
                </Paper>
                <br/>
                <Paper className={classes.entry_paper} >
                    <Typography variant='H5' component='H3'>
                        Pair Null Hypothesis Test
                    </Typography>
                    <TextField
                        id='ks_pvalue'
                        label='ks pvalue'
                        className={classes.textField}
                        value={strainer['ks_pvalue']}
                        onChange={(e) => handleChangeStrainer('ks_pvalue', e)}
                        helperText='more than X'
                        margin='normal'
                    />
                    <TextField
                        id='adf_pvalue'
                        label='adf pvalue'
                        className={classes.textField}
                        value={strainer['adf_pvalue']}
                        onChange={(e) => handleChangeStrainer('adf_pvalue', e)}
                        helperText='less than X'
                        margin='normal'
                    />
                    <TextField
                        id='coint_pvalue'
                        label='coint pvalue'
                        className={classes.textField}
                        value={strainer['coint_pvalue']}
                        onChange={(e) => handleChangeStrainer('coint_pvalue', e)}
                        helperText='less than X'
                        margin='normal'
                    />
                </Paper>
                <br/>

                <Paper className={classes.exit_paper} >
                    <Typography variant='H5' component='H3'>
                        Liquidation
                    </Typography>
                    <TextField
                        id='clear_yield'
                        label='yield'
                        value={strainer['clear_yield']}
                        onChange={(e) => handleChangeStrainer('clear_yield',e)}
                        helperText='reaches over X'
                        margin='normal'
                    />
                    <TextField
                        id='loss_yield'
                        label='loss cut'
                        value={strainer['loss_yield']}
                        onChange={(e) => handleChangeStrainer('loss_yield',e)}
                        helperText='reaches under X'
                        margin='normal'
                    />
                    <TextField
                        id='days'
                        label='expire days'
                        value={strainer['days']}
                        onChange={(e) => handleChangeStrainer('days', e)}
                        helperText='after X days'
                        margin='normal'
                    />
                </Paper>
            </>
        );
    }
}

export default withStyles(styles)(StrainerComponent);
