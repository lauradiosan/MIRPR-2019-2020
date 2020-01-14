import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import 'bootstrap/dist/css/bootstrap.min.css';
import {combineReducers, createStore, applyMiddleware} from 'redux';
import {Provider} from 'react-redux'
import sessionReducer from "./store/reducers/sessionReducer";
import userInputReducer from "./store/reducers/userInputReducer"
import thunk from 'redux-thunk';
const rootReducer = combineReducers({session: sessionReducer, userInput: userInputReducer})

const store = createStore(rootReducer, applyMiddleware(thunk));

ReactDOM.render(<Provider store={store}><App/></Provider>, document.getElementById('app'));
