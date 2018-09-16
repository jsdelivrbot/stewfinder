//@format
import axios from 'axios';

//we need to make sure that this action creator is wired to redux
export const SOOP_SELECTED = 'soop_selected';
export const SOOP_LIKED = 'soop_liked';
export const SOOP_DISLIKED = 'soop_disliked';
export const SOOP_DELETE_LIKE = 'soop_delete_like';
export const SOOP_USER_VOTES = 'soop_user_votes';
export const DAY_SELECTED = 'day_selected';
export const FETCH_SOOPS = 'fetch_soops';

//pulling out of local storage is too slow for remote
//const ROOT_URL = localStorage.getItem('root_url');
//const API_KEY = localStorage.getItem('auth_token');
//const AUTH_STR = 'Token ' + API_KEY;

//local
//const AUTH_STR = 'Token 01f3fa85a9d727bf4651baa2b753ada32390bd06';
//const ROOT_URL = 'http://localhost:8000';

//remote
const AUTH_STR = "Token 324fe6cb5086fb9aca2400b796f723470288dcfa";
const ROOT_URL = "http://stewfinder-backend.us-west-2.elasticbeanstalk.com";

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export function selectSoop(soop) {
  return {
    type: SOOP_SELECTED,
    payload: soop
  };
}

// not linked to any reducer or state at the moment
// link it to state to have the button change verbs / function
export function getUserVotes(soop) {
  const soop_id = soop.id;
  const request = axios.get(`${ROOT_URL}/api/soops/${soop_id}/votes/user`, {
    headers: {Authorization: AUTH_STR}
  });
  return dispatch => {
    request.then(({data}) => {
      dispatch({type: SOOP_USER_VOTES, payload: data});
    });
  };
}

// not linked to any reducer or state at the moment
// link it to state to have the button change verbs / function
export function likeSoop(soop) {
  const soop_id = soop.id;
  const request = axios.get(`${ROOT_URL}/api/soops/${soop_id}/votes/up`, {
    headers: {Authorization: AUTH_STR}
  });
  //.then(res => console.log(res));
  return {
    type: SOOP_LIKED,
    payload: soop
  };
}

// not linked to any reducer or state at the moment
// link it to state to have the button change
export function dislikeSoop(soop) {
  const soop_id = soop.id;
  const request = axios.get(`${ROOT_URL}/api/soops/${soop_id}/votes/down`, {
    headers: {Authorization: AUTH_STR}
  });
  //.then(res => console.log(res));
  return {
    type: SOOP_DISLIKED,
    payload: soop
  };
}

// not linked to any reducer or state at the moment
// link it to state to have the button change
export function deleteLike(soop) {
  const soop_id = soop.id;
  const request = axios.get(`${ROOT_URL}/api/soops/${soop_id}/votes/delete`, {
    headers: {Authorization: AUTH_STR}
  });
  //.then(res => console.log(res));
  return {
    type: SOOP_DELETE_LIKE,
    payload: soop
  };
}

//selectDay
export function selectDay(day) {
  return {
    type: DAY_SELECTED,
    payload: day
  };
}

export function fetchSoops() {
  const request = axios.get(`${ROOT_URL}/api/soops/`, {
    headers: {Authorization: AUTH_STR}
  });

  return dispatch => {
    request.then(({data}) => {
      dispatch({type: FETCH_SOOPS, payload: data});
    });
  };
}
