import React from 'react';
import './App.css';
import {Button, Table} from 'react-bootstrap';
import ReactApexChart from 'react-apexcharts';
import {properties} from "./config";

class App extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            sessionState: 'session-stopped',
            start_session_endpoint: 'http://' + properties.backend_url + '/start_session',
            stop_session_endpoint: 'http://' + properties.backend_url + '/stop_session',
            isLoaded: false,
            items: []
        };
        this.start_session = this.start_session.bind(this);
        this.stop_session = this.stop_session.bind(this);
        this.showPieChart = this.showPieChart.bind(this);
    }

    getTableBodyAsReactElement() {
        if(this.state.isLoaded) {
            let sessions = this.state.items;
            return (sessions.length === 0) ?
                    <h3 className="text-center text-light">
                        There are no sessions registered at the moment.
                    </h3> : (
                        <Table responsive striped bordered hover variant="dark">
                        <thead>
                        <tr>
                            <th>Session ID</th>
                            <th>Start time</th>
                            <th>End time</th>
                        </tr>
                        </thead>
                        <tbody>
                        {sessions.map((item) => {
                            return (
                                <tr key={item.id} style={{cursor: 'pointer'}}
                                    onClick={() => this.selectSession(item.id)}>
                                    {Object.entries(item).map((field) => {
                                        if(field[0].includes("time_stamp")){
                                            let date = "";
                                            let time = "";
                                            if(field[1] !== null){
                                            date = new Date(Number(field[1])).toLocaleDateString();
                                            time = new Date(Number(field[1])).toLocaleTimeString();
                                            }
                                            return <td>{date + " " + time}</td>
                                        } else{
                                            return <td>{field[1]}</td>
                                        }
                                    })}
                                </tr>
                            );
                        })}
                        </tbody>
                        </Table>
            );
        } else{
            return(
                    <h3 className="text-center text-danger">
                        Sessions could not load. Make sure the backend is started.
                    </h3>
            )
        }
    }

    fetchSessions(){
        fetch("http://" + properties.backend_url + "/session", {method: 'post'})
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        items: result
                    });
                },
                (error) => {
                    this.setState({
                        isLoaded: false
                    });
                }
            )
    }

    componentDidMount() {
        this.fetchSessions();
    }

    start_session(){
        this.setState({sessionState: 'session-started'});
        fetch(this.state.start_session_endpoint, {method: 'post'}).then((data) =>console.log(data));
        this.fetchSessions();
    }

    stop_session(){
        this.setState({sessionState: 'session-stopped'});
        fetch(this.state.stop_session_endpoint, {method: 'post'}).then((data) =>console.log(data));
        this.fetchSessions();
    }

    render(){
        return (
            <div className="App">
                <div className="centered">
                <Button
                    variant="secondary"
                    disabled={this.state.sessionState === 'session-started'}
                    onClick={this.start_session}
                >
                    Start session
                </Button>
                <Button
                    variant="secondary"
                    disabled={this.state.sessionState === 'session-stopped'}
                    onClick={this.stop_session}
                >
                    Stop session
                </Button>
                </div>
                <div className="centered">
                    {this.getTableBodyAsReactElement()}
                </div>
                <div className="centered">
                    {this.showPieChart()}
                </div>
            </div>
        );
    }

    fetchSessionDetails(sessionId){
        fetch("http://" + properties.backend_url + "/session_details_emotions/" + sessionId, {method: 'post'})
            .then(res => res.json())
            .then(
                (result) => {
\                    this.setState({
                        areDetailsLoaded: true,
                        details_items: result,
                        },
                        pie_chart_series: series
                    });
                },
                (error) => {
                    this.setState({
                        areDetailsLoaded: false
                    });
                }
            )
    }

    selectSession(sessionId){
        this.fetchSessionDetails(sessionId);
    }

    showPieChart() {
        if (this.state.areDetailsLoaded === true) {
            console.log(this.state.pie_chart_options);
            return (
                <ReactApexChart
                    options={this.state.pie_chart_options}
                    series={this.state.pie_chart_series}
                    type="pie"
                    width="450"
                />
            )
        } else {
            return undefined;
        }
    }
}

export default App;
