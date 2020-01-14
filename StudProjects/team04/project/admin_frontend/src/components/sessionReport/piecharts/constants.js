const PIECHART_OPTIONS = {
    labels: ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral'],
    legend: {
        show: false
    },
    responsive: [{
        breakpoint: 480,
        options: {
            chart: {
                width: 200
            }
        }
    }]
}
export default PIECHART_OPTIONS;