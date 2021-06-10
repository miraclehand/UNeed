import { getDisassembled } from '../util/textUtil';
import { exec_query, select_query } from '../util/dbUtil';

/* NOTE 
    version, chatcheck 하나로 합치기
*/
export function db_drop_table(db) {
    return [
        exec_query(db, 'drop table metadata;', []),
        //exec_query(db, 'drop table version;', []),      // FIXME REMOVEME
        exec_query(db, 'drop table stock;', []),
        exec_query(db, 'drop table watch;', []),
        exec_query(db, 'drop table watch_stock;', []),
        exec_query(db, 'drop table std_disc;', []),
        exec_query(db, 'drop table disc;', []),
        //exec_query(db, 'drop table alert;', []),
        //exec_query(db, 'drop table chatcheck;', []),    // FIXME REMOVEME
        exec_query(db, 'drop table chat_room;', []),
        exec_query(db, 'drop table chat;', []),
        //exec_query(db, 'drop table message;', []),
    ]
}

export function db_create_table(db) {
    //drop_table(db);
    return [
        exec_query(db, 'create table if not exists metadata (' +
                       'stock_ver text, ' +
                       'std_disc_ver text, ' +
                       'last_chat_id text, ' +
                       'last_watch_id int, ' +
                       'last_simula_id text);'
        ),
        /*
        exec_query(db, 'create table if not exists version (' +
                       'stock_ver text, ' +
                       'std_disc_ver text);'
        ),
        */
        exec_query(db, 'create table if not exists stock (' +
                       'code,' +
                       'name text, ' +
                       'dname text); '
        ),
        exec_query(db, 'create table if not exists std_disc (' +
                       'std_disc_id integer primary key autoincrement, ' +
                       'category integer, ' + 
                       'seq integer, ' + 
                       'keyword text, ' +
                       'report_nm text, ' +
                       'report_dnm text); '
        ),
        exec_query(db, 'create table if not exists watch_stock (' +
                       'watch_id integer, ' +
                       'stock_code text); '
        ),
        exec_query(db, 'create table if not exists watch (' +
                       'watch_id integer primary key, ' +
                       'name text, ' +
                       'label text, ' +
                       'stock_codes text, ' +
                       'stock_names text, ' +
                       'std_disc_id integer);'
        ),
        exec_query(db, 'create table if not exists disc (' +
                       'disc_id integer primary key autoincrement, ' +
                       'watch_id int, ' +
                       'rcept_dt text, ' + 
                       'reg_time text, ' +
                       'corp_cls text, ' +
                       'corp_code text, ' +
                       'corp_name text, ' +
                       'stock_code text, ' +
                       'rcept_no text, ' +
                       'report_nm text, ' +
                       'flr_nm text, ' +
                       'rm text, ' + 
                       'tick integer, ' +
                       'content text, ' +
                       'url text);'
        ),
        /*
        exec_query(db, 'create table if not exists alert (' +
                       'id integer primary key autoincrement, ' +
                       'watch_id int, ' +
                       'last_disc_label text, ' +
                       'badge int, ' +
                       'update_time datetime); '
        ),
        */
        exec_query(db, 'create table if not exists chat_room (' +
                       'chat_room_id integer primary key autoincrement, ' +
                       'watch_id int, ' +
                       'last_label text, ' +
                       'badge int, ' +
                       'update_time datetime); '
        ),
        /*
        exec_query(db, 'create table if not exists chatcheck (' +
                       'chat_id text primary key);'
        ),
        */
        exec_query(db, 'create table if not exists chat (' +
                       'chat_id integer primary key autoincrement, ' +
                       'watch_id int, ' +
                       'chat_type int, ' +
                       'corp_code text, ' +
                       'corp_name text, ' +
                       'stock_code text, ' +
                       'report_nm text, ' +
                       'tick integer, ' +
                       'url text, ' +
                       'content text, ' +
                       'rcept_dt text, ' +
                       'reg_time text, ' +
                       'disc_id int, ' +
                       'update_time datetime); '
        ),

    ]
}

