import React from 'react';
import { withStyles } from "@material-ui/core/styles";
import Button from '@material-ui/core/Button';
import InputLabel from '@material-ui/core/InputLabel';
import TextField from '@material-ui/core/TextField';
import SnackbarContent from '@material-ui/core/SnackbarContent';
import ErrorIcon from '@material-ui/icons/Error';
import '../../css/BaseStyle.css';

const styles = theme => ({
    error_color: {
        backgroundColor: theme.palette.error.light,
    },
    error_icon: {
        opacity: 0.9,
        marginRight: theme.spacing(1),
    },
    error_message: {
        display: 'flex',
        alignItems: 'center',
    },
    textField: {
        marginLeft: theme.spacing(1),
        marginRight: theme.spacing(1),
        width: 200,
    },
});


class SignInComponent extends React.Component {
    constructor(props) {
        super(props);

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(e) {
        e.preventDefault();
        const username = e.target.elements['username'].value
        const password = e.target.elements['password'].value

        this.props.handleSubmit(username, password);
    }

    componentDidMount() {
    }

    render() {
        const { classes } = this.props
        const { username, password, failed } = this.props;
        const { handleSubmit } = this;
        const contents = failed ? 'Username or password is incorrect.':''

        return (
            <form onSubmit={ this.handleSubmit }>
                <div className='center'>
                    <strong> Please SignIn </strong>
                    <br/>
                    <TextField
                        name="username"
                        label="Username"
                        className={classes.textField}
                        autoComplete="on"
                        margin="normal"
                      />
                    <TextField
                        name="password"
                        label="Password"
                        className={classes.textField}
                        type="password"
                        autoComplete="current-password"
                        margin="normal"
                      />
                    <br/>
                    <div className='margin-box1'>
                    <Button variant='contained' color='primary' type='submit'>
                        SUBMIT
                    </Button>
                    </div>
                    {contents &&
                        <SnackbarContent className={classes.error_color}
                            message = {
                                <div className={classes.error_message}>
                                    <ErrorIcon className={classes.error_icon}/>
                                    {contents}
                                </div>
                            }
                        />
                    }
                </div>
            </form>
        );
    }
}

export default withStyles(styles)(SignInComponent);
