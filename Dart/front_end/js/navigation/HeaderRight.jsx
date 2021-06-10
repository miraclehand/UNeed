import React from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux';

import { View, Text, Button, TouchableOpacity } from 'react-native';
import { Icon } from 'react-native-elements'
import { MaterialCommunityIcons } from 'react-native-vector-icons';

import { initUnit } from '../actions/UnitAction';
import { exec_query, select_query } from '../util/dbUtil';
import { requestPostWatch } from '../actions/WatchAction';
import { requestPostSimula } from '../actions/SimulaAction';

class Connected extends React.Component {
    constructor(props) {
        super(props);
        
        this.handleCheck        = this.handleCheck.bind(this)
        this.handleWatchPress   = this.handleWatchPress.bind(this)
        this.handleSimulaPress  = this.handleSimulaPress.bind(this)
        this.getWatchFontWeight = this.getWatchFontWeight.bind(this)
        this.getSimulaFontWeight= this.getSimulaFontWeight.bind(this)

    }

    handleCheck(route_name) {
        if (route_name === 'CreateWatch') {
            if (!this.props.unitState.name) {
                alert('이름을 입력하세요.');
                return false
            }
            if (this.props.unitState.stocks.length === 0) {
                alert('종목을 선택하세요.');
                return false
            }
        }
        if (route_name === 'CreateSimula') {
            if (!this.props.unitState.name) {
                alert('이름을 입력하세요.');
                return false
            }
            if (!this.props.unitState.s_date) {
                alert('시작일자를 선택하세요.');
                return false
            }
            if (!this.props.unitState.e_date) {
                alert('종료일자를 선택하세요.');
                return false
            }
            if (this.props.unitState.stocks.length === 0) {
                alert('종목을 선택하세요.');
                return false
            }
        }
        if (route_name === 'SetupWatch') {
            if (!this.props.unitState.std_disc) {
                alert('공시를 선택 입력하세요.');
                return false
            }
        }
        return true
    }

    handleWatchPress() {
        const { metadata, watchs, route_name, navigation } = this.props

        if (!this.handleCheck(route_name)) return

        if (route_name === 'Watch') {
            this.props.initUnit(metadata.last_watch_id)
            navigation.navigate('CreateWatch')
        }
        if (route_name === 'CreateWatch') {
            navigation.navigate('SetupWatch')
        }
        if (route_name === 'SetupWatch') {
            const { os, db, email, token, cntry, unitState } = this.props
            const { requestPostWatch } = this.props

            //alert(JSON.stringify(unitState))
            requestPostWatch(os, db, email, token, cntry, unitState)
            navigation.navigate('Watch')

            /*
            const { name, stocks, std_disc, stock_codes, stock_names } = unitState
            let sql
            sql = 'insert into watch(name, label, stock_codes, stock_names, std_disc_id) values(?,?,?,?,?);',
            exec_query(db, sql, [name, stock_names, stock_codes, stock_names, std_disc.id]).then( (watch) => {
                unitState.id = watch.watch_id
            })
            */

        }
    }

    handleSimulaPress() {
        const { metadata, simulas, route_name, navigation } = this.props

        if (!this.handleCheck(route_name)) return

        if (route_name === 'Simula') {
            this.props.initUnit(metadata.last_simula_id)
            navigation.navigate('CreateSimula')
        }
        if (route_name === 'CreateSimula') {
            navigation.navigate('SetupSimula')
        }
        if (route_name === 'SetupSimula') {
            const { os, db, email, token, cntry, unitState, simula} = this.props
            const { requestPostSimula } = this.props

            console.log('unitStat', unitState)
            console.log('simula', simula)
            requestPostSimula(os, db, email, token, cntry, unitState)
            //navigation.navigate('StatsSimula', {'simula': simula})
            navigation.navigate('Simula')
        }
    }

