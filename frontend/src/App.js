import React, { useEffect, useState } from "react";
import $ from "jquery";

function App() {
  const [data, setData] = useState("");

  useEffect(() => {
    $.get(`http://localhost:5000/api/list-recommenders`, (response) => {
      setData(response);
    });
  }, []);

  return (
    <div className="App">
      <h1>Hello React App</h1>
      <p>Data from Flask API: {data}</p>
    </div>
  );
}

export default App;
