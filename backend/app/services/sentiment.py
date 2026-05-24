import logging
import random
from textblob import TextBlob

logger = logging.getLogger(__name__)

class SentimentService:
    """Service utilizing TextBlob to analyze and generate dynamic review sentiments."""

    def __init__(self):
        # Professional dynamic reviews matched with products
        self.review_bank = {
            'high': [
                "Absolutely love this item! The fabric is incredibly soft, breathable, and fits perfectly. Highly recommended!",
                "Amazing quality. It looks premium and holds up well after multiple washes. Exceeded my expectations.",
                "Perfect styling, very elegant, and comfortable. Definitely worth the price. Five stars!",
                "Great purchase. The details are beautiful, and it's extremely cozy to wear daily.",
                "Very stylish design. I've received so many compliments when wearing this. Will buy another colour!"
            ],
            'medium': [
                "The product is decent for the price, but the sizing runs slightly larger than standard charts.",
                "Okay quality. The fabric is comfortable, though the colors look a bit lighter than the catalog pictures.",
                "It's a reasonable everyday clothing item. Average styling and finish. Fair value.",
                "Slightly slower delivery, but the shirt itself is alright. Standard comfort and fabric weight.",
                "Decent overall. Nothing mind-blowing, but fits fine and looks presentable."
            ],
            'low': [
                "Disappointed with the quality. The fabric feels cheap, rough, and the stitching is already coming loose.",
                "Poor sizing. It shrank significantly after the very first wash, and is now unwearable.",
                "Not as described. The color is completely different from the website and the fit is highly awkward.",
                "Highly overpriced for this tier of material. I do not recommend buying this brand.",
                "Extremely uncomfortable. The material is very stiff, scratchy, and has a weird chemical smell."
            ]
        }

    def generate_reviews_and_sentiment(self, product_rating: float, product_name: str) -> dict:
        """
        Generates 3-4 realistic reviews tailored to the product's rating.
        Runs TextBlob sentiment classification on each and aggregates overall statistics.
        
        :param product_rating: Catalog rating float (0.0 to 5.0).
        :param product_name: Name of the product to insert context.
        :return: Dictionary containing list of reviews with individual scores and final sentiment breakdown.
        """
        try:
            rating = float(product_rating or 0.0)
            
            # Determine sentiment category
            if rating >= 4.0:
                sentiment_type = 'high'
            elif rating >= 3.0:
                sentiment_type = 'medium'
            else:
                sentiment_type = 'low'
            
            # Choose a combination of reviews to represent a normal distribution
            selected_templates = []
            if sentiment_type == 'high':
                # Mostly positive reviews, maybe one neutral
                selected_templates += random.sample(self.review_bank['high'], 2)
                selected_templates.append(random.choice(self.review_bank['medium']))
            elif sentiment_type == 'medium':
                # Balanced positive, neutral, and negative
                selected_templates.append(random.choice(self.review_bank['high']))
                selected_templates.append(random.choice(self.review_bank['medium']))
                selected_templates.append(random.choice(self.review_bank['low']))
            else:
                # Mostly negative reviews, maybe one neutral
                selected_templates += random.sample(self.review_bank['low'], 2)
                selected_templates.append(random.choice(self.review_bank['medium']))

            reviews = []
            positive_count = 0
            neutral_count = 0
            negative_count = 0
            
            for text in selected_templates:
                # Personalize review by injecting product details occasionally
                clean_text = text.replace("this item", f"this {product_name}").replace("The product", f"The {product_name}")
                
                # Analyze using TextBlob
                blob = TextBlob(clean_text)
                polarity = blob.sentiment.polarity       # Range: -1.0 to 1.0
                subjectivity = blob.sentiment.subjectivity # Range: 0.0 to 1.0
                
                # Classify label
                if polarity > 0.15:
                    label = "Positive"
                    positive_count += 1
                elif polarity < -0.15:
                    label = "Negative"
                    negative_count += 1
                else:
                    label = "Neutral"
                    neutral_count += 1
                
                reviews.append({
                    'author': self._generate_random_author(),
                    'comment': clean_text,
                    'polarity': round(polarity, 2),
                    'subjectivity': round(subjectivity, 2),
                    'label': label
                })

            # Calculate composite metrics
            total = len(reviews)
            breakdown = {
                'positive': round((positive_count / total) * 100) if total > 0 else 0,
                'neutral': round((neutral_count / total) * 100) if total > 0 else 0,
                'negative': round((negative_count / total) * 100) if total > 0 else 0,
            }
            
            # Formulate overall conclusion
            if positive_count > negative_count and positive_count > neutral_count:
                overall = "Mostly Positive"
            elif negative_count > positive_count and negative_count > neutral_count:
                overall = "Mostly Critical"
            else:
                overall = "Mixed / Neutral"

            logger.info(f"✅ Executed TextBlob review analysis for product: '{product_name}'")
            return {
                'reviews': reviews,
                'breakdown': breakdown,
                'overall_sentiment': overall
            }

        except Exception as e:
            logger.error(f"❌ Error compiling review sentiments: {e}")
            return {
                'reviews': [],
                'breakdown': {'positive': 0, 'neutral': 0, 'negative': 0},
                'overall_sentiment': "Unavailable"
            }

    def _generate_random_author(self) -> str:
        """Helper to yield mock customer names for authentic review layouts."""
        names = ["Siddharth Sharma", "Aisha Patel", "Vikram Singh", "Priya Nair", "Rohan Mehta", "Neha Gupta", "Amit Verma", "Anjali Rao"]
        return random.choice(names)
