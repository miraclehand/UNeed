export function exec_query(db, sql, params = []) {
    return new Promise((resolve, reject) => {
        db.transaction(tx => {
            tx.executeSql(sql,
                params,
                (_, {rows:{_array}}) => {
                    return resolve(_array);
                }, (t, error) => {
                    alert(error)
                    return resolve(null);
                }
            );
        })
    });
}

export function select_query(db, sql, params = []) {
    return new Promise((resolve, reject) => {
        db.transaction((tx) => {
            tx.executeSql(sql, params, (tx, results) => {
                const { rows } = results;
                let values = [];

                for (let i = 0; i < rows.length; i++) {
                    values.push({
                        ...rows.item(i),
                    });
                }
                resolve(values)
            },
            (error) => {
                reject(error);
            });
        });
    });
}

