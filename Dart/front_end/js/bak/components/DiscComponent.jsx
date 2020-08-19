import React from 'react';
import PropTypes from 'prop-types';
import Table from '@material-ui/core/Table'
import TableHead from '@material-ui/core/TableHead'
import TableBody from '@material-ui/core/TableBody'
import TableRow from '@material-ui/core/TableRow'
import TableCell from '@material-ui/core/TableCell'
import Tooltip from '@material-ui/core/Tooltip';

class DiscComponent extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const { discs } = this.props

        return (
            <div align='center'>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell> 시간 </TableCell>
                            <TableCell> 공시대상회사 </TableCell>
                            <TableCell> 보고서명 </TableCell>
                            <TableCell> 제출인 </TableCell>
                            <TableCell> 접수일자 </TableCell>
                            <TableCell> 비고 </TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        { discs && discs.map((disc,i) => {
                            return (
                                <TableRow key={i}>
                                    <TableCell>{disc.reg_time}</TableCell>
                                    <TableCell>{disc.corp.corp_name}</TableCell>
                                    <TableCell>{disc.report_nm}</TableCell>
                                    <TableCell>{disc.flr_nm}</TableCell>
                                    <TableCell>{disc.rcept_dt}</TableCell>
                                    <TableCell>{disc.rm}</TableCell>
                                </TableRow>
                            )
                        })}
                    </TableBody>
                </Table>
            </div>
        );
    }
}

export default DiscComponent;