    getWatchFontWeight(route_name) {
        if (route_name === 'CreateWatch') {
            if (!this.props.unitState.name) {
                return 'normal'
            }
            if (this.props.unitState.stocks.length === 0) {
                return 'normal'
            }
            return 'bold'
        }
        if (route_name === 'SetupWatch') {
            if (!this.props.unitState.std_disc) {
                return 'normal'
            }
            return 'bold'
        }
    }

    getSimulaFontWeight(route_name) {
        if (route_name === 'CreateSimula') {
            if (!this.props.unitState.name) {
                return 'normal'
            }
            if (!this.props.unitState.s_date) {
                return 'normal'
            }
            if (!this.props.unitState.e_date) {
                return 'normal'
            }
            if (this.props.unitState.stocks.length === 0) {
                return 'normal'
            }
            return 'bold'
        }
        if (route_name === 'SetupSimula') {
            if (!this.props.unitState.std_disc) {
                return 'normal'
            }
            return 'bold'
        }
    }

    render() {
        const { route_name, navigation } = this.props
        const { handleWatchPress,  getWatchFontWeight  } = this
        const { handleSimulaPress, getSimulaFontWeight } = this

        if (route_name === 'Watch') {
            return (
                <View style = {styles.container} >
                {/*
                    <Icon name = 'magnify' size={30} type='material-community'
                        onPress={() => alert('this this')}
                    />
                    */}
                    <Icon name = 'plus-circle' size={30} type='material-community'
                        onPress={handleWatchPress}
                    />
                </View>
            )
        }
        if (route_name === 'CreateWatch') {
            const fontWeight = getWatchFontWeight(route_name)
            return (
                <TouchableOpacity onPress={handleWatchPress} >
                    <Text style = {{ fontWeight:fontWeight }}> Next </Text>
                </TouchableOpacity>
            )
        }
        if (route_name === 'SetupWatch') {
            const fontWeight = getWatchFontWeight(route_name)
            return (
                <TouchableOpacity onPress={handleWatchPress} >
                    <Text style = {{ fontWeight:fontWeight }}> Create </Text>
                </TouchableOpacity>
            )
        }
        if (route_name === 'Simula') {
            return (
                <View style = {styles.container} >
                    <Icon name = 'magnify' size={30} type='material-community'
                        onPress={() => alert('this this')}
                    />
                    <Icon name = 'eye-plus' size={30} type='material-community'
                        onPress={handleSimulaPress}
                    />
                </View>
            )
        }
        if (route_name === 'CreateSimula') {
            const fontWeight = getSimulaFontWeight(route_name)
            return (
                <TouchableOpacity onPress={handleSimulaPress} >
                    <Text style = {{ fontWeight:fontWeight }}> Next </Text>
                </TouchableOpacity>
            )
        }
        if (route_name === 'SetupSimula') {
            const fontWeight = getSimulaFontWeight(route_name)
            return (
                <TouchableOpacity onPress={handleSimulaPress} >
                    <Text style = {{ fontWeight:fontWeight }}> Create </Text>
                </TouchableOpacity>
            )
        }
        return (
            <></>
        )
    }
}

const styles = {
    container: {
        flexDirection:'row',
        justifyContent:'flex-end',
        alignItems:'center'
    }
}

function mapStateToProps (state) {
    return {
        os: state.baseReducer.os,
        db: state.dbReducer.db,
        cntry: state.baseReducer.cntry,
        email: state.userReducer.email,
        metadata: state.dbReducer.metadata,
        watchs: state.watchReducer.watchs,
        simulas: state.simulaReducer.simulas,
        unitState: state.unitReducer,
        simula: state.simulaReducer.simula,
    };
};

function mapDispatchToProps (dispatch) {
    return {
        initUnit: bindActionCreators(initUnit, dispatch),
        requestPostWatch: bindActionCreators(requestPostWatch, dispatch),
        requestPostSimula: bindActionCreators(requestPostSimula, dispatch),
    };
}

const HeaderRight = connect(mapStateToProps, mapDispatchToProps)(Connected);

export default HeaderRight
