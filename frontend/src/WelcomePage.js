import React from "react";
import { Link } from "react-router-dom";

function WelcomePage() {
  return (
    <div style={{ backgroundColor: "#e8e8e8", minHeight: "100vh" }}>
      <div className="d-flex justify-content-center align-items-center" style={{ minHeight: "calc(100vh - 100px)" }}>
        <div className="container-lg">
          <div className="card" style={{ minHeight: "400px" }}>
            <div className="card-body d-flex flex-column justify-content-between">
              <div>
                <h1 className="card-title text-center">Welcome to our Sports Betting Recommendation Service!</h1>
              </div>
              <div className="text-center">
                <h5 className="text-center">
                  We provide expert recommendations for sports betting to help you make informed decisions.
                </h5>
              </div>
              <div className="text-center">
                <p>
                  Ready to get started?{" "}
                  <Link to="/login" className="btn btn-primary">
                    Login
                  </Link>{" "}
                  or{" "}
                  <Link to="/register" className="btn btn-primary">
                    Register
                  </Link>{" "}
                  to access our recommendations.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default WelcomePage;
