from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import MySQLdb.cursors
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.secret_key = '0b44ca19022clea18bb659b30fdf133a0fbc822f115c59cc64c58f2ccb8c71a5'
app.config['SESSION_PERMANENT'] = True

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Juneoct@9'
app.config['MYSQL_DB'] = 'shopping_db'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cursor = None

        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('Email already registered.', 'danger')
                return redirect(url_for('register'))

            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                           (name, email, hashed_password))
            mysql.connection.commit()
            flash('Registration successful!', 'success')
        except MySQLdb.Error as e:
            flash(f'Database error: {e}', 'danger')
        finally:
            if cursor:
                cursor.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user:
                stored_hash = user['password']
                
                if bcrypt.check_password_hash(stored_hash, password):
                    session['logged_in'] = True
                    session['user_id'] = user['user_id']
                    session['name'] = user['name']
                    session.permanent = True
                    
                    flash('Login successful!', 'success')
                    print(f"✅ Redirecting to home | Session Data: {session}")
                    return redirect(url_for('home'))
                else:
                    flash('Invalid credentials.', 'danger')
                    print("❌ Password incorrect")
            else:
                flash('User not found.', 'danger')
                print("❌ User does not exist")

        except MySQLdb.Error as e:
            flash(f'Database error: {e}', 'danger')
            print(f"❌ Database error: {e}")
        finally:
            cursor.close()
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/')
def home():
    if 'logged_in' in session:
        print(f"User {session['name']} is logged in.")

        query = request.args.get('query', '').strip()
        print(f"🔍 Search Query: '{query}'")

        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            if query:
                sql_query = """
                    SELECT * FROM amazon_products 
                    WHERE product_name LIKE %s
                    LIMIT 1000
                """
                params = (f"%{query}%",)
                print(f"📌 Executing Query: {sql_query} with {params}")
                cursor.execute(sql_query, params)
            else:
                cursor.execute("SELECT * FROM amazon_products LIMIT 1000")

            products = cursor.fetchall()
            print(f"✅ Retrieved {len(products)} products")
        except MySQLdb.Error as e:
            flash(f'Database error: {e}', 'danger')
            print(f"❌ Database Error: {e}")
            products = []
        finally:
            if cursor:
                cursor.close()

        return render_template('index.html', name=session['name'], products=products, query=query)

    print("User not logged in, redirecting to login.")
    flash('Login required.', 'warning')
    return redirect(url_for('login'))

@app.route('/product/<int:product_id>')
def product_details(product_id):
    print(f"Fetching product details for ID: {product_id}")
    cursor = None

    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM amazon_products WHERE id = %s", (product_id,))
        product = cursor.fetchone()

        if not product:
            flash('Product not found.', 'danger')
            return redirect(url_for('home'))

        #  AI-generated description
        ai_description = f"The {product['product_name']} is a stylish {product['product_tag']} from {product['brand_name'] or 'a leading brand'}, perfect for modern needs."

        #  Similar products
        cursor.execute("SELECT * FROM amazon_products WHERE id != %s ORDER BY RAND() LIMIT 5", (product_id,))
        recommendations = cursor.fetchall()

        #  Eco-friendly: mocked using high discounts
        cursor.execute("SELECT * FROM amazon_products WHERE discount_percent > 50 AND id != %s ORDER BY RAND() LIMIT 5", (product_id,))
        eco_friendly_recommendations = cursor.fetchall()

        return render_template(
            'product_details.html',
            product=product,
            recommendations=recommendations,
            eco_friendly_recommendations=eco_friendly_recommendations,
            ai_description=ai_description
        )

    except MySQLdb.Error as e:
        flash(f'Database error: {e}', 'danger')
        return redirect(url_for('home'))
    finally:
        if cursor:
            cursor.close()

@app.route('/generate_description/<int:product_id>')
def generate_description(product_id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT product_name, product_tag FROM amazon_products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        cursor.close()

        if not product:
            return jsonify({'error': 'Product not found'}), 404

        
        description = f"The {product['product_name']} is a premium {product['product_tag']} that offers style and comfort."

        return jsonify({'description': description})
    
    except Exception as e:
        print("Error in /generate_description route:", e)
        return jsonify({'error': 'Server error'}), 500

    finally:
        if cursor:
            cursor.close()

if __name__ == '__main__': 
    app.run(debug=True)
