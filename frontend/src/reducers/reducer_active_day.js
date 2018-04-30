import { DAY_SELECTED } from "../actions";
import { TODAY } from "../containers/DateBar";

export default function(state = TODAY, action) {
  switch (action.type) {
    case DAY_SELECTED:
      return action.payload;

    default:
  }
  return state;
}
