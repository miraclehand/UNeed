import React, { Component } from "react";
import {StyleSheet, Text, View, Dimensions, TouchableHighlight} from 'react-native';
import { RecyclerListView, DataProvider, LayoutProvider } from "recyclerlistview";
import BubbleComponent from './BubbleComponent';

const ViewTypes = {
    SIMPLE_ROW: 0,
};

const SCREEN_WIDTH = Dimensions.get("window").width;

class AlertRoomComponent extends React.Component {
    constructor(props) {
        super(props);

        //Create the data provider and provide method which takes in two rows of data and return if those two are different or not.
        //THIS IS VERY IMPORTANT, FORGET PERFORMANCE IF THIS IS MESSED UP
        let dataProvider = new DataProvider((r1, r2) => {
            return r1 !== r2;
        });

        //Create the layout provider
        //First method: Given an index return the type of item e.g ListItemType1, ListItemType2 in case you have variety of items in your list/grid
        //Second: Given a type and object set the exact height and width for that type on given object, if you're using non deterministic rendering provide close estimates
        //If you need data based check you can access your data provider here
        //You'll need data in most cases, we don't provide it by default to enable things like data virtualization in the future
        //NOTE: For complex lists LayoutProvider will also be complex it would then make sense to move it to a different file
        this._layoutProvider = new LayoutProvider(
            index => {
                return ViewTypes.SIMPLE_ROW;
            },
            (type, dim) => {
                dim.width = SCREEN_WIDTH;
                dim.height = 100;
            }
        );

        this._rowRenderer = this._rowRenderer.bind(this);

        //Since component should always render once data has changed, make data provider part of the state
        const gengen = this._generateArray()
        this.state = {
/*
            dataProvider: dataProvider.cloneWithRows(this._generateArray(300))
*/
            dataProvider: dataProvider.cloneWithRows(gengen),

            isViewMounted: true,
        };
    }

    _generateArray() {
        const n = this.props.discs.length
        let arr = new Array(n);
        for (let i = n; i > 0; i--) {
            arr[n-i] = this.props.discs[i-1]
        }
        return arr;
    }

    componentDidUpdate(prevProps) {
        const { discs } = this.props

        if (prevProps.discs === discs) {
            return
        }

        const gengen = this._generateArray()
        const dataProvider = this.state.dataProvider.cloneWithRows(gengen)

        this.setState({ dataProvider })
    }


    //Given type and data return the view component
    _rowRenderer(type, disc) {
        //You can return any view here, CellContainer has no special significance
        return <BubbleComponent disc={disc} />

    }

    render() {
        return (
            <>
                {this.props.discs.length > 0 &&
                <RecyclerListView
                        layoutProvider={this._layoutProvider}
                        dataProvider={this.state.dataProvider}
                        rowRenderer={this._rowRenderer}
                        forceNonDeterministicRendering={true}
                        style={{  transform: [{ scaleY: -1 }] }}
                />
                }
            </>
        );
    }
}

const styles = {
};

export default AlertRoomComponent;
