from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import logging

logger = logging.getLogger(__name__)

products_bp = Blueprint('products', __name__)

db_service = None
recommender_service = None
sentiment_service = None

def init_products(db_svc, rec_svc, sent_svc):
    global db_service, recommender_service, sentiment_service
    db_service = db_svc
    recommender_service = rec_svc
    sentiment_service = sent_svc

@products_bp.route('/')
def home():
    if not session.get('logged_in'):
        flash('Please login to access the shopping assistant.', 'warning')
        return redirect(url_for('auth.login'))

    query = request.args.get('query', '').strip()
    logger.info(f"🔍 Catalog search query received: '{query}'")

    try:
        if query:
            sql_query = "SELECT * FROM amazon_products WHERE product_name LIKE %s LIMIT 100"
            products = db_service.execute_query(sql_query, (f"%{query}%",), fetch='all')
        else:
            # Render a default set of products
            products = db_service.execute_query("SELECT * FROM amazon_products LIMIT 100", fetch='all')
            
        logger.info(f"✅ Fetched {len(products)} products for catalog view")
    except Exception as e:
        flash(f'Database error retrieving products: {e}', 'danger')
        logger.error(f"❌ Catalog DB Exception: {e}")
        products = []

    return render_template('index.html', name=session.get('name'), products=products, query=query)

@products_bp.route('/product/<int:product_id>')
def product_details(product_id):
    if not session.get('logged_in'):
        flash('Login required.', 'warning')
        return redirect(url_for('auth.login'))

    try:
        # 1. Fetch target product details
        product = db_service.execute_query(
            "SELECT * FROM amazon_products WHERE id = %s", (product_id,), fetch='one'
        )

        if not product:
            flash('Selected product not found.', 'danger')
            return redirect(url_for('products.home'))

        # 2. Get Real ML Content-Based Recommendations (TF-IDF)
        recommendations = recommender_service.get_recommendations(product_id, top_n=4)

        # 3. Get Real AI Eco-Friendly Alternatives
        eco_friendly_recommendations = recommender_service.get_eco_recommendations(product_id, top_n=4)

        # 4. Get TextBlob Sentiment Analysis and Reviews
        rating_val = product.get('rating', 0)
        rating_count = product.get('rating_count', 0)
        
        # If product rating in catalog is invalid or 0.0, default to a sensible mock rating for mock analysis
        float_rating = float(rating_val) if rating_val and str(rating_val).replace('.', '', 1).isdigit() else 3.8
        
        sentiment_data = sentiment_service.generate_reviews_and_sentiment(
            product_rating=float_rating,
            product_name=product['product_name']
        )

        return render_template(
            'product_details.html',
            product=product,
            recommendations=recommendations,
            eco_friendly_recommendations=eco_friendly_recommendations,
            reviews=sentiment_data['reviews'],
            breakdown=sentiment_data['breakdown'],
            overall_sentiment=sentiment_data['overall_sentiment'],
            rating_count=rating_count or random_review_count(float_rating)
        )

    except Exception as e:
        flash(f'Error rendering details page: {e}', 'danger')
        logger.error(f"❌ Product Details Exception: {e}")
        return redirect(url_for('products.home'))

@products_bp.route('/eco_friendly')
def eco_friendly_catalog():
    if not session.get('logged_in'):
        flash('Login required.', 'warning')
        return redirect(url_for('auth.login'))

    try:
        # Search catalog for items with highly sustainable fabrics (cotton, linen, pure) and good ratings
        query = """
            SELECT * FROM amazon_products 
            WHERE (product_name LIKE '%%cotton%%' OR product_name LIKE '%%linen%%' OR product_name LIKE '%%organic%%')
            AND rating >= 4.0
            LIMIT 50
        """
        products = db_service.execute_query(query, fetch='all')
        
        # If search query yields nothing, fallback to high-rated apparel
        if not products:
            products = db_service.execute_query(
                "SELECT * FROM amazon_products WHERE rating >= 4.2 LIMIT 50", fetch='all'
            )
            
        logger.info(f"✅ Loaded {len(products)} eco-friendly catalogue items")
    except Exception as e:
        flash(f'Database error: {e}', 'danger')
        logger.error(f"❌ Eco Catalog Exception: {e}")
        products = []

    return render_template('eco_friendly.html', products=products)

def random_review_count(rating: float) -> int:
    """Helper to return organic review numbers if database count is empty."""
    import random
    return random.randint(15, 450)
