import React from 'react';
import MessagesContainer from '../containers/MessagesContainer';

export class MessagesScreen extends React.Component {
    constructor(props) {
        super(props)
    }

componentDidMount() {
        console.log('componentDidMount')
/*
  db.transaction(tx => {
        tx.executeSql(
          'CREATE TABLE IF NOT EXISTS contents (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, picture TEXT, user_id INTEGER, user_name TEXT, user_pic TEXT);'
        );
        tx.executeSql(
          'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, picture TEXT);'
        );
      });
*/
/*
    db.transaction (
        tx => {
      tx.executeSql('INSERT INTO contents (content, picture, user_id, user_name, user_p)')
        }
    )
*/
}
    render () {
        return (
            <MessagesContainer />
        )
    }
}

export default MessagesScreen
