// src/components/NotFound.js

import React from 'react';

function NotFound() {
  return (
    <div style={{
        position: "absolute",
        top: "45%",
        left: "50%",
        transform: "translate(-50%, -50%)",
      }}>
      <h1 style={{textAlign: "center"}}>404 - Page Not Found</h1>
      <h3 style={{textAlign: "center"}}>Sorry, the page you are looking for does not exist.</h3>
    </div>
  );
}

export default NotFound;
