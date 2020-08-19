export function initDB(db) {
    /*
    alert('initDB')
    db.transaction(tx => {
        tx.executeSql("drop table disc",
            [],
            (_,{rows})=> {
            }, (t, error) => {
                alert('error.. drop table disc=>' + error)
            }
        )
    })
    db.transaction(tx => {
        tx.executeSql( "drop table alert",
            [],
            (_,{rows})=> {
            }, (t, error) => {
                alert('error.. drop table alert=>' + error)
            }
        )
    })
    */

    db.transaction(tx => {
        tx.executeSql(
            "create table if not exists watch_list (" +
                "_id integer primary key autoincrement, " +
                "keyword text, " +
                "stock_code text, " +
                "stock_name text);",
            [],
            (_,{rows})=> {
            }, (t, error) => {
                alert('error.. create watch_list=>' + error)
            }
        );
    });
    db.transaction(tx => {
        tx.executeSql(
            "create table if not exists disc (" +
                "_id integer primary key autoincrement, " +
                "rcept_dt text, " + 
                "reg_time text, " +
                "corp_cls text, " +
                "corp_code text, " +
                "corp_name text, " +
                "stock_code text, " +
                "rcept_no text, " +
                "report_nm text, " +
                "flr_nm text, " +
                "rm text, " + 
                "tick integer, " +
                "content text, " +
                "url text);",
            [],
            (_,{rows})=> {
            }, (t, error) => {
                alert('error.. create corp)' + error)
            }
        );
    });
    db.transaction(tx => {
        tx.executeSql(
            "create table if not exists alert (" +
                "_id integer primary key autoincrement, " +
                "watch_list_id int, " +
                "last_disc_id int, " +
                "foreign key(watch_list_id) references watchlist(_id), " +
                "foreign key(last_disc_id) references disc(_id));",
            [],
            (_,{rows})=> {
            }, (t, error) => {
                alert('error.. create alert)' + error)
            }
        );
    });
}

