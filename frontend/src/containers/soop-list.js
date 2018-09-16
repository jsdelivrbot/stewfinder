//@format
import React, {Component} from 'react';
import {connect} from 'react-redux';
import {
  getUserVotes,
  deleteLike,
  dislikeSoop,
  likeSoop,
  selectSoop
} from '../actions/index';
import {bindActionCreators} from 'redux';
import {fetchSoops} from '../actions/index';
import DateBar from './DateBar';
import selectedSoop from '../selectors/selected_soop';

class SoopList extends Component {
  constructor() {
    super();
    this.state = {edited: [], likeLabel: 'like', dislikeLabel: 'dislike'};
  }

  handleLike(soop) {
    //this.setState({edited: this.state.edited.concat(soop.id)});
    let btn_classes = this.likebtn.classList;
    let key;
    let val;
    let obj;

    if (this.state[soop.id + 'likeLabel'] == 'liked') {
      this.props.actions.deleteLike.apply(soop);

      key = soop.id + 'likeLabel';
      val = 'like';
      obj = {};
      obj[key] = val;

      this.setState(obj);
    } else {
      this.props.actions.likeSoop.apply(soop);

      key = soop.id + 'likeLabel';
      val = 'liked';
      obj = {};
      obj[key] = val;

      this.setState(obj);
    }
  }

  handleDislike(soop) {
    //this.setState({edited: this.state.edited.concat(soop.id)});
    let btn_classes = this.dislikebtn.classList;

    if (this.state[soop.id + 'dislikeLabel'] == 'disliked') {
      this.props.actions.deleteLike.apply(soop);

      var key = soop.id + 'dislikeLabel';
      var val = 'dislike';
      var obj = {};
      obj[key] = val;

      this.setState(obj);
    } else {
      this.props.actions.dislikeSoop.apply(soop);

      var key = soop.id + 'dislikeLabel';
      var val = 'disliked';
      var obj = {};
      obj[key] = val;

      this.setState(obj);
    }
  }

  selectSoop(soop) {
    this.resetButtonState(soop);
    if (this.props.activeSoop == soop) {
      this.props.actions.selectSoop.apply(null);
    } else {
      this.props.actions.selectSoop.apply(soop);
    }
  }

  resetButtonState(soop) {
    //if (!this.state.edited.includes(soop.id)) {
    this.setState({likeLabel: 'like', dislikeLabel: 'dislike'});
    //}
  }

  renderList() {
    return this.props.selectedSoops.map(soop => {
      return (
        <div key={soop.title} className="soop-list">
          <li
            key={soop.title}
            className="list-group-item"
            style={{borderRadius: '25px'}}
            onClick={() => {
              this.selectSoop(soop);
            }}>
            <div>
              {soop.score
                ? soop.food +
                  '... ' +
                  soop.title +
                  '... score: ' +
                  soop.score.toFixed(2)
                : soop.food + '... ' + soop.title}
              <div
                className="button"
                style={{
                  display: 'flex'
                }}>
                <button
                  ref={btn => {
                    this.likebtn = btn;
                  }}
                  onClick={e => {
                    this.handleLike(soop);
                  }}
                  className={
                    this.state[soop.id + 'likeLabel'] == 'like' ||
                    this.state[soop.id + 'likeLabel'] == undefined
                      ? 'btn btn-success btn-sm button'
                      : 'btn btn-liked btn-sm button'
                  }>
                  {this.state[soop.id + 'likeLabel'] || 'like'}
                </button>
                <button
                  ref={btn => {
                    this.dislikebtn = btn;
                  }}
                  onClick={() => {
                    this.handleDislike(soop);
                    //this.props.actions.dislikeSoop.apply(soop);
                  }}
                  className={
                    this.state[soop.id + 'dislikeLabel'] == 'dislike' ||
                    this.state[soop.id + 'dislikeLabel'] == undefined
                      ? 'btn btn-danger btn-sm button'
                      : 'btn btn-disliked btn-sm button'
                  }>
                  {this.state[soop.id + 'dislikeLabel'] || 'dislike'}
                </button>
              </div>
            </div>
          </li>
          {this.props.activeSoop != null &&
            soop.title == this.props.activeSoop.title && (
              <div className="soop-details">
                <p>
                  <b>
                    {soop.when} <br />
                    {soop.location}
                  </b>
                </p>
                {soop.details} <span> </span>
                <a href={soop.outUrl} className="btn btn-warning btn-sm">
                  event link
                </a>
              </div>
            )}
        </div>
      );
    });
  }

  render() {
    return (
      <div className="rounded-corners container main-content">
        <DateBar />
        <ul className="left-align">{this.renderList()}</ul>
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

//i think this shows up as this.props.actions.selectSoop.apply()
function mapDispatchToProps(dispatch) {
  return {
    actions: {
      selectSoop: bindActionCreators({apply: selectSoop}, dispatch),
      getUserVotes: bindActionCreators({apply: getUserVotes}, dispatch),
      likeSoop: bindActionCreators({apply: likeSoop}, dispatch),
      dislikeSoop: bindActionCreators({apply: dislikeSoop}, dispatch),
      deleteLike: bindActionCreators({apply: deleteLike}, dispatch),
      fetchSoops: bindActionCreators({apply: fetchSoops}, dispatch)
    }
  };
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(SoopList);
