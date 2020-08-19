import React from 'react'
import { Button } from 'react-native'
import SocialLogin from 'react-social-login'
 
/*
https://codesandbox.io/s/3rpq558rv5?file=/src/index.js
*/
class SocialButton extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <button onClick={this.props.triggerLogin} {...this.props}>
                { this.props.children }
            </button>
        );
        /*

        return (
            <Button
                title = { this.props.children }
                onPress={this.props.triggerLogin} {...this.props}
            />
            );
            */
    }
}
            
export default SocialLogin(SocialButton);
