import React, { Component } from "react";
import { connect } from "react-redux";
import { selectSoop } from "../actions/index";
import { bindActionCreators } from "redux";
import { fetchSoops } from "../actions/index";
import DateBar from "./DateBar";
import selectedSoop from "../selectors/selected_soop";

class SoopList extends Component {
  renderList() {
    return this.props.selectedSoops.map(soop => {
      return (
        <div key={soop.title}>
          <li
            key={soop.title}
            className="list-group-item"
            onClick={() => {
              this.props.actions.selectSoop.apply(soop);
            }}
          >
            {soop.food + "... " + soop.title}
          </li>
          {this.props.activeSoop != null &&
            soop.title == this.props.activeSoop.title && (
              <div>
                <p>
                  <b>
                    {soop.when} <br />
                    {soop.location}
                  </b>
                </p>
                {soop.details} <span> --</span>
                <a href={soop.outUrl}> event link</a>
              </div>
            )}
        </div>
      );
    });
  }

  render() {
    return (
      <div>
        <DateBar />
        <ul>{this.renderList()}</ul>
      </div>
    );
  }
}

// state.selectedSoops --> this.props.selectedSoops
function mapStateToProps(state) {
  return {
    activeSoop: state.activeSoop,
    activeDay: state.activeDay,
    selectedSoops: selectedSoop(state)
  };
}

//function mapDispatchToProps(dispatch) {
//return bindActionCreators({ selectSoop: selectSoop }, dispatch);
//}

function mapDispatchToProps(dispatch) {
  return {
    actions: {
      selectSoop: bindActionCreators({ apply: selectSoop }, dispatch),
      fetchSoops: bindActionCreators({ apply: fetchSoops }, dispatch)
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(SoopList);
