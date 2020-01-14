import React from 'react'
import './createSessionFromVideo.css'
import {connect} from 'react-redux';
import {createSessionFromVideo} from "../../store/actions/sessionsActions";
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css"
import Loader from 'react-loader-spinner'

class CreateSessionFromVideo extends React.Component {
    constructor(props) {
        super(props);
        this.submit = this.submit.bind(this);
        this.state = {
            isInputValid: true,
        };
    }

    isVideoValid(video) {
        return video !== undefined;
    }

    submit(e) {
        e.preventDefault();
        const video = this.state.uploadedVideo;
        const name = this.state.name;
        if (!this.isVideoValid(video)) {
            this.setState({
                isInputValid: false,
                inputErrorMessage: 'No video was uploaded.'
            });
            return;
        }
        let uploadTimeMillis = new Date().getTime();
        this.setState({
            isInputValid: true
        });
        this.props.createSessionFromVideo(video, uploadTimeMillis, name );
    }

    getSubmitMessage() {
        if (this.state.isInputValid === false) {
            return (<div className={'Error-message-text'}>{this.state.inputErrorMessage}</div>);
        }
        if (this.props.uploadSuccess) {
            return (<div className={'Success-message-text'}>{this.props.uploadMessage}</div>);
        } else {
            return (<div className={'Error-message-text'}>{this.props.uploadMessage}</div>);
        }

    }

    getUploadedFileName() {
        const video = this.state.uploadedVideo;
        if (!this.isVideoValid(video)) {
            return (
                <div className={'file-control'}>
                    <div className="form-control bg-dark text-light">
                        {'No file selected...'}
                    </div>
                </div>
            );
        }
        return (
            <div className={'file-control'}>
                <div className="form-control bg-dark text-light">
                    {'Selected file: ' + video.name}
                </div>
            </div>
        );
    }

    setName = (event) => {
        this.setState({name: event.target.value})
    };

    setVideo = () => {
        if (this.uploadedVideoRef === null) {
            this.setState({uploadedVideo: undefined});
        } else {
            this.setState({uploadedVideo: this.uploadedVideoRef.files[0]});
        }
    };

    render() {
        return (
            <div className={'Create-session-from-video'}>
                <div className={'Form-container'}>
                    <form onSubmit={this.submit}>
                        <div className="form-group">
                            <label
                                className="text-light Label-text"
                                htmlFor="name-input"
                            >
                                Short description
                            </label>
                            <input id = "name-input"
                                className={'form-control bg-dark text-light Input-item'}
                                onChange={this.setName}
                            />
                        </div>
                        <div className="form-group">
                            <div className={"text-light Label-text"}>
                                Upload a video
                            </div>
                            <br/>
                            <div style={{width: '100%'}}>
                                <label
                                    className="btn btn-dark file-label border-light"
                                    htmlFor="videoInput"
                                >
                                    Select file
                                </label>
                                {this.getUploadedFileName()}
                                <input
                                    id="videoInput"
                                    className="input-file"
                                    type="file"
                                    ref={(ref) => this.uploadedVideoRef = ref}
                                    onChange={this.setVideo}
                                />
                            </div>
                        </div>
                        {
                            this.props.uploadInProgress ?
                                <div className={'simple-container'}>
                                    <Loader
                                        type="ThreeDots"
                                        color="#1d1c2e"
                                        height={60}
                                        width={60}
                                    />
                                </div> :
                                <div className={'simple-container'}>
                                    <button className="btn btn-dark col-sm-4">Submit</button>
                                </div>
                        }
                        <div className={'simple-container'}>
                            {this.getSubmitMessage()}
                        </div>
                    </form>
                </div>
            </div>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        uploadInProgress: state.session.uploadInProgress,
        uploadMessage: state.session.uploadMessage,
        uploadSuccess: state.session.uploadSuccess
    }
};
const mapDispatchToProps = (dispatch) => {
    return {
        createSessionFromVideo: (video, upload, name) => {
            dispatch(createSessionFromVideo(video, upload, name));
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(CreateSessionFromVideo);