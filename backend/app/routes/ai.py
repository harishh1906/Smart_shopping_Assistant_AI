from flask import Blueprint, jsonify
import logging

logger = logging.getLogger(__name__)

ai_bp = Blueprint('ai', __name__)
db_service = None

def init_ai(db_svc):
    global db_service
    db_service = db_svc

@ai_bp.route('/generate_description/<int:product_id>')
def generate_description(product_id):
    """
    Generates a dynamic, high-quality, simulated AI marketing copy using product details.
    Avoids boring placeholders and creates engaging product stories.
    """
    try:
        product = db_service.execute_query(
            "SELECT product_name, brand_name, product_tag, sizes, rating FROM amazon_products WHERE id = %s",
            (product_id,),
            fetch='one'
        )

        if not product:
            return jsonify({'error': 'Product details not found'}), 404

        name = product.get('product_name')
        brand = product.get('brand_name') or 'a leading fashion line'
        tag = product.get('product_tag') or 'apparel'
        sizes = product.get('sizes') or 'Standard'
        rating = float(product.get('rating', 0.0) or 3.8)

        # Assemble a dynamic marketing description based on the parameters
        sentences = [
            f"Step up your style with the premium {name} designed by the visionaries at {brand}.",
            f"Crafted with meticulous attention to detail, this premium {tag} is designed to offer maximum durability without compromising on modern style.",
            f"With high-fidelity tailoring, it is currently available in a versatile range of sizing choices: {sizes}."
        ]

        if rating >= 4.2:
            sentences.append("As an extremely popular customer choice, it enjoys high-acclaim and superior reviews for regular durability and comfortable daily wear.")
        else:
            sentences.append("Perfect for elevating your casual collection, it represents a versatile and budget-friendly choice for any wardrobe.")

        description = " ".join(sentences)

        logger.info(f"✅ Generated dynamic AI description for product: '{name}'")
        return jsonify({
            'product_id': product_id,
            'description': description
        })

    except Exception as e:
        logger.error(f"❌ Exception during AI description generation: {e}")
        return jsonify({'error': 'Internal server error'}), 500
