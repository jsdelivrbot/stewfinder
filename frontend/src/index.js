import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import reduxThunk from "redux-thunk";

import App from "./components/app";
import reducers from "./reducers";

const createStoreWithMiddleware = applyMiddleware(reduxThunk)(createStore);
localStorage.setItem("auth_token", "1eefcbd33b05b8c56182ae2f953bdd7a33f367b4");
localStorage.setItem(
  "root_url",
  "http://stewfinder-backend.us-west-2.elasticbeanstalk.com"
);

ReactDOM.render(
  <Provider store={createStoreWithMiddleware(reducers)}>
    <App />
  </Provider>,
  document.querySelector(".container")
);
