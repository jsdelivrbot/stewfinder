import axios from "axios";

//we need to make sure that this action creator is wired to redux
export const SOOP_SELECTED = "soop_selected";
export const DAY_SELECTED = "day_selected";
export const FETCH_SOOPS = "fetch_soops";

const ROOT_URL = "http://127.0.0.1:8000";
const API_KEY = localStorage.getItem("auth_token");
const AUTH_STR = "Token 4847d6ca5fb338bd0f35531c4609a0d1bf67b5a6";

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
