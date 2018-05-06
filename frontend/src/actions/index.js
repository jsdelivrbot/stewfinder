import axios from "axios";

//we need to make sure that this action creator is wired to redux
export const SOOP_SELECTED = "soop_selected";
export const DAY_SELECTED = "day_selected";
export const FETCH_SOOPS = "fetch_soops";

const ROOT_URL = localStorage.getItem("root_url");
const API_KEY = localStorage.getItem("auth_token");
const AUTH_STR = "Token " + API_KEY;

export function selectSoop(soop) {
  return {
    type: SOOP_SELECTED,
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
    headers: { Authorization: AUTH_STR }
  });

  return dispatch => {
    request.then(({ data }) => {
      dispatch({ type: FETCH_SOOPS, payload: data });
    });
  };
}
