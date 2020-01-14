let initialState = {
    sliderValue: 0
};
const userInputReducer = (state = initialState, action) => {
    switch (action.type) {
        case 'SET_SLIDER_VALUE': {
            console.log(action);
            let value = action.payload;
            return {
                ...state,
                sliderValue: value
            }
        }
        default:
            return {
                ...state
            };
    }
};

export default userInputReducer;