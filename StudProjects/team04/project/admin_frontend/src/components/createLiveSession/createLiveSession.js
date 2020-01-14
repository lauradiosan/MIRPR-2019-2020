import React from 'react'
import './createLiveSession.css'
import {Button} from "react-bootstrap";
import {connect} from 'react-redux';
import {startSession, stopSession} from "../../store/actions/sessionsActions";

class CreateLiveSession extends React.Component {
    constructor(props) {
        super(props);
        this.startSession = this.startSession.bind(this);
        this.stopSession = this.stopSession.bind(this);
    }

    render() {
        return (
            <div className={'Create-live-session'}>
                <Button
                    className={'Button-custom'}
                    variant="dark"
                    disabled={this.props.currentSessionStarted !== null}
                    onClick={this.startSession}
                >
                    Start session
                </Button>
                <Button
                    className={'Button-custom'}
                    variant="dark"
                    disabled={this.props.currentSessionStarted === null}
                    onClick={this.stopSession}
                >
                    Stop session
                </Button>
                <br/>
                <strong className={'Prompt-text'}>{this.getPromptText()}</strong>
            </div>
        );
    }

    getPromptText(){
        if(this.props.currentSessionStarted !== null){
            return 'Session with id: ' + this.props.currentSessionStarted.id  + ' is started.';
        } else {
            return 'No session is started at the moment.';
        }
    }

    startSession() {
        this.props.startSession();
    }

    stopSession() {
        this.props.stopSession();
    }
}

const mapStateToProps = (state) => {
    return{
        currentSessionStarted: state.session.currentSessionStarted
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        startSession: () => {
            dispatch(startSession());
        },
        stopSession: () => {
            dispatch(stopSession());
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(CreateLiveSession);