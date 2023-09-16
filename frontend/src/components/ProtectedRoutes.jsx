import { Outlet, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";
import {isAuth} from "../api"; // Import your isAuth function

const ProtectedRoutes = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(null);

  useEffect(() => {
    // Use useEffect to perform the asynchronous check
    const checkAuthentication = async () => {
      const authStatus = await isAuth(); // Use the isAuth function
      setIsAuthenticated(authStatus);
    };

    checkAuthentication();
  }, []); // The empty dependency array ensures the effect runs once

  if (isAuthenticated === null) {
    return null; // Render nothing while checking authentication
  }

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
};

export default ProtectedRoutes;
