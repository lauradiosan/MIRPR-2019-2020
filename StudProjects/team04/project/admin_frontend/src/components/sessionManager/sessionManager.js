import React from 'react';
import {Table} from 'react-bootstrap';
import {connect} from "react-redux";
import {selectTab} from "../../store/actions/headerActions";
import {selectSession} from "../../store/actions/sessionsActions";

class SessionManager extends React.Component {

    getTableBodyAsReactElement() {
        if (this.props.isLoaded) {
            let sessions = this.props.items;
            return (sessions.length === 0) ?
                <h3 className="text-center text-light">
                    There are no sessions registered at the moment.
                </h3> : (
                    <Table responsive striped bordered hover variant="dark">
                        <thead>
                        <tr>
                            <th>Session ID</th>
                            <th>Description</th>
                            <th>Upload time</th>
                        </tr>
                        </thead>
                        <tbody>
                        {sessions.map((item) => {
                            return (
                                <tr key={item.id} style={{cursor: 'pointer'}}
                                    onClick={() => this.selectSession(item.id)}>
                                    {Object.entries(item).map((field) => {
                                        if (field[0].includes("upload_time_stamp")) {
                                            let date = "";
                                            let time = "";
                                            if (field[1] !== null) {
                                                date = new Date(Number(field[1])).toLocaleDateString();
                                                time = new Date(Number(field[1])).toLocaleTimeString();
                                            }
                                            return <td key={field[0] + item.id}>{date + " " + time}</td>
                                        } else {
                                            return <td key={field[1] + item.id}>{field[1]}</td>
                                        }
                                    })}
                                </tr>
                            );
                        })}
                        </tbody>
                    </Table>
                );
        } else {
            return (
                <h3 className="text-center text-danger">
                    Sessions could not load. Make sure the backend is started.
                </h3>
            )
        }
    }

    render() {
        return (
            <div className="App">
                <div className="centered">

                </div>
                <div className="centered">
                    {this.getTableBodyAsReactElement()}
                </div>
            </div>
        );
    }

    selectSession(sessionId) {
        this.props.selectSession(sessionId);
    }
}

const mapStateToProps = (state) => {
    return {
        isLoaded: state.session.isLoaded,
        items: state.session.sessions,
        sessionDetails: state.session.sessionDetails
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        selectSession: (sessionId) => {
            dispatch(selectSession(sessionId));
            dispatch(selectTab('Session report'));
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(SessionManager);