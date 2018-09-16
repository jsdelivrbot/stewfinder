import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import reduxThunk from "redux-thunk";

import App from "./components/app";
import reducers from "./reducers";

const createStoreWithMiddleware = applyMiddleware(reduxThunk)(createStore);

//local
//localStorage.setItem("auth_token", "01f3fa85a9d727bf4651baa2b753ada32390bd06");
//localStorage.setItem(
    //"root_url", "http://localhost:8000"
//);

//remote
localStorage.setItem("auth_token", "324fe6cb5086fb9aca2400b796f723470288dcfa");
localStorage.setItem(
  "root_url", "http://stewfinder-backend.us-west-2.elasticbeanstalk.com"
);

ReactDOM.render(
  <Provider store={createStoreWithMiddleware(reducers)}>
    <App />
  </Provider>,
  document.querySelector(".container")
);
