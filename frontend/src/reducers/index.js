import { combineReducers } from "redux";
import SoopsReducer from "./reducer_soops";
import ActiveSoop from "./reducer_active_soop";
import ActiveDay from "./reducer_active_day";

//this is the redux 'global' state
const rootReducer = combineReducers({
  soops: SoopsReducer,
  activeSoop: ActiveSoop,
  activeDay: ActiveDay
});

export default rootReducer;
