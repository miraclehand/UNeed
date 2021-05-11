import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';
import { requestWatch, requestDeleteWatch } from '../actions/WatchAction';
import WatchComponent from '../components/WatchComponent';
import { Text, TextInput, Button } from 'react-native';
import { Vibration } from 'react-native';
//import { signOutAsync, getCachedUserAsync } from '../init/InitUser';
import { signOut  } from '../actions/UserAction';
import { deleteAuthState  } from '../device/user';
import { db_drop_table, db_create_table  } from '../device/db';

//import { setUser } from '../actions/UserAction';
import { requestCandle } from '../actions/CandleAction';
//import { upsertAlertRoom } from '../actions/AlertRoomAction';
//import { upsertAlert } from '../actions/AlertAction';
//import { upsertChatRoom } from '../actions/ChatRoomAction';
import { requestPutChatCheck } from '../actions/ChatAction';
//import { receiveMessage } from '../actions/MessageAction';

import { requestPostWatch } from '../actions/WatchAction';

import { incBadge, clrBadge } from '../actions/BadgeAction';

import { exec_query, select_query } from '../util/dbUtil';


import * as WebBrowser from 'expo-web-browser';
import * as Google from 'expo-auth-session/providers/google';

WebBrowser.maybeCompleteAuthSession();

export class Connected extends React.Component {
    constructor(props) {
        super(props)

        this.handlePress  = this.handlePress.bind(this)
        this.handleDelete = this.handleDelete.bind(this)

        this.select_ver = this.select_ver.bind(this)
        this.select_watch1 = this.select_watch1.bind(this)
        this.select_watch2 = this.select_watch2.bind(this)
        this.select_watch3 = this.select_watch3.bind(this)
        this.select_watch4 = this.select_watch4.bind(this)
        this.logout = this.logout.bind(this)
        this.insert_watch = this.insert_watch.bind(this)
        this.select_std_disc= this.select_std_disc.bind(this)
        this.select_chat_room= this.select_chat_room.bind(this)
        this.select_chat= this.select_chat.bind(this)
        this.clear_chat_room= this.clear_chat_room.bind(this)
        this.select_chat_id= this.select_chat_id.bind(this)
        this.upd_chatcheck= this.upd_chatcheck.bind(this)
        this.clr = this.clr.bind(this)
        this.noti1 = this.noti1.bind(this)
        this.noti2 = this.noti2.bind(this)
        this.clear_db = this.clear_db.bind(this)
        //const [request, response, promptAsync] = Google.useAuthRequest({
        /*
        let aa=
        Google.useAuthRequest({
            expoClientId: '536908281748-teiiu4iu80p3romorrcj90pivgkbvkev.apps.googleusercontent.com',
            iosClientId: '536908281748-n5190ntbccf3gklu3f7h4im226edbjpc.apps.googleusercontent.com',
            androidClientId: '536908281748-jjtno1de0mpknm2nohh594o7q2oiasa5.apps.googleusercontent.com',
            webClientId: '536908281748-iut4mcukcfn8agn19iu2ioiqpfu2gces.apps.googleusercontent.com',
        //    scopes: ['openid', 'profile', 'email'],
        });
        */
         this.state = {
            name : ""
        }

    }

    componentDidMount() {
        const {os, db, dbName, email, token, cntry } = this.props

        this.props.requestWatch(os, db, email, token, cntry);
        //alert(response)
/*
        if (this.response?.type === 'success') {
            const { authentication } = response;
        }
        */
        //const json = '{"result":true, "count":42}';
        //const obj = JSON.parse(json);

        //console.log(JSON.stringify(obj));
    }

    handlePress() {
    /*
        (async () => {
            await signOutAsync(this.props.authState);
            const user = await getCachedUserAsync()
            this.props.setUser(user);
        }
        )()
        */
    }

    handleDelete(watch) {
        const {os, db, dbName, email, token, cntry } = this.props

        this.props.requestDeleteWatch(os, db, email, token, cntry, watch);
    }

    select_ver() {
        alert('select_ver')
        select_query(this.props.db, 'select * from version;')
            .then(version => {
                    alert(version[0].stock_ver)
                }
            )
    }
    upd_chatcheck() {
        const {os, db, email, token, cntry, chat_id } = this.props
        this.props.requestPutChatCheck(os, db, email, token, cntry, chat_id)
    }
    select_watch1() {
        alert('select_watch1')
        select_query(this.props.db, 'select * from watch;')
            .then(watch => {
                    alert(JSON.stringify(watch))
                }
            )
    }
    select_watch2() {
        alert('select_watch2')
        const {os, db, dbName, email, token, cntry } = this.props

        this.props.requestWatch(os, db, email, token, cntry);
    }

