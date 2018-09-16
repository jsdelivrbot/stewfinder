import React, { Component } from "react";
import { connect } from "react-redux";

import SoopList from "../containers/soop-list";
import { fetchSoops } from "../actions";

class App extends Component {
  // auto-called by react when this component shows up in the DOM
  componentDidMount() {
    this.props.fetchSoops();
  }

  render() {
    return (
      <div className="rounded-corners app-main">
        <SoopList />
      </div>
    );
  }
}

export default connect(null, { fetchSoops })(App);
