import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Align python imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app
from app.config import Config

class TestAuthRoutes(unittest.TestCase):
    """Unit test suite validating user session authentication flows."""
    
    def setUp(self):
        # Override config details for testing
        class TestConfig(Config):
            TESTING = True
            SECRET_KEY = 'test_secret_key'
            
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    @patch('app.routes.auth.db_service')
    def test_register_page_loads(self, mock_db):
        """Verifies registration GET interface serves correctly."""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create Account', response.data)

    @patch('app.routes.auth.db_service')
    def test_login_page_loads(self, mock_db):
        """Verifies login GET interface serves correctly."""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In', response.data)

    @patch('app.routes.auth.db_service')
    @patch('app.routes.auth.bcrypt')
    def test_successful_login(self, mock_bcrypt, mock_db):
        """Verifies successful login flow sets session state."""
        # Setup mock db query
        mock_db.execute_query.return_value = {
            'user_id': 1,
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'hashed_password'
        }
        mock_bcrypt.check_password_hash.return_value = True
        
        # POST credentials
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'secure_password'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back, Test User!', response.data)
        
        # Verify session state using client
        with self.client.session_transaction() as sess:
            self.assertTrue(sess.get('logged_in'))
            self.assertEqual(sess.get('name'), 'Test User')

    @patch('app.routes.auth.db_service')
    def test_invalid_login_missing_fields(self, mock_db):
        """Verifies that empty login parameters trigger warnings."""
        response = self.client.post('/login', data={
            'email': '',
            'password': ''
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please fill in all credentials.', response.data)

    def test_logout_clears_session(self):
        """Verifies session clearance upon logout calls."""
        # Inject custom session variable
        with self.client.session_transaction() as sess:
            sess['logged_in'] = True
            sess['name'] = 'Active User'
            
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out.', response.data)
        
        # Check session is cleared
        with self.client.session_transaction() as sess:
            self.assertFalse(sess.get('logged_in'))
            self.assertIsNone(sess.get('name'))

if __name__ == '__main__':
    unittest.main()
