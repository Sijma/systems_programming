import React, { useEffect, useState } from 'react';
import $ from 'jquery';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Fetch data from Flask API on component mount
    $.get('/api/', (data) => {
      setMessage(data);
    });
  }, []);

  return (
    <div className="App">
      <h1>Hello from React!</h1>
      <p>Message from Flask API:</p>
      <p>{message}</p>
    </div>
  );
}

export default App;
