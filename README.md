Smart Shopping Assistant
A web-based shopping assistant that helps users compare prices for clothing items across multiple e-commerce platforms (Amazon, Walmart, and Flipkart). The platform also provides product recommendations using a machine learning model based on product similarity.

Features
Product Search: Search for clothing items by name.

Price Comparison: Compare product prices across Amazon, Walmart, and Flipkart.

Product Recommendations: Get product recommendations based on similarity to the selected product using PCA (Principal Component Analysis) and Cosine Similarity.

Dynamic UI: Interactive user interface with price comparison highlighting the lowest price in green.

Responsive Design: Fully responsive layout for a seamless experience across devices.

Technology Stack
Frontend:

HTML5

CSS3

JavaScript

Jinja (Template Engine for Flask)

Backend:

Python (Flask)

Pandas (for handling product data)

NumPy (for calculations)

scikit-learn (for PCA and Cosine Similarity)

Machine Learning:

Principal Component Analysis (PCA)

Cosine Similarity for product recommendations

Additional Tools:

WordCloud (for product descriptions)

Docker (for containerization)

Prerequisites
Before running this project, ensure that you have the following installed:

Python 3.x (Recommended version: 3.7 or above)

pip (Python package manager)

Dependencies
To install all the required dependencies, use the following command:


pip install -r requirements.txt
requirements.txt contains all the Python dependencies for this project:


Flask==2.0.3
pandas==1.3.3
numpy==1.21.2
scikit-learn==0.24.2
wordcloud==1.8.1
Running the Project
Clone the repository:

If you haven't already cloned the repository, use this command to clone it:


git clone https://github.com/your-username/smart-shopping-assistant.git
cd smart-shopping-assistant
Set up a Virtual Environment (optional but recommended):


python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate  # On Windows

Install Dependencies:

pip install -r requirements.txt

Run the Application:

python app.py
Your app should now be running on http://127.0.0.1:5000/. Open this URL in your web browser.

Docker (Optional):
If you want to run the app in a Docker container, follow these steps:

Build the Docker image:

bash
Copy
Edit
docker build -t shopping-assistant .
Run the Docker container:

bash
Copy
Edit
docker run -p 5000:5000 shopping-assistant
The app will be available at http://localhost:5000.

Project Structure

Smart-Shopping-Assistant/
│
├── app.py                # Flask app with routes and logic
├── requirements.txt      # List of dependencies
├── Dockerfile            # Dockerfile for containerization
├── static/               # Folder for static files (CSS, images, etc.)
│   └── styles.css        # CSS file for styling the app
├── templates/            # Folder for HTML templates
│   ├── index.html        # Home page template
│   └── product_details.html  # Product details page template
└── venv/                 # Virtual environment 
ML Model Overview
Principal Component Analysis (PCA): Used to reduce the dimensionality of the product feature space and create a simpler representation of the data.

Cosine Similarity: Used to measure how similar two products are based on their reduced features (from PCA). This similarity score helps in recommending products that are similar to the one the user is interested in.

How the Model Works:
Data Preparation: We simulate product features and use PCA to reduce the features into a lower-dimensional space.

Similarity Calculation: We compute the cosine similarity between the reduced features of all products.

Recommendation: When a user selects a product, we use the similarity scores to recommend the top 5 products that are most similar.
