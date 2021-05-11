import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import VirtualizedSelect from 'react-virtualized-select';
import Table from '@material-ui/core/Table';
import TableHead from '@material-ui/core/TableHead';
import TableBody from '@material-ui/core/TableBody';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';
import Paper from '@material-ui/core/Paper';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import green from '@material-ui/core/colors/green';
import MenuItem from '@material-ui/core/MenuItem';
import IconButton from '@material-ui/core/IconButton';
import DeleteOutlinedIcon from '@material-ui/icons/DeleteOutlined';
import { checkManager } from '../functions/auth';
import {MuiPickersUtilsProvider,KeyboardDatePicker} from '@material-ui/pickers';
import dayjs from 'dayjs';
import DayjsUtils from '@date-io/dayjs';
import 'dayjs/locale/ko';

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
    cell_red: {
        color: 'rgb(255,250,250)',
        backgroundColor: 'rgba(220, 20, 60, 1)',
        textAlign: 'right',

    },
    cell_blue: {
        color: 'rgb(255,250,250)',
        backgroundColor: 'rgba(0, 0, 255, 1)',
        textAlign: 'right',

    },
});

function withCommas(x) {
    if (typeof x == 'undefined') {
        return 'NaN'
    }
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

class TradingComponent extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            stock1: '',
            stock2: '',
            date1: dayjs().format('YYYY-MM-DD'),
            date2: dayjs().format('YYYY-MM-DD'),
            positions: [
                { value: '+', label: 'LONG', },
                { value: '-', label: 'SHORT',},
            ],
            pos1: '+',
            pos2: '-',
        };

        this.handleChangeDate  = this.handleChangeDate.bind(this);
        this.handleChangeStock = this.handleChangeStock.bind(this);
        this.handleChangePos   = this.handleChangePos.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

        this.genNewPairTable = this.genNewPairTable.bind(this);
        this.genNewPairBody  = this.genNewPairBody.bind(this);

        this.genEntryTable  = this.genEntryTable.bind(this);
        this.genEntriesBody = this.genEntriesBody.bind(this);
        this.genEntryRows   = this.genEntryRows.bind(this);
        this.genEntryCells  = this.genEntryCells.bind(this);

        this.genHeader = this.genHeader.bind(this);
        this.handleCloseEntry = this.handleCloseEntry.bind(this);
    }
  
    handleChangeDate(id, selectValue) {
        this.setState({[id]:selectValue})
    }

    handleChangeStock(id, selectValue) {
        this.setState({[id]:selectValue})
    }

    handleChangePos(id, form) {
        this.setState({[id]:form.target.value})
    }

    handleCloseEntry(e, cntry, entry_id) {
        this.props.handleCloseEntry(cntry, entry_id)
    }

    genNewPairTable() {
        const { genHeader, genNewPairBody } = this

        const headers = [{ value:'종목',     align:'center'},
                         { value:'진입일자', align:'center'},
                         { value:'포지션',   align:'center'},
                         { value:'단가',     align:'center'},
                         { value:'수량',     align:'center'},
        ]

        return (
        <>
            <Table className='new_pair'>
                <col style={{width:'20%'}}/>
                <col style={{width:'20%'}}/>
                <col style={{width:'20%'}}/>
                <col style={{width:'20%'}}/>
                <col style={{width:'20%'}}/>
                <TableHead>
                    <TableRow>
                        { genHeader(headers) }
                    </TableRow>
                </TableHead>
                <TableBody>
                    <TableRow className='pair1'>
                        { genNewPairBody(1) }
                    </TableRow>
                    <TableRow className='pair2'>
                        { genNewPairBody(2) }
                    </TableRow>
                </TableBody>
            </Table>
            </>
        )
    }

    genHeader(headers) {
        return (
            <>
            {headers.map(header => {
                return (
                    <TableCell align={header.align}> {header.value} </TableCell>
                )
            })}
            </>
        )
    }

    genNewPairBody(id) {
        const { stocks } = this.props
        const { wrapper, progress } = this.props.classes;
        const { handleChangeStock, handleChangeDate, handleChangePos } = this
        const stockName = ['stock'+ id]
        const posName   = ['pos'  + id]
        const dateName  = ['date' + id]
        const qtyName   = ['qty'  + id]
        const uvName    = ['uv'   + id]
        const stock     = eval('this.state.' + stockName)
        const date      = eval('this.state.' + dateName)
        const enabled = stocks.length == 0 ? false : true
        const posValue  = eval('this.state.' + posName)

        return (
            <>
            <TableCell className={wrapper}>
                <VirtualizedSelect
                    labelKey='label'
                    ValueKey='code'
                    disabled={!enabled}
                    options={stocks}
                    value={stock}
                    onChange={(value) => handleChangeStock(stockName,value)}
                />
                {!enabled && <CircularProgress size={24} className={progress}/>}
            </TableCell>
            <TableCell align='center'>
                <MuiPickersUtilsProvider utils={DayjsUtils} locale='ko'>
                    <KeyboardDatePicker
                        variant='inline'
                        autoOk
                        format='YYYY-MM-DD'
                        label='Date'
                        value={date}
                        onChange={(e) => handleChangeDate(dateName, e)}
                    />
                </MuiPickersUtilsProvider>
            </TableCell>
            <TableCell align='center'>
                <TextField name={posName}
                    select
                    value={posValue}
                    label="Position"
                    onChange={(value) => handleChangePos(posName,value)}
                >
                    {this.state.positions.map(option => (
                        <MenuItem key={option.value} value={option.value}>
                            {option.label}
                        </MenuItem>
                    ))}
                 </TextField>
            </TableCell>
            <TableCell align='right'>
                <TextField name={uvName} label='Unit Price'/>
            </TableCell>
            <TableCell align='right'>
                <TextField name={qtyName} label='Quantity'/>
            </TableCell>
            </>
        )
    }

    genEntryTable() {
        const { genHeader, genEntriesBody } = this
        const headers = [{ value:'Action',   align:'center'},
                         { value:'종목',     align:'center'},
                         { value:'평가손익', align:'right'},
                         { value:'수익률',   align:'right'},
                         { value:'단가',     align:'right'},
                         { value:'수량',     align:'right'},
                         { value:'금액',     align:'right'},
                         { value:'현재가',   align:'right'},
                         { value:'진입시점', align:'center'},
        ]

        return (
            <Paper>
                <Table className='entries'>
                    <col style={{width:'5%'}}/>
                    <col style={{width:'15%'}}/>
                    <col style={{width:'8%'}}/>
                    <col style={{width:'6%'}}/>
                    <col style={{width:'6%'}}/>
                    <col style={{width:'6%'}}/>
                    <col style={{width:'8%'}}/>
                    <col style={{width:'6%'}}/>
                    <col style={{width:'8%'}}/>
                    <TableHead>
                        { genHeader(headers) }
                    </TableHead>
                    <TableBody>
                        { genEntriesBody() }
                    </TableBody>
                </Table>
            </Paper>
        )
    }

    genEntryCells(id,label,value,uv,qty,amt,tick,date) {
        const yieldRate = (value / amt * 100).toFixed(2)

        return (
            <>
            <TableCell name={['label'+id]} align= 'left'>{label}</TableCell>
            <TableCell name={['value'+id]} align='right'>{withCommas(value)}</TableCell>
            <TableCell name={['yield'+id]} align='right'>{withCommas(yieldRate)}</TableCell>
            <TableCell name={['uv'+id]}    align='right'>{withCommas(uv)}</TableCell>
            <TableCell name={['qty'+id]}   align='right'>{withCommas(qty)}</TableCell>
            <TableCell name={['amt'+id]}   align='right'>{withCommas(amt)}</TableCell>
            <TableCell name={['tick'+id]}  align='right'>{withCommas(tick)}</TableCell>
            <TableCell align='center'>{date}</TableCell>
            </>
        )
    }

    genEntryRows(entry) {
        const { cell_red, cell_blue } = this.props.classes;
        const { genEntryCells, handleCloseEntry } = this
        const { entry_id, sum } = entry
        const { cntry1, label1, qty1, uv1, amt1, date1, tick1, value1 } = entry
        const { cntry2, label2, qty2, uv2, amt2, date2, tick2, value2 } = entry
        const cell_color = isNaN(sum) ? '' : sum > 0 ? cell_red : cell_blue

        return (
            <>
            <TableRow>
                <TableCell align='center' rowspan={2}>
                    <IconButton onClick={(e)=> handleCloseEntry(e, cntry1, entry_id)}>
                        <DeleteOutlinedIcon fontSize="large" /> 
                    </IconButton>
                </TableCell>
                {genEntryCells('1',label1,value1,uv1,qty1,amt1,tick1,date1)}
            </TableRow>
            <TableRow>
                {genEntryCells('2',label2,value2,uv2,qty2,amt2,tick2,date2)}
            </TableRow>
            <TableRow>
                <TableCell name='dummy'/>
                <TableCell align='center'>Total</TableCell>
                <TableCell className={cell_color}>{withCommas(sum)}</TableCell>
                <TableCell name='dummy'/>
            </TableRow>
            </>
        )
    }

    genEntriesBody() {
        const { entries } = this.props
        const { genEntryRows } = this

        return (
            <>
                {entries && entries.map(entry => {
                    return genEntryRows(entry)
                })}
            </>
        )
    }

    handleSubmit(e) {
        e.preventDefault();

        const {stock1, stock2 } = this.state
        const date1 = dayjs(this.state.date1).format('YYYY-MM-DD')
        const date2 = dayjs(this.state.date2).format('YYYY-MM-DD')

        let basket1 = {
            code: stock1.code,
            date: date1,
            pos: e.target.elements['pos1'].value,
            qty: e.target.elements['qty1'].value,
            uv: e.target.elements['uv1'].value,
        }
        let basket2 = {
            code: stock2.code,
            date: date2,
            pos: e.target.elements['pos2'].value,
            qty: e.target.elements['qty2'].value,
            uv: e.target.elements['uv2'].value,
        }

        this.props.handleOpenEntry(basket1, basket2)
    }

    render() {
        const { handleSubmit, genNewPairTable, genEntryTable } = this
        const { level, entries } = this.props
        const enabled = checkManager(level)
        const { cell_red, cell_blue } = this.props.classes;

        let total = 0

        entries && entries.map(entry => {
            const tick1 = this.props.ticks[entry.code1]
            const tick2 = this.props.ticks[entry.code2]
            const qty1 = entry.qty1
            const qty2 = entry.qty2
            const pos1 = entry.pos1
            const pos2 = entry.pos2
            const uv1 = entry.uv1
            const uv2 = entry.uv2
            const cost1 = entry.cost1
            const cost2 = entry.cost2
            const sign1 = pos1 == '+' ? 1 : -1
            const sign2 = pos2 == '+' ? 1 : -1

            let fee1  = tick1 * qty1 * (pos1 == '+' ? 0.00015 : 0.001)
            let fee2  = tick2 * qty2 * (pos2 == '+' ? 0.00015 : 0.001)
            let tax1  = pos1 == '+' ? tick1 * qty1 * 0.0025 : 0
            let tax2  = pos2 == '+' ? tick2 * qty2 * 0.0025 : 0

            fee1 = fee1 - fee1 % 10
            fee2 = fee2 - fee2 % 10
            tax1 = tax1 - tax1 % 10
            tax2 = tax2 - tax2 % 10

            tax1 = entry.track1 == 'ETF' ? 0 : tax1
            tax2 = entry.track2 == 'ETF' ? 0 : tax2

            entry.tick1 = tick1
            entry.tick2 = tick2
            entry.value1 = sign1 * qty1 * (tick1 - uv1) - cost1 - fee1 - tax1
            entry.value2 = sign2 * qty2 * (tick2 - uv2) - cost2 - fee2 - tax2
            entry.sum = entry.value1 + entry.value2
            total = total + entry.sum
        })

        const cell_color = isNaN(total) ? '' : total > 0 ? cell_red : cell_blue


        return (
            <div>
                <form onSubmit={ handleSubmit }>
                    <Paper>
                        { genNewPairTable() }
                    </Paper>
                    <br/>
                    <Button
                        variant='contained'
                        color='primary'
                        type='submit'
                        disabled={!enabled}
                    >
                        ADD
                    </Button>
                </form>
                <br/>
                <Paper>
                    <Table>
                        <TableRow>
                            <TableCell width='10%' className={cell_color}>
                                {withCommas(total)}
                            </TableCell>
                            <TableCell width='90%' name='dummy'/>
                        </TableRow>
                    </Table>
                </Paper>
                <br/>
                <Paper>
                    { genEntryTable() }
                </Paper>
            </div>
        );
    }
}

export default withStyles(styles)(TradingComponent);
