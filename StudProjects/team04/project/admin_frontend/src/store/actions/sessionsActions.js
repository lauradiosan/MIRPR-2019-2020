import {properties} from "../../config/config";
import axios from 'axios';
import toaster from 'toasted-notes';
import 'toasted-notes/src/styles.css';

export const fetchAllSessions = () => {
    return (dispatch) => {
        fetch("http://" + properties.backend_url + "/session", {method: 'post'})
            .then(res => res.json())
            .then((res) => {
                    console.log("Loaded all sessions. Sessions: " + JSON.stringify(res));
                    let result = {
                        sessions: res,
                        success: true
                    };
                    dispatch(
                        {
                            type: "FETCH_ALL_SESSIONS",
                            payload: {result}
                        }
                    );
                },
                (error) => {
                    console.log("Could not fetch sessions. Error: " + error);
                    let result = {
                        sessions: [],
                        success: false
                    };
                    dispatch(
                        {
                            type: "FETCH_ALL_SESSIONS",
                            payload: {result}
                        }
                    );
                }
            );
    }
};

export const fetchSessionDetails = (sessionId) => {
    return (dispatch) => {
        fetch("http://" + properties.backend_url + "/session_details_emotions/" + sessionId, {method: 'post'})
            .then(res => res.json())
            .then(
                (res) => {
                    let mappedItems = [];
                    if (res.length !== 0)
                        mappedItems = res.reduce(function (map, obj) {
                            map[obj.videoTimeStamp] = obj;
                            return map;
                        })
                    console.log("Loaded session details for session with id " + sessionId + ": " + JSON.stringify(res));
                    dispatch({
                        type: "SHOW_SESSION_REPORT",
                        payload: {
                            sessionId: sessionId,
                            isLoaded: true,
                            items: res,
                            itemsByTimeStamp: mappedItems
                        }
                    });
                },
                (error) => {
                    console.log("Loading session details failed. Error: " + error);
                    dispatch({
                        type: "SHOW_SESSION_REPORT",
                        payload: {
                            isLoaded: false
                        }
                    });
                }
            );
    }
};

export const startSession = () => {
    return (dispatch) => {
        fetch("http://" + properties.backend_url + "/start_session", {method: 'post'})
            .then(res => res.json())
            .then((data) => {
                    console.log("Received started session: " + data);
                    let result = {
                        currentSessionStarted: data,
                        success: true
                    };
                    dispatch({type: "START_SESSION", payload: {result}});
                },
                (error) => {
                    console.log("Could not start session. Error: " + error);
                    let result = {
                        currentSessionStarted: null,
                        success: false
                    };
                    dispatch({type: "START_SESSION", payload: {result}});
                }
            );
    }
};
export const selectSession = (id) => {
    return {
        type: "SELECT_SESSION",
        payload: id
    }
};
export const stopSession = () => {
    return (dispatch) => {
        fetch("http://" + properties.backend_url + "/stop_session", {method: 'post'})
            .then(res => res.json())
            .then((data) => {
                    console.log("Received stopped session: " + data);
                    let result = {
                        stoppedSession: data,
                        success: true
                    };
                    dispatch({type: "STOP_SESSION", payload: {result}});
                },
                (error) => {
                    console.log("Could not stop session. Error: " + error);
                    let result = {
                        success: false
                    };
                    dispatch({type: "STOP_SESSION", payload: {result}});
                }
            );
    }
};
const processVideo = (id, video, upload, name) => {
    const data = new FormData();
    data.append('id', id);
    data.append('video', video);
    data.append('start', upload);
    data.append('name', name);
    console.log("Process video called");
    return (dispatch) => {
        dispatch({type: "UPLOAD_IN_PROGRESS"});
        axios.post("http://" + properties.backend_url + "/process_video", data, {})
            .then((response) => {
                console.log("Session created: " + JSON.stringify(response.data));
                toaster.notify('Upload completed!', {
                    duration: 10000
                });
                dispatch({
                    type: "UPLOAD_FINISHED",
                    payload: {
                        response: response.data,
                        success: true
                    }
                });
            }, (error) => {
                toaster.notify('Upload failed!', {
                    duration: 2000
                });
                console.log("Could not create session: " + error);
                dispatch({
                    type: "UPLOAD_FINISHED",
                    payload: {
                        success: false
                    }
                });
            });
    }
};
export const createSessionFromVideo = (video, upload, name) => {
    const data = new FormData();
    data.append('video', video);
    data.append('start', upload);
    data.append('name', name);
    return (dispatch) => {
        axios.post("http://" + properties.backend_url + "/create_session", data, {})
            .then((response) => {
                console.log("Session created: " + JSON.stringify(response.data));
                dispatch({
                    type: "SESSION_CREATED",
                    payload: {
                        response: response.data,
                    }
                });
                dispatch(processVideo(response.data.id, video, upload, name));
            }, (error) => {
                toaster.notify('Upload failed!', {
                    duration: 2000
                });
                console.log("Could not create session: " + error);
                dispatch({
                    type: "UPLOAD_FINISHED",
                    payload: {
                        success: false
                    }
                });
            });
    }
};