    select_watch3() {
        alert('select_watch3')
        const sql = 'select a.*, b.std_disc_id, b.report_nm std_disc_report_nm, b.report_dnm std_disc_report_dnm from watch a, std_disc b where a.std_disc_id = b.std_disc_id order by a.watch_id;'

        select_query(this.props.db, sql)
            .then(watch => {
                    alert(JSON.stringify(watch))
                    //alert('[' + watch[watch.length - 1].watch_id + ']' + watch[watch.length - 1].name)
                }
            )
    }
    select_watch4() {
        alert('select_watch4')
        const {watchs } = this.props
        alert(JSON.stringify(watchs))
    }
    clear_chat_room() {
        alert('clear_chat_room')
        exec_query(this.props.db, 'delete from chat_room;')
        exec_query(this.props.db, 'delete from chat;')
    }
    select_chat_room() {
        alert('select_chat_room')
        select_query(this.props.db, 'select * from chat_room;')
            .then(chat_room => {
                alert(JSON.stringify(chat_room))
            })
        select_query(this.props.db, 'select a.*, b.name watch_name ' +
                                    '  from chat_room a' +
                                    '      ,watch b' +
                                    ' where a.watch_id = b.watch_id' +
                                    ' order by a.update_time desc;')
            .then(chat_room => {
                alert(JSON.stringify(chat_room))
            })
    }
    select_chat_id() {
        alert('select_chat_id')
        select_query(this.props.db, 'select * from chatcheck;')
            .then(chat_id => {
                alert(JSON.stringify(chat_id))
            })
    }
    select_chat() {
        alert('select_chat')
        select_query(this.props.db, 'select * from chat;')
            .then(chat => {
                alert(JSON.stringify(chat))
            })
    }

    select_std_disc() {
        alert('select_std_disc')
        select_query(this.props.db, 'select * from std_disc;')
            .then(std_disc => {
                alert(JSON.stringify(std_disc))
            })
    }
    clear_db() {
        this.props.db_drop_table(this.props.db)
    }

