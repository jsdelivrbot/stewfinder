//@format
import {createSelector} from 'reselect';
import _ from 'lodash';

const soopSelector = state => {
  console.log(state.soops);
  return state.soops;
};
const selectedSoopSelector = state => state.activeDay;

const getSoops = (soops, activeDay) => {
  const selectedSoops = _.filter(soops, soop =>
    _.includes(String(activeDay), String(soop.day))
  );

  return selectedSoops;
};

export default createSelector(
  soopSelector, // pick off some state
  selectedSoopSelector, //pick off more state
  getSoops //last arg is the function with select logic
);
