import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import AuthPage from "./components/AuthPage";
import Dashboard from "./components/Dashboard";

const Home = () => (
  <div style={{ textAlign: "center", marginTop: "50px" }}>
    <h1>Welcome to Smart Shopping Assistant</h1>
    <p><a href="/register">Register</a> or <a href="/login">Login</a> to continue.</p>
  </div>
);

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<AuthPage type="register" />} />
        <Route path="/login" element={<AuthPage type="login" />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
};

export default App;
