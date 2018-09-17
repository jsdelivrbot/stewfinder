import React, { Component } from "react";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { selectDay } from "../actions/index";

var weekday = new Array(7);
weekday[0] = "Mon";
weekday[1] = "Tue";
weekday[2] = "Wed";
weekday[3] = "Thur";
weekday[4] = "Fri";
weekday[5] = "Sat";
weekday[6] = "Sun";

Date.prototype.addDays = function(days) {
  var dat = new Date(this.valueOf());
  dat.setDate(dat.getDate() + days);
  return dat;
};

Date.prototype.getUTCLocalDate = function() {
  var target = new Date(this.valueOf());
  var offset = target.getTimezoneOffset();
  var Y = target.getUTCFullYear();
  var M = target.getUTCMonth();
  var D = target.getUTCDate();
  var h = target.getUTCHours();
  var m = target.getUTCMinutes();
  var s = target.getUTCSeconds();

  return new Date(Date.UTC(Y, M, D, h, m - offset, s));
};

const today = new Date().getUTCLocalDate();
export const TODAY = today.toLocaleDateString();
export const TODAY_NUM = today.getDay();
export const TODAY_DAY = weekday[TODAY_NUM];

class DateBar extends Component {
  // returns an array of the next x days
  getDays(startDate = today, daysToAdd = 5) {
    //this will be returned
    var returnDays = [];
    //begins as today
    const curDate = new Date().getUTCLocalDate();

    //push each day into the array
    for (var i = 0, len = daysToAdd; i < len; i++) {
      var dayToAdd = curDate.addDays(i);
      returnDays.push(dayToAdd);
    }

    //console.log(returnDays.map(day => day.getDay()));
    return returnDays;
  }

  //map days to an array of the next week
  renderDays() {
    var days = this.getDays();
    return days.map(day => {
      var className = `weekday-table ${
        day.toLocaleDateString() == this.props.activeDay ? "active" : "inactive"
      }`;
      return (
        <td
          key={day}
          className={className}
          onClick={() => this.props.selectDay(day.toLocaleDateString())}
          scope="col"
        >
            {
                window.innerWidth > 365?
                day.toLocaleString(window.navigator.language, { weekday: "short" }):
                day.toLocaleString(window.navigator.language, { weekday: "short" }).slice(0,1)
            }
        </td>
      );
    });
  }

  render() {
    return (
        <table 
            className="rounded-table date-bar table table-dark table-responsive-lg table-bordered"
            style={{
                    "borderCollapse":"separate",
                    "border":"solid #f8f8ff 3px",
                    "borderRadius":"12px",
                    "MozBorderRadius":"6px",
                    "boxShadow": "10px 10px 10px grey"
            }}
        >
        <tbody>
          <tr >{this.renderDays()}</tr>
        </tbody>
      </table>
    );
  }
}

function mapStateToProps(state) {
  return {
    activeDay: state.activeDay
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators({ selectDay: selectDay }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(DateBar);
