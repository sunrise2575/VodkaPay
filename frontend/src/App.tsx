import React, { Component } from "react";
import { Route } from "react-router-dom";
import { UserAuth } from "components/UserAuth";

function App() {
  return (
    <div className="App">
      <Route exact path="/" component={UserAuth} />
      <Route path="/ranking" component={UserAuth} />
    </div>
  );
}

export default App;
