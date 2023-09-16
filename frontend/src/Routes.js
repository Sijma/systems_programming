import React from "react";
import { Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import WelcomePage from "./components/WelcomePage";
import Dashboard from "./components/Dashboard";
import ProtectedRoutes from "./components/ProtectedRoutes";
import NotFound from './components/NotFound';
import VerifyEmail from "./components/VerifyEmail";

const My_Routes = () => {
  return (
    <div className="app">
        <Routes>
            <Route exact path="/" element={<WelcomePage/>} />
            <Route exact path="/login" element={<Login/>} />
            <Route exact path="/register" element={<Register/>} />
            <Route path="/verify_email/:token" element={<VerifyEmail/>} />
            <Route path="/dashboard" element={<ProtectedRoutes/>}>
                <Route index element={<Dashboard/>} />
            </Route>
            <Route path='*' element={<NotFound/>} /> {/* This route matches any unknown route */}
        </Routes>
    </div>
  );
};

export default My_Routes;
