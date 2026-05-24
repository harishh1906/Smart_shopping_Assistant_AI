import logging
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.services.db import DatabaseService

logger = logging.getLogger(__name__)

class RecommendationService:
    """Service providing content-based recommendations using TF-IDF & Cosine Similarity."""
    
    def __init__(self, db_service: DatabaseService):
        self.db = db_service
        self.eco_keywords = ['cotton', 'pure cotton', 'organic', 'linen', 'khadi', 'handwoven', 'jute', 'sustainable', 'hemp', 'bamboo']

    def get_recommendations(self, product_id: int, top_n: int = 5) -> list:
        """
        Fetches the top N most similar products in the same category using TF-IDF and Cosine Similarity.
        
        :param product_id: Primary key of the product.
        :param top_n: Number of recommendations to return.
        :return: List of recommended product dictionaries.
        """
        try:
            # 1. Fetch current product
            current_product = self.db.execute_query(
                "SELECT * FROM amazon_products WHERE id = %s", (product_id,), fetch='one'
            )
            if not current_product:
                return []

            category = current_product.get('product_tag')
            if not category:
                # Fallback to random if no category tag exists
                return self._get_random_fallback(product_id, top_n)

            # 2. Fetch all products of the same category
            candidate_products = self.db.execute_query(
                "SELECT * FROM amazon_products WHERE product_tag = %s AND id != %s LIMIT 1500",
                (category, product_id),
                fetch='all'
            )
            
            if not candidate_products or len(candidate_products) < 2:
                return self._get_random_fallback(product_id, top_n)

            # 3. Build corpus
            # Put the target product at the top of the list (index 0) for TF-IDF vectorization
            corpus = [current_product] + list(candidate_products)
            
            df = pd.DataFrame(corpus)
            # Create feature text using product metadata
            df['feature_text'] = (
                df['product_name'].fillna('') + ' ' + 
                df['brand_name'].fillna('') + ' ' + 
                df['brand_tag'].fillna('')
            ).str.lower()

            # 4. Compute TF-IDF & Cosine Similarity
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(df['feature_text'])
            
            # Match the first document (our target product) against all other candidates
            similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix).flatten()
            
            # Add similarity score to candidates
            df['similarity_score'] = similarity_scores
            
            # Filter out the target product (which is index 0)
            df_recs = df.iloc[1:].sort_values(by='similarity_score', ascending=False)
            
            # Return top N products
            recs = df_recs.head(top_n).to_dict(orient='records')
            
            logger.info(f"✅ Calculated similar recommendations for product ID: {product_id} in category '{category}'")
            return recs

        except Exception as e:
            logger.error(f"❌ Error computing ML recommendations: {e}")
            return self._get_random_fallback(product_id, top_n)

    def get_eco_recommendations(self, product_id: int, top_n: int = 5) -> list:
        """
        Returns eco-friendly green alternatives within the same category.
        Uses sustainability keyword matching and high-discount matching to rank alternatives.
        
        :param product_id: Primary key of the product.
        :param top_n: Number of recommendations to return.
        :return: List of eco-friendly product dictionaries.
        """
        try:
            # 1. Fetch current product
            current_product = self.db.execute_query(
                "SELECT * FROM amazon_products WHERE id = %s", (product_id,), fetch='one'
            )
            if not current_product:
                return []

            category = current_product.get('product_tag')
            if not category:
                category = ''

            # 2. Build a SQL search with sustainable fabric keywords
            keyword_clauses = " OR ".join(["product_name LIKE %s" for _ in self.eco_keywords])
            query = f"""
                SELECT * FROM amazon_products 
                WHERE product_tag = %s AND id != %s AND ({keyword_clauses}) 
                LIMIT 500
            """
            params = [category, product_id] + [f"%{kw}%" for kw in self.eco_keywords]
            
            candidates = self.db.execute_query(query, tuple(params), fetch='all')

            # Fallback if no matching sustainable materials are found in the category
            if not candidates or len(candidates) < 2:
                # Mock eco-friendly by looking at high discount / rating products in the same category
                candidates = self.db.execute_query(
                    """SELECT * FROM amazon_products 
                       WHERE product_tag = %s AND id != %s AND (discount_percent > 45 OR rating >= 4.0) 
                       LIMIT 100""",
                    (category, product_id),
                    fetch='all'
                )

            if not candidates:
                return self._get_random_fallback(product_id, top_n)

            # 3. Run Cosine Similarity to find the closest matches in sustainable variants
            corpus = [current_product] + list(candidates)
            df = pd.DataFrame(corpus)
            df['feature_text'] = (
                df['product_name'].fillna('') + ' ' + 
                df['brand_name'].fillna('')
            ).str.lower()

            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(df['feature_text'])
            similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix).flatten()
            
            df['similarity_score'] = similarity_scores
            df_recs = df.iloc[1:].sort_values(by=['similarity_score', 'rating'], ascending=[False, False])
            
            logger.info(f"✅ Generated eco-friendly recommendations for product ID: {product_id}")
            return df_recs.head(top_n).to_dict(orient='records')

        except Exception as e:
            logger.error(f"❌ Error getting eco-friendly recommendations: {e}")
            return self._get_random_fallback(product_id, top_n)

    def _get_random_fallback(self, product_id: int, limit: int = 5) -> list:
        """Helper fallback query to fetch random products when similarity matrix is sparse."""
        return self.db.execute_query(
            "SELECT * FROM amazon_products WHERE id != %s ORDER BY RAND() LIMIT %s",
            (product_id, limit),
            fetch='all'
        )
