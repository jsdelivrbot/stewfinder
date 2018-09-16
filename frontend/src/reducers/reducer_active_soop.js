import { SOOP_SELECTED } from "../actions";

// passed from actions --> reducers
export default function(state = null, action) {
  switch (action.type) {
    case SOOP_SELECTED:
      return action.payload;

    default:
  }
  return state;
}
