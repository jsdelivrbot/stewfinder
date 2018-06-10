import axios from "axios";

//we need to make sure that this action creator is wired to redux
export const SOOP_SELECTED = "soop_selected";
export const DAY_SELECTED = "day_selected";
export const FETCH_SOOPS = "fetch_soops";

//pulling out of local storage is too slow
//const ROOT_URL = localStorage.getItem("root_url");
//const API_KEY = localStorage.getItem("auth_token");
//const AUTH_STR = "Token " + API_KEY;

const AUTH_STR = "Token 1eefcbd33b05b8c56182ae2f953bdd7a33f367b4";
const ROOT_URL = "http://stewfinder-backend.us-west-2.elasticbeanstalk.com";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

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
  const auth = axios({
    method: "POST",
    url: `${ROOT_URL}/api/auth/`,
    data: {
      username: "admin",
      password: "ranger"
    }
  });

  const request = axios.get(`${ROOT_URL}/api/soops/`, {
    headers: { Authorization: AUTH_STR }
  });

  return dispatch => {
    request.then(({ data }) => {
      dispatch({ type: FETCH_SOOPS, payload: data });
    });
  };
}
