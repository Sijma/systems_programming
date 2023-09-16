import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { verifyEmail } from "../api"; // Import the verifyEmail function

const VerifyEmail = () => {
  const { token } = useParams(); // Get the token from the URL
  const [verificationStatus, setVerificationStatus] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Verify the email using the token
    const verifyUserEmail = async () => {
      try {
        const response = await verifyEmail(token);

        if (response.message === "Email verified successfully") {
          // Email verified successfully
          setVerificationStatus("success");

          // Redirect to the login page after a delay
          setTimeout(() => {
            navigate("/login");
          }, 3000);
        } else {
          // Email verification failed
          setVerificationStatus("failure");
        }
      } catch (error) {
        // Handle errors (e.g., network issues)
        setVerificationStatus("failure");
      }
    };

    verifyUserEmail();
  }, [token, navigate]);

  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <div className="verification-container text-center">
        {verificationStatus === "success" ? (
          <div className="alert alert-success" role="alert">
            Email verified successfully. Redirecting to login page...
          </div>
        ) : verificationStatus === "failure" ? (
          <div className="alert alert-danger" role="alert">
            Invalid or expired verification token.
          </div>
        ) : (
          <div className="alert alert-info" role="alert">
            Verifying email...
          </div>
        )}
      </div>
    </div>
  );
};

export default VerifyEmail;
