# Smart Shopping Assistant - Setup Guide

## Overview
This application has been fixed and is now ready to run. All hardcoded credentials have been moved to environment variables, and all import/syntax errors have been resolved.

## Fixed Issues

### 1. **app.py (Flask Application)**
   - ✅ Moved hardcoded database credentials to environment variables
   - ✅ Fixed double `cursor.close()` issue in `generate_description` route
   - ✅ Added missing imports (os, dotenv)
   - ✅ Added proper cursor initialization (`cursor = None`) in all routes
   - ✅ Added proper error handling with `if cursor:` checks in finally blocks

### 2. **requirements.txt**
   - ✅ Added missing dependencies:
     - `flask-mysqldb`
     - `flask-bcrypt`
     - `python-dotenv`

### 3. **.env File**
   - ✅ Created with proper environment variables:
     - Flask configuration (FLASK_SECRET_KEY)
     - MySQL connection details (MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
     - Node.js configuration (SECRET_KEY, DB_PASSWORD, PORT)

### 4. **server.js (Node.js/Express)**
   - ✅ Updated to use environment variables for database connection
   - ✅ Added fallback defaults for all environment variables
   - ✅ Proper error handling for database connection
   - ✅ JWT secret key now uses environment variable

### 5. **index.js (Alternative Node.js Server)**
   - ✅ Removed non-existent `./routes/auth` import
   - ✅ Added basic health check endpoint
   - ✅ Fixed CORS import (added cors to package.json)

### 6. **package.json**
   - ✅ Added `cors` dependency

### 7. **.gitignore**
   - ✅ Updated with comprehensive patterns for Python, Node.js, and sensitive files

## Running the Application

### Prerequisites
- Python 3.x
- Node.js and npm
- MySQL server running on localhost

### 1. Set up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Set up Node.js Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

Edit the `.env` file and update the database credentials:

```env
MYSQL_PASSWORD=your_mysql_password_here
```

### 4. Set up Database

```bash
# Import the database schema
mysql -u root -p < shopping_db.sql
```

### 5. Run the Flask Application

```bash
python app.py
```

The Flask app will run on `http://localhost:5000`

### 6. (Optional) Run Node.js Server

If you want to use the Node.js/Express server for JWT-based API:

```bash
node server.js
```

This will run on the port specified in `.env` (default: 5000)

Or use the simpler index.js:

```bash
node index.js
```

This will run on port 3000.

## Application Structure

- **app.py** - Main Flask application with user authentication and product search
- **server.js** - Node.js/Express server with JWT authentication and recommendations API
- **index.js** - Alternative simple Node.js server with CORS support
- **templates/** - Jinja2 templates for the web interface
- **static/** - CSS and static assets
- **.env** - Environment variables (DO NOT commit to git)

## Security Notes

- ⚠️ The `.env` file is excluded from git via `.gitignore`
- ⚠️ Default credentials in `.env` should be changed for production
- ⚠️ SECRET_KEY should be regenerated for production use
- ⚠️ Debug mode should be disabled in production

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| FLASK_SECRET_KEY | Flask session secret | Generated key |
| MYSQL_HOST | MySQL server host | localhost |
| MYSQL_USER | MySQL username | root |
| MYSQL_PASSWORD | MySQL password | (required) |
| MYSQL_DB | Database name | shopping_db |
| SECRET_KEY | JWT secret for Node.js | Generated key |
| DB_PASSWORD | Alias for MYSQL_PASSWORD | (required) |
| PORT | Node.js server port | 5000 |

## Testing the Application

1. Start the Flask application
2. Navigate to `http://localhost:5000/register`
3. Register a new user account
4. Login with the registered credentials
5. Search for products
6. View product details

## Troubleshooting

### Database Connection Error
- Ensure MySQL is running: `sudo service mysql status`
- Verify credentials in `.env` file
- Check if database exists: `mysql -u root -p -e "SHOW DATABASES;"`

### Import Errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Node.js Errors
- Reinstall node modules: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version` (should be 14+)

## Next Steps

For production deployment:
1. Use a production WSGI server (gunicorn, uWSGI) for Flask
2. Use a process manager (PM2) for Node.js
3. Set up nginx as a reverse proxy
4. Use a production database (not localhost)
5. Enable SSL/TLS certificates
6. Implement rate limiting
7. Add logging and monitoring
