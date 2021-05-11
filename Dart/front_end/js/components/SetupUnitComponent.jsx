import React from 'react';
import { View, Text, TextInput, Dimensions, TouchableOpacity, StyleSheet, FlatList } from 'react-native'
import { Badge, SearchBar, Button, Divider } from 'react-native-elements'
import Constants from 'expo-constants';
import { RecyclerListView, DataProvider, LayoutProvider } from "recyclerlistview";
import { Feather } from 'react-native-vector-icons';
import { findText, getDisassembled } from '../util/textUtil';

const SCREEN_WIDTH = Dimensions.get("window").width;

class SetupUnitComponent extends React.Component {
    constructor(props) {
        super(props);

        this.searchStdDisc = this.searchStdDisc.bind(this)
        this.handleSelectStdDisc = this.handleSelectStdDisc.bind(this)
        this.handleDeselectStdDisc = this.handleDeselectStdDisc.bind(this)

        this._rowRenderer = this._rowRenderer.bind(this);
        this.renderSelectedStdDisc = this.renderSelectedStdDisc.bind(this)
        this.renderUnitDetail = this.renderUnitDetail.bind(this)

        this.onFocus = this.onFocus.bind(this)

        this._layoutProvider = new LayoutProvider(
            index => {
                return 0;
            },
            (type, dim) => {
                dim.width = SCREEN_WIDTH;
                dim.height = 35;
            }
        );

        const dataProvider = new DataProvider((r1, r2) => { return r1 !== r2; })

        this.state = {
            placeholder: 'Search Discs...',
            value: '',
            visibleDetail: false,
            selectedDisc: '',
            dataProvider: dataProvider.cloneWithRows(this.props.std_discs)
        };
    }

    componentDidUpdate(prevProps) {
        const { std_discs } = this.props

        if (prevProps.std_discs === std_discs) {
            return
        }
        const dataProvider=this.state.dataProvider.cloneWithRows(std_discs)

        this.setState({ dataProvider })
    }

    searchStdDisc(value) {
        const std_discs = this.props.std_discs.filter( std_disc =>
            findText(std_disc.report_dnm, value) > -1
        );

        const dataProvider = this.state.dataProvider.cloneWithRows(std_discs)

        if (std_discs.length > 0) {
            this.setState({ value, dataProvider })
        } else {
            this.setState({ value })
        }
    }

    handleSelectStdDisc(newStdDisc) {
        const std_discs = this.props.std_discs.filter( std_disc =>
            findText(std_disc.report_nm, this.state.value) > -1
         && std_disc.id !== newStdDisc.id
        );

        const dataProvider = this.state.dataProvider.cloneWithRows(std_discs)

        this.setState({ dataProvider, visibleDetail:true, selectedDisc:newStdDisc })
        this.props.handleUnitStdDisc(newStdDisc)
    }

    onFocus() {
        this.setState({ visibleDetail:false })
    }

    handleDeselectStdDisc(delStdDisc) {
        this.props.handleUnitStdDisc(null)
        this.onFocus()
        const dataProvider=this.state.dataProvider.cloneWithRows(this.props.std_discs)
        this.setState({ dataProvider, visibleDetail:false })
    }

    _rowRenderer(type, item, index, extendedState) {
        return (
            <View style ={{ alignItems: 'flex-start' }} >
                <Button
                    titleStyle={{marginLeft:5}}
                    type = "clear"
                    title = {item.report_nm}
                    onPress={() => this.handleSelectStdDisc(item)}
                    icon = { <Feather size={15} name="square" /> }
                />
            </View>
        )
    }

    renderSelectedStdDisc( {item} ) {
        return (
            <Button
                buttonStyle={{borderRadius:25, marginLeft:10}}
                titleStyle={{marginLeft:5}}
                type  = "outline"
                title = {item.report_nm}
                icon  = { <Feather size={15} name="x-circle" /> }
                onPress={() => this.handleDeselectStdDisc(item)}
            />
        )
    }

