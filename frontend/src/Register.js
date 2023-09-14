import React, { useState } from "react";
import { registerUser } from "./api"; // Import the registerUser function

function Register() {
  const [email, setEmail] = useState(""); // State for email input
  const [password, setPassword] = useState(""); // State for password input

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Call the registerUser function from api.js
      const response = await registerUser(email, password);

      // Handle successful registration (e.g., show a success message)
      console.log("Registration successful:", response);

      // You can also redirect the user to the login page or perform other actions
    } catch (error) {
      // Handle registration failure (e.g., show an error message)
      console.error("Registration failed:", error.responseJSON);
    }
  };

  return (
    <div className="register-container">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)} // Update 'email' state on input change
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
            onChange={(e) => setPassword(e.target.value)} // Update 'password' state on input change
            required
          />
        </div>
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;