    logout() {
        this.props.signOut()
        deleteAuthState()
    }
    insert_watch() {
        const {os, db, email, token, cntry } = this.props
        const stocks = [{code:'005930'},{code:'000270'}]
        let newWatch1 = { id:1, name: 'watch_name1', stocks: stocks, label: 'label1', stock_codes: '005930,000270', stock_names: '삼성전자,기아차', std_disc: {id: 1, report_nm: '단일판매 공급계약1', report_dnm: '단일판매 공급계약11'} }
        let newWatch2 = { id:2, name: 'watch_name2', stocks: stocks, label: 'label2', stock_codes: '005930,000270', stock_names: '삼성전자,기아차', std_disc: {id: 1, report_nm: '단일판매 공급계약2', report_dnm: '단일판매 공급계약22'} }

        this.props.requestPostWatch(os, db, email, token, cntry, newWatch1)
        this.props.requestPostWatch(os, db, email, token, cntry, newWatch2)
        //this.props.incBadge(this.state.name)
    }
    clr() {
        const {os, db, email, token, cntry } = this.props
        const stocks = [{code:'352820'},{code:'095610'}]
        const newWatch = { id:2, name: 'watch_name2', stocks: stocks, label: 'label2', stock_codes: '352820,095610', stock_names: '빅히트,테스',  std_disc_id: {id:2, report_nm: '대주주변경1', report_dnm: '대주주변경2'} }

        this.props.requestPostWatch(os, db, email, token, cntry, newWatch)
        //this.props.clrBadge(this.state.name)
    }
    noti1() {
        Vibration.vibrate();
        const _watch_id = 1 //this.state.name
        const _disc = {rcept_dt:'2021-01-13', reg_time:'12:20', corp_code:'00593', corp_name:'삼성전자', stock_code:'005930', rcept_no: 'rcept_no:1', report_nm: '리리리포포포트트트1',  flr_nm:'flr_nm', rm:'rm', tick:1234, content:'코코코코코코코1',url:'http://url.com'}
        const data = { 'watch_id': _watch_id, 'disc': _disc }
        const watch_id = data['watch_id']
        const disc     = data['disc']
        //this.props.incBadge(watch_id)
        const last_label =  disc['report_nm']
        const chat = {rcept_dt:'2021-01-13', reg_time:'12:20', corp_code:'00593', corp_name:'삼성전자', stock_code:'005930', rcept_no: 'rcept_no:1', report_nm: '리리리포포포트트트1',  flr_nm:'flr_nm', rm:'rm', tick:1234, content:'코코코코코코코1',url:'http://url.com'}
        //this.props.upsertChatRoom(this.props.db, watch_id, last_label)
        //this.props.receiveMessage(this.props.db, watch_id, disc)
        //this.props.upsertChat(this.props.db, watch_id, chat)
    }
    noti2() {
        Vibration.vibrate();
        const _watch_id = 2 //this.state.name
        const _disc = {rcept_dt:'2021-01-13', reg_time:'12:20', corp_code:'00593', corp_name:'삼성전자', stock_code:'005930', rcept_no: 'rcept_no:1', report_nm: '리리리포포포트트트2',  flr_nm:'flr_nm', rm:'rm', tick:1234, content:'코코코코코코코2',url:'http://url.com'}
        const data = { 'watch_id': _watch_id, 'disc': _disc }
        const watch_id = data['watch_id']
        const disc     = data['disc']
        //this.props.incBadge(watch_id)
        const last_label =  disc['report_nm']
        const chat = {rcept_dt:'2021-01-13', reg_time:'12:20', corp_code:'00593', corp_name:'삼성전자', stock_code:'005930', rcept_no: 'rcept_no:1', report_nm: '리리리포포포트트트1',  flr_nm:'flr_nm', rm:'rm', tick:1234, content:'코코코코코코코1',url:'http://url.com'}
        //this.props.upsertChatRoom(this.props.db, watch_id, last_label)
        //this.props.receiveMessage(this.props.db, watch_id, disc)
        //this.props.upsertChat(this.props.db, watch_id, chat)
    }
    render() {
        const { os, watchs } = this.props

        return (
        <>
                <WatchComponent
                    os={os}
                    watchs={watchs}
                    navigation={this.props.navigation}
                    rooms={this.props.rooms}
                    handleDelete={this.handleDelete}
                />
                {/*
                <Button title='SelectChatRoom' onPress={this.select_chat_room}/>
                <Button title='SelectWatch1' onPress={this.select_watch1} />
                <Button title='SelectChatid' onPress={this.select_chat_id} />
                <Button title='SelectStdDisc' onPress={this.select_std_disc} />
                <Button title='SelectStock' onPress={this.select_std_disc} />
                <Button title='SelectVersion' onPress={this.select_ver} />
                <Button title='Logout' onPress={this.logout} />
                */}
                {/*
                <Button title='SelectWatch2' onPress={this.select_watch2} />
                <Text> {this.props.count} </Text>
                <Text> {JSON.stringify(this.props.badges, null, 2)} </Text>
                <TextInput value={this.state.name}
                    onChangeText={text => this.setState({name:text})}
                />
                <Button title='ChtCheck' onPress={this.chatcheck} />
                <Button title='PutChtCheck' onPress={this.upd_chatcheck} />
                <Button title='SelectChat' onPress={this.select_chat} />
                <Button title='SelectWatch3' onPress={this.select_watch3} />
                <Button title='SelectWatch4' onPress={this.select_watch4} />
                <Button title='InsertWatch' onPress={this.insert_watch} />
                <Button title='RECV_NOTI1' onPress={this.noti1} />
                <Button title='RECV_NOTI2' onPress={this.noti2} />
                <Button title='ClearChatRoom' onPress={this.clear_chat_room} />
                <Button title='ClearDB' onPress={this.clear_db} />
                */}
        </>
        )
                //<Button title='SignOut' onPress={this.handlePress} />
   }
}

function mapStateToProps (state) {
    return {
        email: state.userReducer.email,
        authState: state.userReducer.authState,
        pushToken: state.userReducer.pushToken,
        os: state.baseReducer.os,
        db: state.dbReducer.db,
        chat_id: state.dbReducer.chat_id,
        dbName: state.dbReducer.dbName,
        cntry: state.baseReducer.cntry,
        watchs: state.watchReducer.watchs,
        candleState: state.candleReducer,
        //count: state.badgeReducer.count,
        //badges: state.badgeReducer.badges,
        rooms: state.chatRoomReducer.rooms,
        navigation: state.baseReducer.navigation,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        //setUser      : bindActionCreators(setUser, dispatch),
        requestWatch : bindActionCreators(requestWatch,  dispatch),
        requestDeleteWatch: bindActionCreators(requestDeleteWatch, dispatch),
        requestCandle: bindActionCreators(requestCandle, dispatch),
        signOut: bindActionCreators(signOut, dispatch),
        incBadge: bindActionCreators(incBadge, dispatch),
        clrBadge: bindActionCreators(clrBadge, dispatch),
        //upsertChatRoom: bindActionCreators(upsertChatRoom, dispatch),
        //upsertChat: bindActionCreators(upsertChat, dispatch),
        requestPostWatch: bindActionCreators(requestPostWatch, dispatch),
        //receiveMessage: bindActionCreators(receiveMessage, dispatch),
        requestPutChatCheck: bindActionCreators(requestPutChatCheck, dispatch),
//        receiveNotification : bindActionCreators(receiveNotification, dispatch),
        db_drop_table: bindActionCreators(db_drop_table, dispatch),
        db_create_table: bindActionCreators(db_create_table, dispatch),
    };
}

const WatchContainer = connect(mapStateToProps, mapDispatchToProps)(Connected);
export default WatchContainer;
