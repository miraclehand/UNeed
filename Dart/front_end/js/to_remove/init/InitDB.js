import { getDisassembled } from '../util/textUtil';
import { exec_query, select_query } from '../util/dbUtil';

/* db: std_disc, disc, unit, simula */
/*
export function initDB(db) {
    //drop_table(db);
    create_table(db);
    //alert(server_version.stock_version)
}
*/

function drop_table(db) {
    exec_query(db, 'drop table version;', []);
    exec_query(db, 'drop table stock;', []);
    exec_query(db, 'drop table watch;', []);
    exec_query(db, 'drop table watch_stock;', []);
    exec_query(db, 'drop table std_disc;', []);
    exec_query(db, 'drop table disc;', []);
    exec_query(db, 'drop table alert;', []);
}

export function create_table(db) {
        //drop_table(db);
    exec_query(db, 'create table if not exists version (' +
                   'stock_ver text, ' +
                   'std_disc_ver text);'
    );
    exec_query(db, 'create table if not exists stock (' +
                   'code,' +
                   'name text, ' +
                   'dname text); '
    );
    exec_query(db, 'create table if not exists std_disc (' +
                   'id integer primary key autoincrement, ' +
                   'report_nm text, report_dnm text);'
    );
    exec_query(db, 'create table if not exists watch_stock (' +
                   'id integer, ' +
                   'stock_code text); '
    );
    exec_query(db, 'create table if not exists watch (' +
                   'id integer primary key, ' +
                   'name text, ' +
                   'label text, ' +
                   'stock_codes text, ' +
                   'stock_names text, ' +
                   'std_disc_id integer);'
    );
    exec_query(db, 'create table if not exists disc (' +
                   'id integer primary key autoincrement, ' +
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
    );
    exec_query(db, 'create table if not exists alert (' +
                   'id integer primary key autoincrement, ' +
                   'watch_id int, ' +
                   'room_id int, ' +
                   'last_disc_label text, ' +
                   'update_time datetime); '
    );
}

/*
function init_std_disc(db) {
    // # 1.지분공시
    insert_std_disc(db, '임원ㆍ주요주주특정증권등소유상황보고서')
    insert_std_disc(db, '주식등의대량보유상황보고서')
    insert_std_disc(db, '공개매수신고서')

    // # 2.주요사항보고
    insert_std_disc(db, '자기주식취득결정')
    insert_std_disc(db, '자기주식취득신탁계약체결결정')
    insert_std_disc(db, '타법인주식 및 출자증권 취득/처분/양수/양도 결정')
    insert_std_disc(db, '유상/무상증자 결정')
    insert_std_disc(db, '감자결정')
    insert_std_disc(db, '전환사채권 발행결정')
    insert_std_disc(db, '주권관련 사채권 양도/양수 결정')
    insert_std_disc(db, '회사 분할/합병 결정')
    insert_std_disc(db, '유형자산 양수/양도 결정')
    insert_std_disc(db, '영업 양수/양도 결정')
    insert_std_disc(db, '신주인수권부사채권발행결정')
    insert_std_disc(db, '교환사채권발행결정')

    // 3.정기공시
    insert_std_disc(db, '사업보고서')
    insert_std_disc(db, '분기보고서')
    insert_std_disc(db, '반기보고서')

    // 4.거래소 공시
    insert_std_disc(db, '단일판매ㆍ공급계약체결')
    insert_std_disc(db, '최대주주등 소유주식 변동 신고서')
    insert_std_disc(db, '감사보고서 제출')
    insert_std_disc(db, '자산재평가')

    insert_std_disc(db, '조회공시')
    insert_std_disc(db, '최대주주변경')
}

function insert_std_disc(db, report_nm) {
    const report_dnm = getDisassembled(report_nm)

    exec_query(db, 'insert into std_disc(report_nm,report_dnm) values(?,?);',
        [report_nm, report_dnm]
    )
}
*/
/*
function insert_stock(db, stock_code, stock_name) {
    exec_query(db, 'insert into stock(stock_code,stock_name) values(?,?);',
        [stock_code, stock_name]
    )
}

function init_stock(db) {
    insert_stock(db, '000000', '전체')
    insert_stock(db, '005930', '삼성전자')
    insert_stock(db, '000660', 'SK하이닉스')
    insert_stock(db, '000270', '기아차')
}
*/
