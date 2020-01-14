import React from 'react';
import {connect} from 'react-redux';
import './sessionReport.css';
import {selectTab} from "../../store/actions/headerActions";
import {setSliderValue} from "../../store/actions/userActions";
import {Row, Col, Container} from 'reactstrap';
import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';
import GeneralPieChart from './piecharts/generalPieChart.js';
import TImeStampPieChart from './piecharts/timeStampPieChart.js'
import {fetchSessionDetails} from "../../store/actions/sessionsActions";

class SessionReport extends React.Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
        this.showSliderValue = this.showSliderValue.bind(this);
        this.tryUpdateDetails = this.tryUpdateDetails.bind(this);
    }
    componentDidMount() {
        this.props.loadData(this.props.sessionID);
        this.setState({interval: setInterval(this.tryUpdateDetails, 5000)});
    }
    componentWillUnmount() {
        clearInterval(this.state.interval);

    }

    handleChange(event, newValue) {
        this.props.setSliderValue(newValue);
    }
    tryUpdateDetails() {
        this.props.loadData(this.props.sessionID);
    }
    showSliderValue() {
        let seconds = 0;
        let minutes = 0;
        minutes = Math.floor(this.props.sliderValue / 60);
        seconds = this.props.sliderValue % 60;
        let valueText = "" + (this.props.sliderValue > 10 ? "" : "0") + seconds;
        return `${minutes}:${valueText}`
    }

    render() {

        if (!this.props.sessionDetails.isLoaded)
            return (<strong className={'Prompt-text'}>Still loading session details...</strong>);
        if (!this.sessionHasData())
            return (<strong className={'Prompt-text'}>This session has no data.</strong>);

        return (
            <div>
                <Row md={1}>
                    <Col md={4}>
                        <div className={"Back-button centered"}>
                            <button onClick={this.props.goBack} className={"btn btn-dark"}>
                                Go back to sessions table
                            </button>
                        </div>
                    </Col>
                    <Col md={8}>
                    </Col>
                </Row>
                <Row md={9}>
                    <Col md={4}>
                        <div className="centered">
                            <GeneralPieChart/>
                        </div>
                    </Col>
                    <Col md={4}>
                        <div className="centered">
                            <TImeStampPieChart/>
                        </div>
                    </Col>
                    <Col md={4}>
                        <img
                            width={400}
                            height={400}
                            src={"http://127.0.0.1:5000/get_image_for_session_and_second/" +
                            this.props.sessionDetails.sessionId + '/' + this.props.sliderValue}
                        />
                    </Col>
                </Row>
                <Row md={1}>
                    <Col md={6}>
                    </Col>
                    <Col md={4}>
                        <div className="centered">
                            <Typography id="sliderLabel" gutterBottom className="label-text bigger">
                                Time stamp
                            </Typography>
                            <Slider className="blue"
                                    onChange={this.handleChange}
                                    value={this.props.sliderValue}
                                    aria-labelledby="sliderLabel"
                                    step={1}
                                    max={this.props.sessionDetails.items[this.props.sessionDetails.items.length - 1].videoTimeStamp}
                                    min={0}
                                    orientation="horizontal"
                            />
                        </div>
                    </Col>
                    <Col md={2}>

                    </Col>
                </Row>
                <Row md={1}>
                    <Col md={6}>

                    </Col>
                    <Col md={4}>
                        <div className="centered">
                            <Typography className="label-text bigger">
                                {this.showSliderValue()}
                            </Typography>
                        </div>
                    </Col>
                    <Col md={2}>

                    </Col>
                </Row>
            </div>
        );
    }

    sessionHasData() {
        let series = this.props.sessionDetails.items;
        for (let i = 0; i < series.length; i++) {
            if (series[i] !== 0) {
                return true;
            }
        }
        return false;
    }
}

const mapStateToProps = (state) => {
    return {
        sessionDetails: state.session.sessionDetails,
        sliderValue: state.userInput.sliderValue,
        source: state.session.imageSource,
        sessionID: state.session.currentSessionId
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        goBack: () => {
            dispatch(selectTab('Manage sessions'));
        },
        setSliderValue: (value) => {
            dispatch(setSliderValue(value));
        },
        loadData: (id) => {
            dispatch(fetchSessionDetails(id))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(SessionReport);