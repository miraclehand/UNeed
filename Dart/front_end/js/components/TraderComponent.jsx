import React from 'react';

import { createMaterialTopTabNavigator } from '@react-navigation/material-top-tabs';
import BuyComponent from './trader/BuyComponent'
import SellComponent from './trader/SellComponent'
import ModifyComponent from './trader/ModifyComponent'
import CancelComponent from './trader/CancelComponent'

const Tab = createMaterialTopTabNavigator();

class TraderComponent extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Tab.Navigator>
                <Tab.Screen name="매도">
                    {(props) => <SellComponent {...props} {...this.props} />}
                </Tab.Screen>
                <Tab.Screen name="매수">
                    {(props) => <BuyComponent {...props} {...this.props} />}
                </Tab.Screen>
                <Tab.Screen name="정정">
                    {(props) => <ModifyComponent {...props} {...this.props} />}
                </Tab.Screen>
                <Tab.Screen name="취소">
                    {(props) => <CancelComponent {...props} {...this.props} />}
                </Tab.Screen>
            </Tab.Navigator>
        )
    }
}

export default TraderComponent;
