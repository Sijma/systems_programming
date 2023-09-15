import React from "react";
import { logout } from "./api"; // Import the API functions
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();

  const handleGetRecommendation = () => {
    // Implement logic to get a recommendation
  };

  const handleSubscribe = () => {
    // Implement logic to subscribe to recommendations
  };

  const handleLogout = () => {
    logout()
    navigate("/login")
  };

  return (
    <div className="container">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card mt-5">
            <div className="card-body">
              <h2 className="card-title text-center">Dashboard</h2>
              <div className="text-center">
                <button
                  className="btn btn-primary mb-3"
                  onClick={handleGetRecommendation}
                >
                  Get Recommendation
                </button>
                <br />
                <button
                  className="btn btn-success mb-3"
                  onClick={handleSubscribe}
                >
                  Subscribe to Recommendations
                </button>
                <br />
                <button
                  className="btn btn-danger"
                  onClick={handleLogout}
                >
                  Log Out
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
