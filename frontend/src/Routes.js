import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./Login";
import Register from "./Register";
import Dashboard from "./Dashboard";
import PrivateRoute from "./PrivateRoute";

const My_Routes = () => {
  return (
    <div className="app">
        <Routes>
            <Route exact path="/login" element={<Login/>} />
            <Route exact path="/register" element={<Register/>} />
            <Route exact path="/dashboard" element={<Dashboard/>} />
            {/*<Navigate to="/" />*/}
        </Routes>
    </div>
  );
};

export default My_Routes;
