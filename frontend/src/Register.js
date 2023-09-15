import React, { useState } from "react";
import { registerUser } from "./api"; // Import the registerUser function
import {Link} from "react-router-dom";

function Register() {
  const [email, setEmail] = useState(""); // State for email input
  const [password, setPassword] = useState(""); // State for password input
  const [error, setError] = useState(""); // State for the error message

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
      setError(error.responseJSON.message);
    }
  };

  return (
  <div className="container">
    <div className="row justify-content-center">
      <div className="col-md-6">
        <div className="card mt-5">
          <div className="card-body">
            <h2 className="card-title text-center">Register</h2>
            {error && <p className="alert alert-danger">{error}</p>} {/* Display error message if there's an error */}
            <form onSubmit={handleSubmit}>
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
                  Register
                </button>
              </div>
            </form>
            <p className="mt-3 text-center">
              Already have an account? <Link to="/login">Login</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
);

}

export default Register;
