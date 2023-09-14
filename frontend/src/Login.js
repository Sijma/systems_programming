// src/components/Login.js

import React, { useState } from "react";
import { loginUser } from "./api"; // Import the API functions
import $ from "jquery";

function Login() {
  const [token, setToken] = useState(""); // State to store the token
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

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
      console.error('Login failed:', error.responseJSON);
      // TODO: Handle login failure
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
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
    </div>
  );
}

export default Login;
