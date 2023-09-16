import React, { useState } from "react";
import { logout } from "../api"; // Import the API functions
import { useNavigate } from "react-router-dom";
import ManageSubscription from "./ManageSubscription"; // Import the ManageSubscription component

function Dashboard() {
  const navigate = useNavigate();
  const [showManageSubscription, setShowManageSubscription] = useState(false);

  const handleGetRecommendation = () => {
    // Implement logic to get a recommendation
  };

  const handleSubscribe = () => {
    setShowManageSubscription(true); // Set the flag to show the ManageSubscription component
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div style={{ backgroundColor: "#e8e8e8", minHeight: "100vh" }}>
      {showManageSubscription ? (
              <ManageSubscription
                setShowManageSubscription={setShowManageSubscription}
              />
            ) : (
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
                    Manage Subscriptions
                  </button>
                  <br />
                  <button className="btn btn-danger" onClick={handleLogout}>
                    Log Out
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      )}
    </div>
  );
}

export default Dashboard;