export function db_select_table(db) {
    return [
        select_query(db, 'select * from metadata;'),
        select_query(db, 'select * from stock;'),
        select_query(db, 'select * from std_disc;'),
        select_query(db, 'select a.*, b.name watch_name ' +
                         '  from chat_room a' +
                         '       ,watch b' +
                         ' where a.watch_id = b.watch_id' +
                         ' order by a.update_time desc;'
        ),
    ]
}

export function reset_stock(db, stocks) {
    exec_query(db, 'delete from stock;')
    stocks.map(stock => {
        exec_query(db, 'insert into stock(code, name, dname) values(?, ?, ?);', [stock.code, stock.name, stock.dname]);
    })
}

export function reset_std_disc(db, std_discs) {
    exec_query(db, 'delete from std_disc;')
    std_discs.map(std_disc => {
        exec_query(db, 'insert into std_disc(std_disc_id, category, seq, keyword, report_nm, report_dnm) values(?, ?, ?, ?, ?, ?);', [std_disc.std_disc_id, std_disc.category, std_disc.seq, std_disc.keyword, std_disc.report_nm, std_disc.report_dnm]);
    })
}

/*
export function update_soa(db, soa) {
    exec_query(db, 'update soa set stock = ? ,std_disc = ?, chat = ?;', [soa.stock, soa.std_disc, soa.chat])
}

export function insert_soa(db, soa) {
    exec_query(db, 'insert into soa(stock, std_disc, chat) values(?,?,?);', [soa.stock, soa.std_disc, soa.chat])
}
*/

export async function insert_disc(db, watch_id, disc) {
    const sql = 'insert into disc(watch_id, rcept_dt, reg_time, corp_cls, corp_code, corp_name, stock_code, rcept_no, report_nm, flr_nm, rm, tick, content, url ) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'

    const aaa = await exec_query(db, sql, [watch_id, disc['rcept_dt'], disc['reg_time'], disc['corp_cls'], disc['corp_code'], disc['corp_name'], disc['stock_code'], disc['rcept_no'], disc['report_nm'], disc['flr_nm'], disc['rm'], disc['tick'], disc['content'], disc['url']])
    return aaa
}

export function db_update_version(db, version) {
    exec_query(db, 'update metadata set stock_ver = ?, std_disc_ver = ?;', [version.stock_ver, version.std_disc_ver])
}

/* FIXME */
/*
export function insert_version(db, version) {
    exec_query(db, 'insert into version(stock_ver, std_disc_ver) values(?,?);', [version.stock_ver, version.std_disc_ver])
}

export function insert_chat_id(db, chat_id) {
    exec_query(db, 'insert into chatcheck(chat_id) values(?);', [chat_id])
}
*/
export function db_insert_metadata(db, metadata) {
    const { stock_ver, std_disc_ver, last_chat_id, last_watch_id, last_simula_id } = metadata

    exec_query(db, 'insert into metadata(stock_ver, std_disc_ver, last_chat_id, last_watch_id, last_simula_id) values(?,?,?,?,?);', [stock_ver, std_disc_ver, last_chat_id, last_watch_id, last_simula_id])
}

export function upsert_chat_room(db, watch_id, last_label) {
    let sql

    sql = 'select badge from chat_room where watch_id = ?'

    select_query(db, sql, [watch_id])
        .then(rst => {
            if (rst.length === 0) {
                sql = 'insert into chat_room(watch_id, last_label, badge, update_time ) values(?,?,?,datetime(\'now\'))'
                exec_query(db, sql, [watch_id, last_label, 1])
            } else {
                sql = 'update chat_room set last_label = ?, badge = ?, update_time = datetime(\'now\') where watch_id = ?'
                exec_query(db, sql, [last_label, rst[0].badge+1, watch_id])
            }
        })
}

export function insert_chat(db, chat) {
    const { watch_id, chat_type, rcept_dt, reg_time, corp_code, corp_name, stock_code, rcept_no, report_nm, tick, content, url } = chat

    const sql = 'insert into chat(watch_id, chat_type, corp_code, corp_name, stock_code, report_nm, tick, url, content, rcept_dt, reg_time) values(?,?,?,?,?,?,?,?,?,?,?)'

    exec_query(db, sql, [watch_id, chat_type, corp_code, corp_name, stock_code, report_nm, tick, url, content, rcept_dt, reg_time])
}

