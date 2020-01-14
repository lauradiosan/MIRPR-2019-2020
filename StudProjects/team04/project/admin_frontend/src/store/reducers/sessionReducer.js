let initialState = {
    tabs: [
        {id: 1, name: 'Manage sessions'},
        {id: 3, name: 'Create session from video'}
    ],
    currentSessionId: 0,
    selectedTab: 'Manage sessions',
    uploadInProgress: false,
    uploadMessage: '',
    imageLoadInProgress: false,
    imageLoadSuccess: false,
    imageSource: {},
    uploadSuccess: false,
    sessionCreatedFromVideo: null,
    sessions: [],
    currentSessionStarted: null,
    isLoaded: false,
    sessionDetails: {
        sessionId: -1,
        isLoaded: false,
        items: [],
        itemsByTimeStamp: []
    }
};

const sessionReducer = (state = initialState, action) => {
    switch (action.type) {
        case 'FETCH_ALL_SESSIONS': {
            console.log(action);
            let result = action.payload.result;
            return {
                ...state,
                sessions: result.sessions,
                isLoaded: result.success
            }
        }
        case 'START_SESSION': {
            let result = action.payload.result;
            if (result.success === true) {
                return {
                    ...state,
                    sessions: [...state.sessions, result.currentSessionStarted],
                    currentSessionStarted: result.currentSessionStarted
                }
            } else {
                return {
                    ...state
                }
            }
        }
        case 'STOP_SESSION': {
            let result = action.payload.result;
            if (result.success === true) {
                let sessions = state.sessions;
                let stoppedSession = result.stoppedSession;
                for (let i = 0; i < sessions.length; i++) {
                    if (sessions[i].id === stoppedSession.id) {
                        sessions[i] = stoppedSession;
                        break;
                    }
                }
                return {
                    ...state,
                    sessions: sessions,
                    currentSessionStarted: null
                }
            } else {
                return {
                    ...state
                }
            }
        }
        case 'SELECT_SESSION': {
            console.log(action);
            return {
                ...state,
                currentSessionId: action.payload
            }
        }
        case 'SHOW_SESSION_REPORT': {
            console.log(state.sessionDetails);
            return {
                ...state,
                sessionDetails: action.payload

            }
        }
        case 'SELECT_TAB': {
            return {
                ...state,
                selectedTab: action.tabName
            }
        }
        case 'UPLOAD_IN_PROGRESS': {
            return {
                ...state,
                uploadInProgress: true
            }
        }
        case 'IMAGE_PENDING': {
            return {
                ...state,
                imageLoadInProgress: true
            }
        }
        case 'IMAGE_SUCCESS': {
            return {
                ...state,
                imageLoadInProgress: false,
                imageLoadSuccess: true,
                imageSource: action.payload
            }
        }
        case 'IMAGE_FAILED': {
            return {
                ...state,
                imageLoadInProgress: false,
                imageLoadSuccess: false
            }
        }
        case 'SESSION_CREATED': {
            let sessionCreatedFromVideo = action.payload.response;
            sessionCreatedFromVideo.uploadInProgess = true;
            let uploadMessage =
                'Create session with id |' + sessionCreatedFromVideo.id + '|.';
            return {
                ...state,
                sessionCreatedFromVideo: sessionCreatedFromVideo,
                uploadMessage: uploadMessage,
                sessions: [...state.sessions, sessionCreatedFromVideo]
            };
        }
        case 'UPLOAD_FINISHED': {
            if (action.payload.success === true) {
                let sessionCreatedFromVideo = action.payload.response;
                sessionCreatedFromVideo.uploadInProgess = false;
                let uploadMessage =
                    'Video finished uploading! Create session with id |' + sessionCreatedFromVideo.id + '|.';
                return {
                    ...state,
                    uploadInProgress: false,
                    sessionCreatedFromVideo: sessionCreatedFromVideo,
                    uploadMessage: uploadMessage,
                    uploadSuccess: action.payload.success,
                    sessions: [...state.sessions, sessionCreatedFromVideo]
                };
            } else {
                return {
                    ...state,
                    uploadInProgress: false,
                    uploadSuccess: action.payload.success,
                    uploadMessage: 'Video failed to upload!'
                }
            }
        }
        default:
            return {
                ...state
            };
    }
};

export default sessionReducer;