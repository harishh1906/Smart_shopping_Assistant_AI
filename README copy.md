# Smart Shopping Assistant with AI - Setup Instructions


This is a Flask-based AI-powered shopping assistant that compares clothing product prices across platforms (Amazon, Flipkart, etc.) using a MySQL database.

---

## System Requirements

- Python 3.8+
- MySQL Server & MySQL Workbench
- Git (optional)

---


# STEPExtract the ZIP to a folder 

- (e.g., `Smart_shopping_Assistant_AI/`)


## 🐍 2. Set Up Python Environment

###  Create Virtual Environment 


cd Smart_shopping_Assistant_AI
python -m venv venv

# Activate it:

venv\Scripts\activate

###  Install Required Packages


- pip install -r requirements.txt

- If `requirements.txt` is missing, you can create it (on your dev machine):

- pip freeze > requirements.txt


##  3. Set Up MySQL Database

###  Install MySQL
- Download and install MySQL Server and MySQL Workbench

###  Import the Database Dump ( 2 options )

# option 1 


# Import the Project Database

Download GitHub project ZIP and extract it.

Open MySQL Workbench.

Go to File → Open SQL Script

Open the file shopping_db.sql

Click the ⚡ Run (Execute) button.

✅ This will create the shopping_db database with amazon_products and users tables. 

# option 2

###  Create the Database

Open MySQL terminal or MySQL Workbench and run:

# In sql

- CREATE DATABASE shopping_db;

# Import the Database Dump

- Ensure `shopping_db.sql` is in the project folder. Then run:


- mysql -u root -p shopping_db < shopping_db.sql

- Enter the MySQL root password when prompted
- This will create `amazon_products` and `users` tables with all the data


## 4. Update Database Config in Flask App

In `app.py` (or your config file), make sure your MySQL connection settings match your environment:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql_password' 
app.config['MYSQL_DB'] = 'shopping_db'

##  5. Run the Flask App

### A. Activate your virtual environment (if not already):

venv\Scripts\activate

### B. Start the app:

- python app.py


Visit [http://localhost:5000](http://localhost:5000) in your browser 

---

## 📦 Project Structure Overview
```
Smart_shopping_Assistant_AI/
├── app.py                # Flask application
├── shopping_db.sql       # SQL dump of the MySQL database
├── templates/            # HTML templates
├── static/               # CSS/JS/Images
├── requirements.txt      # Python dependencies
├── README copy.md             # This file
└── 

