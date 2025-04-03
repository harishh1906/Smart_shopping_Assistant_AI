import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const AuthPage = ({ type }) => {
  const [formData, setFormData] = useState({ name: "", email: "", password: "" });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const url = type === "register" ? "http://localhost:5000/register" : "http://localhost:5000/login";
    
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      if (response.ok) {
        alert(data.message);
        if (type === "login") {
          localStorage.setItem("token", data.token);
          navigate("/dashboard");
        } else {
          navigate("/login");
        }
      } else {
        alert(data.error);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>{type === "register" ? "Register" : "Login"}</h2>
      <form onSubmit={handleSubmit}>
        {type === "register" && (
          <input type="text" name="name" placeholder="Name" onChange={handleChange} required />
        )}
        <br />
        <input type="email" name="email" placeholder="Email" onChange={handleChange} required />
        <br />
        <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
        <br />
        <button type="submit">{type === "register" ? "Register" : "Login"}</button>
      </form>
    </div>
  );
};

export default AuthPage;
