import _ from "lodash";
import { FETCH_SOOPS } from "../actions";

export default function(state = {}, action) {
  switch (action.type) {
    case FETCH_SOOPS:
      console.log(_.mapKeys(action.payload, "id"));
      return _.mapKeys(action.payload, "id");

    default:
      return state;
  }
}
