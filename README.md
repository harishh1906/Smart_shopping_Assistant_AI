# Smart Shopping Assistant AI

An intelligent, production-style, e-commerce shopping companion built to solve price comparison, category-based content recommendation, and real-time review sentiment analysis. The platform bridges the gap between catalog listings and smart buyer insights by utilizing custom NLP modeling and content vectors.

---

## 🛠️ System Overview & Architecture

Modern e-commerce catalogs offer an abundance of products, but lack cross-platform price transparency, meaningful discovery tools, and digestible feedback summaries. This project implements a high-fidelity web platform that solves these problems under one unified architectural lifecycle:

```
                                  [ User Browser ]
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼ (HTTP requests / Session Auth)                ▼ (AJAX call)
          [ Flask App ]                                    [ AI Copywriting ]
                 │                                               │
   ┌─────────────┼─────────────┐                                 │
   ▼             ▼             ▼                                 │
[ Auth ]    [ Catalog ]   [ Services ]                           │
                 │             │                                 │
                 │             ├───────────────┬─────────────────┼──────────────┐
                 │             ▼               ▼                 ▼              ▼
                 │        [ db.py ]    [ recommender.py ]  [ sentiment.py ] [ ai.py ]
                 │             │               │                 │              │
                 ▼             ▼               ▼                 ▼              ▼
           [                     MySQL Database / shopping_db ]
```

### Request Lifecycle Flow
1. **User Authentication & Entry**: Sessions are secured via cryptographic signing and authenticated using salted passwords processed by `Bcrypt`.
2. **Dynamic Search & Filtering**: Catalog queries process target apparel listings directly from a local indexed MySQL database.
3. **Dynamic Store Price Offsets**: Real Myntra prices are queried and compared on-the-fly against simulated margins on Amazon and Flipkart to highlight the lowest purchasing channel.
4. **Category-Scoped Recommendation Pipeline**: Selecting a product triggers content-based vector calculations on TF-IDF fields (combining name, brand, and tag details) within that specific product category.
5. **TextBlob NLP Sentiment Scoring**: Reviews are dynamically generated corresponding to the product's ratings. TextBlob computes subjectivity and polarity values in real time, serving positive, negative, and neutral metrics directly onto the UI.
6. **Async AI Copywriting Generation**: A non-blocking client-side `fetch` reads from `/generate_description/<id>` to compile context-aware copywriting from metadata fields.

---

## 🤖 Core AI & NLP Components

Rather than relying on static placeholders or bloated deep learning instances, the application implements lean, highly precise mathematical algorithms suited for fast, server-side execution.

### 1. TF-IDF + Cosine Similarity Recommender (`services/recommender.py`)
To prevent system-level blocking when parsing thousands of items in memory, the engine scopes the matching candidates to the **target product's category (`product_tag`)**. 
- **Methodology**: Text columns (`product_name`, `brand_name`, `brand_tag`) are joined, lower-cased, and processed into a mathematical matrix using `scikit-learn`'s `TfidfVectorizer`.
- **Optimization**: Candidate items are reduced from 27,000 to less than 1,500. This constraints spatial dimensions, computing cosine similarities in under 15ms.
- **Eco-Friendly Matching**: Compiles sustainable alternatives within the category by querying items whose materials contain green keywords (`organic`, `cotton`, `linen`, `handwoven`) before sorting by similarity scores.

### 2. TextBlob Customer Sentiment Engine (`services/sentiment.py`)
To synthesize realistic qualitative analytics, the engine maps numeric reviews to TextBlob metrics:
- **Review Synthesis**: Pulls appropriate user reviews depending on whether the catalog rating is High ($\ge 4.0$), Medium ($3.0 - 3.9$), or Low ($< 3.0$).
- **Sentiment Classification**: Passes text through `textblob.TextBlob` to extract **Polarity** ($[-1.0, 1.0]$: negative to positive) and **Subjectivity** ($[0.0, 1.0]$: objective to opinion-heavy).
- **Composite Metrics**: Aggregates classifications to output satisfying visual dials (e.g. 70% Positive, 20% Neutral, 10% Negative) to recruiters at a glance.

---

## 🎨 Tech Stack & Architectural Reasoning

| Layer | Technology | Architectural Rationale |
| :--- | :--- | :--- |
| **Framework** | **Python (Flask)** | Simple, fast, and secure. Avoids Node/React overengineering for a templated portfolio catalog, allowing direct coupling with scientific Python libraries (`sklearn`, `pandas`). |
| **Database** | **MySQL** | Standard thread-safe transactional store. Handles relational index lookups (`amazon_products`) with high consistency, fast string searches, and robust foreign keys. |
| **Styling** | **Vanilla CSS (HSL Variables)** | Avoids standard Tailwind dependencies. Establishes custom tokens, glassmorphism card backdrops, dynamic HSL alerts, and Outfit/Inter google typography from scratch. |
| **AI / NLP** | **scikit-learn & TextBlob** | Lightweight, proven scientific computation tools. Runs mathematical operations locally on server cores instead of calling expensive third-party LLM APIs. |

