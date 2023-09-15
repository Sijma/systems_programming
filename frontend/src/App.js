import React, { useEffect, useState } from "react";
import { BrowserRouter } from "react-router-dom";
import My_Routes from "./Routes";
import $ from "jquery";

function App() {
  return (
    <div className="App">
        <BrowserRouter>
            <My_Routes />
        </BrowserRouter>
    </div>
  );
}

export default App;
