// src/components/Login.js

import React, {useState} from "react";
import {loginUser} from "./api"; // Import the API functions
import {Link} from "react-router-dom";
import { useNavigate } from "react-router-dom";
import $ from "jquery";

function Login() {
  const navigate = useNavigate();
  const [token, setToken] = useState(""); // State to store the token
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(""); // State for the error message

  const navigateDashboard = () => {
    navigate('/dashboard');
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    const email = $('#email').val();
    const password = $('#password').val();

    try {
      const response = await loginUser(email, password);
      const { access_token, refresh_token } = response;

      // Store both access_token and refresh_token in localStorage
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);

      setToken(access_token);

      console.log('Login successful:', response);
      navigateDashboard();
    } catch (error) {
      //console.error('Login failed:', error.responseJSON);
      setError(error.responseJSON.message);
    }
  };

  return (
    <div className="container">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card mt-5">
            <div className="card-body">
              <h2 className="card-title text-center">Login</h2>
              {error && <p className="alert alert-danger">{error}</p>} {/* Display error message if there's an error */}
              <form onSubmit={handleLogin}>
                <div className="mb-3">
                  <label htmlFor="email" className="form-label">
                    Email:
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="form-control"
                    required
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="password" className="form-label">
                    Password:
                  </label>
                  <input
                    type="password"
                    id="password"
                    name="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="form-control"
                    required
                  />
                </div>
                <div className="text-center">
                  <button type="submit" className="btn btn-primary">
                    Login
                  </button>
                </div>
              </form>
              <p className="mt-3 text-center">
                Don't have an account?{" "}
                <Link to="/register">Register</Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
