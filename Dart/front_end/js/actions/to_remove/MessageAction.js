import * as ACTION_TYPE from '../constants/action-types';
import * as URL from '../constants/url';
import { getHeaderAuth } from './FetchOptions';
import { exec_query, select_query } from '../util/dbUtil';

export function receiveMessage(db, watch_id, chat) {
    const { rcept_dt, reg_time, corp_code, corp_name, stock_code, rcept_no, report_nm, tick, content, url } = chat

    const chat_type = 1
    const sql = 'insert into chat(watch_id, chat_type, corp_code, corp_name, stock_code, report_nm, tick, url, content, rcept_dt, reg_time) values(?,?,?,?,?,?,?,?,?,?,?)'

    exec_query(db, sql, [watch_id, chat_type, corp_code, corp_name, stock_code, report_nm, tick, url, content, rcept_dt, reg_time])

    //const chat = {'watch_id':watch_id, 'chat_type':chat_type, 'corp_code':corp_code, 'corp_name':corp_name, 'stock_code':stock_code, 'tick':tick, 'report_nm':report_nm, 'url':url, 'content':content, 'rcept_dt':rcept_dt, 'reg_time':reg_time}
    return dispatch => {
        dispatch({type: ACTION_TYPE.UPSERT_CHAT, chat})
    }
}
