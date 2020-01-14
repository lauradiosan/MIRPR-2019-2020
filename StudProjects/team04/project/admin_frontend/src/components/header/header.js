import React from "react";
import {connect} from "react-redux";
import {selectTab} from "../../store/actions/headerActions";

class Header extends React.Component {
    constructor(props) {
        super(props);
        this.selectTab = this.selectTab.bind(this);
    }

    selectTab(tabName) {
        this.props.selectTab(tabName);
    }

    getTabs() {
        let tabs = this.props.tabs;
        let selectedTab = this.props.selectedTab;
        return (
            <ul className="navbar-nav ml-auto">
                {
                    tabs.map((tab) => {
                        if (tab.name === selectedTab) {
                            return (
                                <li key={tab.id} className="nav-item active">
                                    <a
                                        style={text}
                                        className="nav-link"
                                        href="#"
                                        onClick={() => this.selectTab(tab.name)}
                                    >
                                        {tab.name}
                                    </a>
                                </li>
                            );
                        } else {
                            return (
                                <li key={tab.id} className="nav-item">
                                    <a
                                        style={text}
                                        className="nav-link"
                                        href="#"
                                        onClick={() => this.selectTab(tab.name)}
                                    >
                                        {tab.name}
                                    </a>
                                </li>
                            );
                        }
                    })
                }
            </ul>
        );
    }

    render() {
        return (
            <nav style={header} className="navbar navbar-expand-lg navbar-dark bg-dark static-top">
                <div className="container">
                    <a className="navbar-brand" href="#">
                        <span style={text}>
                            <img
                                width={150}
                                height={150}
                                src={require('../../resources/logo.png')}
                                alt=""
                            />
                        </span>
                    </a>
                    <div className="navbar navbar-expand-sm">
                        {this.getTabs()}
                    </div>
                </div>
            </nav>
        );
    }
}

const text = {
    fontSize: 15,
    fontWeight: 'bold'
};

const header = {};

const mapStateToProps = (state) => {
    return {
        tabs: state.session.tabs,
        selectedTab: state.session.selectedTab
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        selectTab: (tabName) => {
            dispatch(selectTab(tabName));
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Header);