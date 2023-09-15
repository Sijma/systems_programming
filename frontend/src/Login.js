// src/components/Login.js

import React, {useState} from "react";
import {loginUser} from "./api"; // Import the API functions
import {Link} from "react-router-dom";
import $ from "jquery";
import "./css/App.css"; // Import the CSS file

function Login() {
  const [token, setToken] = useState(""); // State to store the token
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(""); // State for the error message

  const handleLogin = async (e) => {
    e.preventDefault();

    const email = $('#email').val();
    const password = $('#password').val();

    try {
      const response = await loginUser(email, password);
      const { access_token } = response;

      localStorage.setItem('token', access_token);

      setToken(access_token);

      console.log('Login successful:', response);
      // TODO: Handle successful login
    } catch (error) {
      //console.error('Login failed:', error.responseJSON);
      setError(error.responseJSON.message);
      // TODO: Handle login failure
    }
  };

  return (
      <div className="form-background">
        <div className="login-container">
          <h2>Login</h2>
          {error && <p className="error-message">{error}</p>} {/* Display error message if there's an error */}
          <form onSubmit={handleLogin}>
            <div className="form-group">
              <label htmlFor="email">Email:</label>
              <input
                  type="email"
                  id="email"
                  name="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
              />
            </div>
            <div className="form-group">
              <label htmlFor="password">Password:</label>
              <input
                  type="password"
                  id="password"
                  name="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
              />
            </div>
            <button type="submit">Login</button>
          </form>
          <Link to="/register" className="swap-button">
            Register
          </Link>
        </div>
      </div>
  );
}
export default Login;
