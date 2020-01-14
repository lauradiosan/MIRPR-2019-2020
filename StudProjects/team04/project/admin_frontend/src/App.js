import React from 'react';
import './App.css';
import Header from './components/header/header'
import SessionManager from "./components/sessionManager/sessionManager";
import CreateLiveSession from "./components/createLiveSession/createLiveSession";
import CreateSessionFromVideo from "./components/createSessionFromVideo/createSessionFromVideo";
import {connect} from 'react-redux';
import {fetchAllSessions} from "./store/actions/sessionsActions";
import SessionReport from "./components/sessionReport/sessionReport";

class App extends React.Component {

    componentDidMount() {
        this.props.fetchAllSessions();
    }

    renderSelectedTabContent() {
        let selectedTab = this.props.selectedTab;
        switch (selectedTab) {
            case 'Create live session':
                return (
                    <CreateLiveSession/>
                );
            case 'Create session from video':
                return (
                    <CreateSessionFromVideo/>
                );
            case 'Manage sessions':
                return (
                    <SessionManager/>
                );
            case 'Session report':
                return (
                    <SessionReport/>
                );
            default:
                return ("");
        }
    }

    render() {
        return (
            <div className={'App'}>
                <Header/>
                <div className={'Scrollable-container'}>
                    {this.renderSelectedTabContent()}
                </div>
            </div>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        selectedTab: state.session.selectedTab
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        fetchAllSessions: () => {
            dispatch(fetchAllSessions());
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(App);
