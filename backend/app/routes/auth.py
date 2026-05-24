from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

# We will inject the db_service after blueprint initialization
db_service = None

def init_auth(db_svc):
    global db_service
    db_service = db_svc

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not name or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            # Check if user already exists
            existing_user = db_service.execute_query(
                "SELECT * FROM users WHERE email = %s", (email,), fetch='one'
            )

            if existing_user:
                flash('Email already registered.', 'danger')
                return redirect(url_for('auth.register'))

            # Insert user record
            db_service.execute_query(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed_password),
                fetch='none'
            )
            flash('Registration successful! Please login.', 'success')
            logger.info(f"✅ User registered: {email}")
            return redirect(url_for('auth.login'))

        except Exception as e:
            flash(f'Database error occurred during registration: {e}', 'danger')
            logger.error(f"❌ Registration DB Exception: {e}")

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # If already logged in, redirect home
    if session.get('logged_in'):
        return redirect(url_for('products.home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Please fill in all credentials.', 'danger')
            return redirect(url_for('auth.login'))

        try:
            user = db_service.execute_query(
                "SELECT * FROM users WHERE email = %s", (email,), fetch='one'
            )

            if user and bcrypt.check_password_hash(user['password'], password):
                session['logged_in'] = True
                session['user_id'] = user['user_id']
                session['name'] = user['name']
                session.permanent = True
                
                flash(f"Welcome back, {user['name']}!", 'success')
                logger.info(f"✅ Login successful for user: {email}")
                return redirect(url_for('products.home'))
            else:
                flash('Invalid email or password.', 'danger')
                logger.warning(f"❌ Invalid login attempt for: {email}")

        except Exception as e:
            flash(f'Database error during login: {e}', 'danger')
            logger.error(f"❌ Login DB Exception: {e}")

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    logger.info("✅ User logged out, session cleared.")
    return redirect(url_for('auth.login'))
