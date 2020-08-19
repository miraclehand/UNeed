import React from 'react';
import PropTypes from 'prop-types';
import Table from '@material-ui/core/Table'
import TableHead from '@material-ui/core/TableHead'
import TableBody from '@material-ui/core/TableBody'
import TableRow from '@material-ui/core/TableRow'
import TableCell from '@material-ui/core/TableCell'
import Tooltip from '@material-ui/core/Tooltip';

class ChartComponent extends React.Component {
    constructor(props) {
        super(props);
        this.genHeader = this.genHeader.bind(this)
        this.genBody = this.genBody.bind(this)
    }

    genHeader() {
        const headers = ['종목명', '현재가', '목표주가', '추정EPS', '추정PER', '업종PER', 'PER', '배당수익률', '투자의견(1~5)']
        return (
            <>
                { headers.map(header => {
                    return <TableCell>{header}</TableCell>
                })}
            </>
        )
    }

    genBody(company) {
        return (
            <>
                <TableCell>{company.name}</TableCell>
                <TableCell>{company.close}</TableCell>
                <TableCell>{company.target_price}</TableCell>
                <TableCell>{company.cns_eps}</TableCell>
                <TableCell>{company.cns_per}</TableCell>
                <TableCell>{company.per_field}</TableCell>
                <TableCell>{company.per}</TableCell>
                <TableCell>{company.dividend}</TableCell>
                <TableCell>{company.invt_opinion}</TableCell>
            </>
        )
    }

    render() {
        const { genHeader, genBody } = this
        const reg_chart  = this.props.charts[0]
        const log_chart  = this.props.charts[1]
        const hist_chart = this.props.charts[2]
        const vol_chart  = this.props.charts[3]
        const company1   = this.props.companies[0]
        const company2   = this.props.companies[1]
        const title_log  = '최적화, 계산값, 선택한 공적분'
        const title_hist = 'ks:정규성(↑), adf:정상성(↓), coint:공적분(↓)'

        return (
            <div align='center'>
                {reg_chart && <img src = {reg_chart} />}
                {log_chart &&
                    <Tooltip title={title_log} placement='top'>
                        <img src = {log_chart} />
                    </Tooltip>
                }
                {hist_chart &&
                    <Tooltip title={title_hist} placement='top'>
                        <img src = {hist_chart} />
                    </Tooltip>
                }
                {vol_chart && <img src = {vol_chart} />}
                <Table>
                    <TableHead>
                        <TableRow>
                            { genHeader() }
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        <TableRow> { company1 && genBody(company1) } </TableRow>
                        <TableRow> { company2 && genBody(company2) } </TableRow>
                    </TableBody>
                </Table>
            </div>
        );
    }
}

export default ChartComponent;
