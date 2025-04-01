from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
import random
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud

app = Flask(__name__)

# Load sample dataset (50 clothing products)
products = pd.DataFrame({
    'id': range(50),
    'name': [f'Clothing Item {i}' for i in range(50)],
    'brand': [random.choice(['Nike', 'Adidas', 'Zara', 'H&M']) for _ in range(50)],
    'price': np.random.randint(10, 100, 50),
    'amazon_price': np.random.randint(10, 100, 50),
    'walmart_price': np.random.randint(10, 100, 50),
    'flipkart_price': np.random.randint(10, 100, 50),
    'ratings': [round(random.uniform(3, 5), 1) for _ in range(50)],
    'description': ["Sample description" for _ in range(50)],
    'features': ["Cotton, Breathable" for _ in range(50)]
})

# ML Model for Recommendations (PCA & Cosine Similarity)
product_features = np.random.rand(50, 5)
pca = PCA(n_components=2)
reduced_features = pca.fit_transform(product_features)
similarity_matrix = cosine_similarity(reduced_features)

def get_recommendations(product_id, top_n=5):
    idx = product_id
    scores = list(enumerate(similarity_matrix[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    recommendations = [products.iloc[i[0]] for i in scores[1:top_n+1]]
    return recommendations

@app.route('/')
def home():
    query = request.args.get('query', '')
    filtered_products = products[products['name'].str.contains(query, case=False, na=False)]
    return render_template('index.html', products=filtered_products.to_dict(orient='records'))

@app.route('/compare', methods=['POST'])
def compare_prices():
    selected_ids = request.json.get('selected_ids', [])
    selected_products = products[products['id'].isin(selected_ids)]
    return jsonify(selected_products.to_dict(orient='records'))

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = products.loc[products['id'] == product_id].iloc[0]
    recommendations = get_recommendations(product_id)
    return render_template('product_details.html', product=product, recommendations=recommendations)

@app.route('/generate_description/<int:product_id>')
def generate_description(product_id):
    product = products.iloc[product_id]
    text = f"{product['name']} from {product['brand']} offers premium quality at ${product['price']}. "
    text += "This product is rated high on sustainability."
    wordcloud = WordCloud(width=400, height=200).generate(text)
    wordcloud.to_file("static/wordcloud.png")
    return jsonify({'description': text, 'wordcloud': 'static/wordcloud.png'})

if __name__ == '__main__':
    app.run(debug=True)