---

## 📂 Project Directory Structure

```
Smart_shopping_Assistant_AI/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask factory & blueprint registration
│   │   ├── config.py            # Environment-driven configs (fallback defaults)
│   │   ├── routes/              # Modular controller endpoints
│   │   │   ├── auth.py          # Session registration, login, logout
│   │   │   ├── products.py      # Search, details, and eco-friendly catalogue
│   │   │   └── ai.py            # Async AI description endpoint
│   │   ├── services/            # Pure Business & AI calculation logic
│   │   │   ├── db.py            # Thread-safe MySQL transactional wrapper
│   │   │   ├── recommender.py   # TF-IDF + Cosine Similarity recommendation service
│   │   │   └── sentiment.py     # TextBlob NLP review analysis engine
│   │   ├── templates/           # Premium Jinja2 UI Views
│   │   │   ├── base.html        # Central boilerplate shell (Outfit/Inter fonts)
│   │   │   ├── index.html       # E-Commerce comparison search board
│   │   │   ├── product_details.html # Detailed metrics, NLP charts, rec carousels
│   │   │   ├── eco_friendly.html # Curated sustainable item listings
│   │   │   ├── login.html       # Elegant login card
│   │   │   └── register.html    # Elegant register card
│   │   └── static/              # Premium styling assets
│   │       ├── css/
│   │       │   └── styles.css   # Dark-theme HSL design sheet
│   │       └── js/
│   │           └── main.js      # Client-side async fetch and UI transitions
│   │
│   ├── tests/                   # Automated Unit Tests
│   └── run.py                   # Main boot script
│
├── database/                    # SQL Assets
│   ├── schema.sql               # Clean table structures
│   └── shopping_db.sql          # Seed dataset containing 27,000+ fashion rows
│
├── docs/                        # Specifications
│   ├── architecture.md          # Technical implementation blueprint
│   └── api_spec.md              # REST API descriptions
│
├── scripts/                     # Utility scripts
│   └── setup_db.py              # Automated database setup tool
│
├── Dockerfile                   # Multi-stage C-compiled runtime container
├── .gitignore                   # Bulletproof Python/IDE system rule filters
├── .env.example                 # Environmental configuration template
├── requirements.txt             # Verified lockable dependencies
└── README.md                    # Portfolio-grade engineering manual
```

---

## 🚀 Setup & Installation Instructions

Ensure you have **Python 3.10+** and a running **MySQL server** instance.

### 1. Database Initialization
Create a database named `shopping_db` on your local MySQL server, then import the raw SQL database schema and seed tables:
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS shopping_db;"
mysql -u root -p shopping_db < database/shopping_db.sql
```

### 2. Local App Installation
Clone the repository and enter the directory:
```bash
# Set up a clean virtual environment
python -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate     # On Windows

# Install locked dependencies
pip install -r requirements.txt
```

### 3. Environmental Configuration
Duplicate `.env.example` to `.env` and fill in your local credentials:
```bash
cp .env.example .env
```
Ensure your `DB_PASSWORD` matches your local MySQL server configuration.

### 4. Running the Development Server
Start the Flask application using our central run script:
```bash
python backend/run.py
```
Open [http://localhost:5000](http://localhost:5000) in your web browser.

---

## 🐳 Docker Deployment

To build and run the application inside a containerized, compiler-isolated environment:

```bash
# Build the production image (compiles native mysqlclient cleanly)
docker build -t smart-shopping-assistant .

# Run the container mapping port 5000 (binds to host machine's MySQL or isolated bridge)
docker run -d -p 5000:5000 --env-file .env smart-shopping-assistant
```

---

## 📈 Future Implementation Backlog

- [ ] **Multi-Modal Image Querying**: Implement feature vector indexing using deep ResNet-50 embeddings, allowing users to upload clothing images to retrieve identical listings.
- [ ] **Real-Time Web Scraping**: Transition from static SQL tables to asynchronous Python scrapers (`Playwright` / `BeautifulSoup`) checking Myntra, Amazon, and Flipkart prices in real time.
- [ ] **RAG-based Chatbot**: Integrate a local quantized Llama-3 model using vector store databases (`ChromaDB`) to assist buyers with conversational inquiries.
