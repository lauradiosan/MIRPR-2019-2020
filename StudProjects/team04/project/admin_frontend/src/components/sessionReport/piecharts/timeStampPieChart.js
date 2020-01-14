import PIECHART_OPTIONS from './constants.js';
import React from 'react';
import ReactApexChart from "react-apexcharts";
import {connect} from 'react-redux';
import './timeStampPieChart.css';
import Typography from '@material-ui/core/Typography';

class TimeStampPieChart extends React.Component {

    getFieldsAsArray(session_details, timeStamp) {
        const selected = session_details[timeStamp];
        return [selected.angryProbability, selected.disgustProbability, selected.fearProbability,
                selected.happyProbability, selected.sadProbability, selected.surpriseProbability,
                selected.neutralProbability];
    }
    render() {
        if(!this.props.items[this.props.sliderValue])
            return (
                <div className = "max-size centered">
                    <Typography className = "label-text bigger">
                        Data not avaiable
                    </Typography>
                </div>);
        if(this.props.items[this.props.sliderValue].emotion == -1)
            return (
                <div className = "max-size centered smaller">
                    <Typography className = "label-text bigger">
                         Face not detected
                    </Typography>
                </div>);
        return (
            <ReactApexChart
                options={PIECHART_OPTIONS}
                series={this.getFieldsAsArray(this.props.items, this.props.sliderValue)}
                type="pie"
                width="450"
             />
        );
    }
}
const mapStateToProps = (state) => {
    return {
        items: state.session.sessionDetails.itemsByTimeStamp,
        sliderValue: state.userInput.sliderValue
    }
};

export default connect(mapStateToProps)(TimeStampPieChart);