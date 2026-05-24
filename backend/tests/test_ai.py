import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Align python imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app
from app.config import Config
from app.services.recommender import RecommendationService
from app.services.sentiment import SentimentService

class TestAIComponents(unittest.TestCase):
    """Unit test suite validating content-based recommendation logic and TextBlob sentiments."""

    def setUp(self):
        # Override config details for testing
        class TestConfig(Config):
            TESTING = True
            SECRET_KEY = 'test_secret_key'
            
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        
        # Instantiate services with mock DB
        self.mock_db = MagicMock()
        self.recommender = RecommendationService(self.mock_db)
        self.sentiment = SentimentService()

    def test_recommender_tf_idf_similarity(self):
        """Verifies TF-IDF cosine similarity matrices are computed correctly on categories."""
        # 1. Mock DB query outputs
        self.mock_db.execute_query.side_effect = [
            # Target product
            {
                'id': 1,
                'product_name': 'Pure Cotton Slim T-Shirt',
                'brand_name': 'Nike',
                'product_tag': 'tshirts',
                'brand_tag': 'nike'
            },
            # Category candidate list
            [
                {
                    'id': 2,
                    'product_name': 'Pure Cotton Slim Tee',
                    'brand_name': 'Nike',
                    'product_tag': 'tshirts',
                    'brand_tag': 'nike'
                },
                {
                    'id': 3,
                    'product_name': 'Synthetic Sports Cap',
                    'brand_name': 'Puma',
                    'product_tag': 'tshirts',
                    'brand_tag': 'puma'
                }
            ]
        ]

        # 2. Get recommendations
        recommendations = self.recommender.get_recommendations(product_id=1, top_n=2)
        
        # 3. Assert results
        self.assertEqual(len(recommendations), 2)
        # The 'Classic Pure Cotton Tee' should have a higher similarity score because it shares "pure", "cotton", "t-shirt" attributes with target.
        self.assertEqual(recommendations[0]['id'], 2)
        self.assertTrue('similarity_score' in recommendations[0])

    def test_sentiment_text_classification(self):
        """Verifies TextBlob sentiment reviews yield correct polarity values."""
        # Run classification on mock rating
        data = self.sentiment.generate_reviews_and_sentiment(product_rating=4.5, product_name="Nike Joggers")
        
        # Assert structure
        self.assertTrue('reviews' in data)
        self.assertTrue('breakdown' in data)
        self.assertEqual(data['overall_sentiment'], "Mostly Positive")
        self.assertGreaterEqual(len(data['reviews']), 2)
        
        # Verify TextBlob metrics are computed as floats in range [-1.0, 1.0] and [0.0, 1.0]
        first_review = data['reviews'][0]
        self.assertIsInstance(first_review['polarity'], float)
        self.assertTrue(-1.0 <= first_review['polarity'] <= 1.0)
        self.assertTrue(0.0 <= first_review['subjectivity'] <= 1.0)

    @patch('app.routes.ai.db_service')
    def test_async_description_generator_api(self, mock_db):
        """Verifies that async AI descriptions serve dynamic sentences."""
        mock_db.execute_query.return_value = {
            'product_name': 'Linen Summer Dress',
            'brand_name': 'Zara',
            'product_tag': 'dresses',
            'sizes': 'S, M, L',
            'rating': 4.6
        }
        
        response = self.client.get('/generate_description/5')
        self.assertEqual(response.status_code, 200)
        
        json_data = response.get_json()
        self.assertEqual(json_data['product_id'], 5)
        self.assertIn('Linen Summer Dress', json_data['description'])
        self.assertIn('Zara', json_data['description'])

if __name__ == '__main__':
    unittest.main()
