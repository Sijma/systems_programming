import React, { useState, useEffect } from "react";
import { getRecommendation, getRecommenders } from "../api"; // Import the API functions

function GetRecommendation({ setShowGetRecommendation }) {
  const [generators, setGenerators] = useState([]); // State for generator options
  const [selectedGenerator, setSelectedGenerator] = useState(""); // State for selected generator
  const [amount, setAmount] = useState(1); // State for the number of recommendations
  const [recommendations, setRecommendations] = useState([]); // State for recommendations
  const [loading, setLoading] = useState(false); // State to track loading state
  const [message, setMessage] = useState(""); // State for messages (e.g., success, error)

  const columns = recommendations.length > 0 ? Object.keys(recommendations[0]) : [];

  useEffect(() => {
    // Fetch the list of generators from API when the component mounts
    getGeneratorOptions();
  }, []);

  const getGeneratorOptions = async () => {
    try {
      // Call the getRecommenders function from api.js to fetch the list of generators
      const response = await getRecommenders();
      setGenerators(response); // Set the list of generators in state
    } catch (error) {
      console.error("Error fetching generators:", error);
    }
  };

  const handleGetRecommendation = async () => {
  setLoading(true);
  try {
    // Call the getRecommendation function from api.js to get recommendations
    const response = await getRecommendation(selectedGenerator, amount);
    setRecommendations(response.selections); // Update recommendations with response.selections
    setMessage("Recommendations fetched successfully");
  } catch (error) {
    console.error("Error fetching recommendations:", error);
    setMessage("Error: Recommendations fetch failed");
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="text-center">
      <div className="d-flex flex-column justify-content-center align-items-center vh-100">
        <div className="card mb-3 p-3 w-50">
          <h2>Get Recommendations</h2>
          <div className="mb-3">
            <label htmlFor="generator" className="form-label">
              Select Generator:
            </label>
            <select
              id="generator"
              className="form-select"
              value={selectedGenerator}
              onChange={(e) => setSelectedGenerator(e.target.value)}
              required
            >
              <option value="">Select a Generator</option>
              {generators.map((generator) => (
                <option key={generator} value={generator}>
                  {generator}
                </option>
              ))}
            </select>
          </div>
          <div className="mb-3">
            <label htmlFor="amount" className="form-label">
              Number of Recommendations:
            </label>
            <input
              type="number"
              id="amount"
              className="form-control"
              value={amount}
              onChange={(e) => setAmount(Math.min(Math.max(parseInt(e.target.value), 1), 5))}
              required
            />
          </div>
          <button
            className="btn btn-primary"
            onClick={handleGetRecommendation}
            disabled={loading}
          >
            Get Recommendations
          </button>
          <button
            className="btn btn-danger mt-3"
            onClick={() => setShowGetRecommendation(false)}
          >
            Back
          </button>
          {message && (
            <div
              className={`alert ${
                message.startsWith("Error") ? "alert-danger" : "alert-success"
              } alert-dismissible fade show mt-3`}
              role="alert"
            >
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
        {recommendations.length > 0 && (
          <div className="card mb-3 p-3 w-75">
            <h2>Recommendations</h2>
            <table className="table table-bordered">
              <thead>
                <tr>
                  {columns.map((column) => (
                    <th key={column}>{column}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {recommendations.map((recommendation, index) => (
                  <tr key={index}>
                    {columns.map((column) => (
                      <td key={column}>{recommendation[column]}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default GetRecommendation;
