import PIECHART_OPTIONS from './constants.js';
import React from 'react';
import ReactApexChart from "react-apexcharts";
import {connect} from 'react-redux';

class GeneralPieChart extends React.Component {
    getPieChartSeriesFromJSONResult(session_details) {
        let happyCount = 0;
        let sadCount = 0;
        let fearCount = 0;
        let disgustCount = 0;
        let angryCount = 0;
        let neutralCount = 0;
        let surpriseCount = 0;
        session_details.map((item) => {
            Object.entries(item).map((field) => {
                if (field[0] === 'emotion') {
                    if (field[1] === 3) {
                        happyCount += 1;
                    } else if (field[1] === 4) {
                        sadCount += 1;
                    } else if (field[1] === 2) {
                        fearCount += 1;
                    } else if (field[1] === 1) {
                        disgustCount += 1;
                    } else if (field[1] === 0) {
                        angryCount += 1;
                    } else if (field[1] === 6) {
                        neutralCount += 1;
                    } else if (field[1] === 5) {
                        surpriseCount += 1;
                    }
                }
            })
        });
        return [angryCount, disgustCount, fearCount, happyCount, sadCount, surpriseCount, neutralCount];
    }
    render() {
        return (
            <ReactApexChart
                options={PIECHART_OPTIONS}
                series={this.getPieChartSeriesFromJSONResult(this.props.items)}
                type="pie"
                width="450"
             />
        );
    }
}

const mapStateToProps = (state) => {
    return {
        items: state.session.sessionDetails.items
    }
};

export default connect(mapStateToProps)(GeneralPieChart);