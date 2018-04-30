import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import reduxThunk from "redux-thunk";

import App from "./components/app";
import reducers from "./reducers";

const createStoreWithMiddleware = applyMiddleware(reduxThunk)(createStore);
localStorage.setItem("auth_token", "4847d6ca5fb338bd0f35531c4609a0d1bf67b5a6");

ReactDOM.render(
  <Provider store={createStoreWithMiddleware(reducers)}>
    <App />
  </Provider>,
  document.querySelector(".container")
);