    renderUnitDetail() {
        console.log('renderUnitDetail', this.state.selectedDisc)
        switch (this.state.selectedDisc.id) {
            /* #1.지분공시  */
            case 1: /* 임원ㆍ주요주주특정증권등소유상황보고서 */
                return <></>
            case 2: /* 주식등의대량보유상황보고서 */
                return <></>
            case 3: /* 공개매수신고서 */
                return <></>

            /* #2.주요사항보고  */
            case 3: /* 공개매수신고서 */
                return <></>
            case 4: /* 자기주식취득결정 */
                return <></>
            case 5: /* 자기주식취득신탁계약체결결정 */
                return <></>
            case 6: /* 타법인주식 및 출자증권 취득/처분/양수/양도 결정 */
                return <></>
            case 7: /* 유상/무상증자 결정 */
                return <></>
            case 8: /* 감자결정 */
                return <></>
            case 9: /* 전환사채권 발행결정 */
                return <></>
            case 10: /* 주권관련 사채권 양도/양수 결정 */
                return <>
                </>
            case 11: /* 회사 분할/합병 결정 */
            /*
                    계약금액
                    최근매출
                    매출대비
                    */
                return (
                    <View>
                    <Text>계약금액:</Text>
                    <TextInput value={this.state.name}/>
                    <Text>최근매츨:</Text>
                    <TextInput value={this.state.name}/>
                    <Text>매츨대비:</Text>
                    <TextInput value={this.state.name}/>
                    </View>
                )
            case 12: /* 유형자산 양수/양도 결정 */
                return <></>
            case 13: /* 영업 양수/양도 결정 */
                return <></>
            case 14: /* 신주인수권부사채권발행결정 */
                return <></>
            case 15: /* 교환사채권발행결정 */
                return <></>

            /* #3.정기공시  */
            case 16: /* 사업보고서 */
                return <></>
            case 17: /* 분기보고서 */
                return <></>
            case 18: /* 반기보고서 */
                return <></>

            /* #4.거래소 공시  */
            case 19: /* 단일판매ㆍ공급계약체결 */
                return <></>
            case 20: /* 최대주주등 소유주식 변동 신고서 */
                return <></>
            case 21: /* 감사보고서 제출 */
                return <></>
            case 22: /* 자산재평가 */
                return <></>

            case 23: /* 조회공시 */
                return <></>
            case 24: /* 최대주주변경 */
                return <></>
            default:
                return <></>

        }
        return <></>
    }
    render() {
        return (
            <>
                {this.props.unitStdDisc &&
                    <View style={{ height:'6%' }} >
                        <FlatList
                            data = {[this.props.unitStdDisc]}
                            horizontal
                            keyExtractor={item=>item.std_disc_id.toString()}
                            renderItem = {this.renderSelectedStdDisc}
                        />
                    </View>
                }
                <SearchBar
                    placeholder={this.state.placeholder}
                    onChangeText={this.searchStdDisc}
                    value={this.state.value}
                    onFocus={this.onFocus}
                    platform='ios'
                />
                {!this.state.visibleDetail &&
                  this.state.dataProvider._size > 0 &&
                <RecyclerListView
                    layoutProvider={this._layoutProvider}
                    dataProvider={this.state.dataProvider}
                    rowRenderer={this._rowRenderer}
                    style={{ flex:1 }}
                />
                }
                {this.state.visibleDetail &&
                 this.renderUnitDetail()
                }
            </>
        )
    }
}

const styles = StyleSheet.create({
    container: {
        backgroundColor: '#fff',
        justifyContent: 'center',
        flex:1,
    },
    flexRow: {
        flex:1,
        flexDirection: 'row',
        alignItems:'flex-start',
    },
    container2: {
        backgroundColor: '#fff',
        justifyContent: 'center',
        height:100
    },
})

export default SetupUnitComponent;
