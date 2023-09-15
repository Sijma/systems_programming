import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootswatch/dist/zephyr/bootstrap.min.css';
import React, { useEffect, useState } from "react";
import { BrowserRouter } from "react-router-dom";
import My_Routes from "./Routes";

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
