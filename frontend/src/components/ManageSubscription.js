import React, { useState, useEffect } from "react";
import {
  subscribe,
  viewSubscription,
  editSubscription,
  deleteSubscription,
  getRecommenders,
} from "../api"; // Import the API functions

function ManageSubscription({ setShowManageSubscription }) {
  const [recommenders, setRecommenders] = useState([]); // State for recommender options
  const [selectedRecommender, setSelectedRecommender] = useState(""); // State for selected recommender
  const [frequency, setFrequency] = useState(""); // State for subscription frequency
  const [numRecommendations, setNumRecommendations] = useState(1); // State for the number of recommendations
  const [subscription, setSubscription] = useState(null); // State for current subscription
  const [message, setMessage] = useState(""); // State for messages (e.g., success, error)
  const [loading, setLoading] = useState(false); // State to track loading state

  useEffect(() => {
    // Fetch the list of recommenders from API when the component mounts
    getRecommenderOptions();

    // Fetch and display current subscriptions
    viewCurrentSubscriptions();
  }, []);

  const getRecommenderOptions = async () => {
    try {
      // Call the getRecommenders function from api.js to fetch the list of recommenders
      const response = await getRecommenders();
      setRecommenders(response); // Set the list of recommenders in state
    } catch (error) {
      console.error("Error fetching recommenders:", error);
    }
  };

  const viewCurrentSubscriptions = async () => {
    try {
      // Call the viewSubscription function from api.js to fetch and display the current subscription
      const response = await viewSubscription();
      setSubscription(response); // Set the current subscription as an object
    } catch (error) {
      // Handle the case when there's no active subscription
      setSubscription(null); // Set the current subscription as null
    }
  };

  const handleBack = () => {
    setShowManageSubscription(false); // Set the flag to hide the ManageSubscription component
  };

  const handleSubscribe = async () => {
    console.log(numRecommendations)
    if (!selectedRecommender || !frequency || isNaN(numRecommendations)) {
      // Check if any of the fields is empty
      setMessage("Error: Please fill out all fields.");
      return;
    }

    setLoading(true);
    try {
      // Call the subscribeUser function from api.js to subscribe
      await subscribe(selectedRecommender, frequency, numRecommendations);
      setMessage("Subscription added successfully");
      viewCurrentSubscriptions(); // Refresh the current subscriptions list
    } catch (error) {
      console.error("Error subscribing:", error);
      setMessage("Subscription failed");
    } finally {
      setLoading(false);
    }
  };

  const handleEditSubscription = async () => {
    if (!selectedRecommender || !frequency || isNaN(numRecommendations)) {
      // Check if any of the fields is empty
      setMessage("Error: Please fill out all fields.");
      return;
    }

    setLoading(true);
    try {
      // Call the editSubscription function from api.js to edit the subscription
      await editSubscription(selectedRecommender, frequency, numRecommendations);
      setMessage("Subscription updated successfully");
      viewCurrentSubscriptions(); // Refresh the current subscriptions list
    } catch (error) {
      console.error("Error editing subscription:", error);
      setMessage("Error: Subscription update failed");
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteSubscription = async () => {
    setLoading(true);
    try {
      // Call the deleteSubscription function from api.js to delete the subscription
      await deleteSubscription();
      setMessage("Subscription deleted successfully");
      viewCurrentSubscriptions(); // Refresh the current subscriptions list
    } catch (error) {
      console.error("Error deleting subscription:", error);
      setMessage("Subscription deletion failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`text-center`}>
      <div className="d-flex flex-column justify-content-center align-items-center vh-100">
        <div className="card mb-3 p-3 w-25">
          <h2>Manage Subscription</h2>
          <div className="mb-3">
            <label htmlFor="recommender" className="form-label">
              Select Recommender:
            </label>
            <select
              id="recommender"
              className="form-select"
              value={selectedRecommender}
              onChange={(e) => setSelectedRecommender(e.target.value)}
              required
            >
              <option value="">Select a Recommender</option>
              {recommenders.map((recommender) => (
                <option key={recommender} value={recommender}>
                  {recommender}
                </option>
              ))}
            </select>
          </div>
          <div className="mb-3">
            <label htmlFor="frequency" className="form-label">
              Select Frequency:
            </label>
            <select
              id="frequency"
              className="form-select"
              value={frequency}
              onChange={(e) => setFrequency(e.target.value)}
              required
            >
              <option value="">Select Frequency</option>
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>
          <div className="mb-3">
            <label htmlFor="numRecommendations" className="form-label">
              Number of Recommendations:
            </label>
            <input
              type="number"
              id="numRecommendations"
              className="form-control"
              value={numRecommendations}
              onChange={(e) =>
                setNumRecommendations(
                  Math.min(Math.max(parseInt(e.target.value), 1), 5)
                )
              }
              required
            />
          </div>
          {subscription ? (
            <button
              className="btn btn-primary"
              onClick={handleEditSubscription}
              disabled={loading}
            >
              Edit Subscription
            </button>
          ) : (
            <button
              className="btn btn-success"
              onClick={handleSubscribe}
              disabled={loading}
            >
              Subscribe
            </button>
          )}
          {message && (
            <div className={`alert ${message.startsWith("Error") ? "alert-danger" : "alert-success"} alert-dismissible fade show mt-3`} role="alert">
              {message}
              <button
                type="button"
                className="btn-close"
                data-bs-dismiss="alert"
                aria-label="Close"
                onClick={() => setMessage("")}
              ></button>
            </div>
          )}
        </div>
        <div className="card mb-3 p-3 w-25">
          <h2>Current Subscription</h2>
          {subscription ? (
            <div>
              <p>
                <strong>Email:</strong> {subscription.email}
              </p>
              <p>
                <strong>Recommender:</strong> {subscription.recommender}
              </p>
              <p>
                <strong>Frequency:</strong> {subscription.frequency}
              </p>
              <p>
                <strong>Number of Recommendations:</strong>{" "}
                {subscription.num_recommendations}
              </p>
              <button
                className="btn btn-danger"
                onClick={handleDeleteSubscription}
                disabled={loading}
              >
                Delete Subscription
              </button>
            </div>
          ) : (
            <p>No active subscriptions</p>
          )}
        </div>
        <div className="text-center">
          <button className="btn btn-danger" onClick={handleBack}>
            Back
          </button>
        </div>
      </div>
    </div>
  );
}

export default ManageSubscription;
