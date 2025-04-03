const express = require("express");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const db = require("../db");
require("dotenv").config();

const router = express.Router();

// User Registration
router.post("/register", async (req, res) => {
    const { name, email, password } = req.body;

    if (!name || !email || !password) {
        return res.status(400).json({ message: "All fields are required" });
    }

    try {
        // Check if email already exists
        db.query("SELECT * FROM users WHERE email = ?", [email], async (err, results) => {
            if (results.length > 0) {
                return res.status(400).json({ message: "Email already exists" });
            }

            // Hash password
            const hashedPassword = await bcrypt.hash(password, 10);

            // Insert user
            db.query("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                [name, email, hashedPassword], (err, result) => {
                    if (err) {
                        return res.status(500).json({ message: "Database error", error: err });
                    }
                    res.status(201).json({ message: "User registered successfully!" });
                }
            );
        });
    } catch (error) {
        res.status(500).json({ message: "Server error", error });
    }
});

// User Login
router.post("/login", (req, res) => {
    const { email, password } = req.body;

    if (!email || !password) {
        return res.status(400).json({ message: "All fields are required" });
    }

    try {
        db.query("SELECT * FROM users WHERE email = ?", [email], async (err, results) => {
            if (results.length === 0) {
                return res.status(400).json({ message: "Invalid credentials" });
            }

            const user = results[0];

            // Compare password
            const isMatch = await bcrypt.compare(password, user.password);
            if (!isMatch) {
                return res.status(400).json({ message: "Invalid credentials" });
            }

            // Generate JWT Token
            const token = jwt.sign({ userId: user.user_id, email: user.email }, process.env.SECRET_KEY, { expiresIn: "1h" });

            res.status(200).json({ message: "Login successful!", token });
        });
    } catch (error) {
        res.status(500).json({ message: "Server error", error });
    }
});

module.exports = router;
