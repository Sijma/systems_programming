import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./Login";
import Register from "./Register";
import Dashboard from "./Dashboard";
import ProtectedRoutes from "./ProtectedRoutes";
import NotFound from './NotFound';

const My_Routes = () => {
  return (
    <div className="app">
        <Routes>
            <Route exact path="/login" element={<Login/>} />
            <Route exact path="/register" element={<Register/>} />
            <Route element={<ProtectedRoutes/>}>
                <Route path="/dashboard" element={<Dashboard/>} />
            </Route>
            <Route path='*' element={<NotFound/>} /> {/* This route matches any unknown route */}
        </Routes>
    </div>
  );
};

export default My_Routes;
