import React from "react";
import { Routes, Route } from "react-router-dom";
import Login from "./Login";
import Register from "./Register";
import WelcomePage from "./WelcomePage";
import Dashboard from "./Dashboard";
import ProtectedRoutes from "./ProtectedRoutes";
import NotFound from './NotFound';

const My_Routes = () => {
  return (
    <div className="app">
        <Routes>
            <Route exact path="/" element={<WelcomePage/>} />
            <Route exact path="/login" element={<Login/>} />
            <Route exact path="/register" element={<Register/>} />
            <Route path="/dashboard" element={<ProtectedRoutes/>}>
                <Route index element={<Dashboard/>} />
            </Route>
            <Route path='*' element={<NotFound/>} /> {/* This route matches any unknown route */}
        </Routes>
    </div>
  );
};

export default My_Routes;
