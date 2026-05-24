import sqlite3
import logging
import os

logger = logging.getLogger(__name__)

# Sample catalog dataset for instant portfolio demoing (seeding 12 diverse items)
SEED_PRODUCTS = [
    (1, 'Pure Cotton Printed Sweatshirt', 'Mast & Harbour', '3.8', '111', 1799.0, 629.0, 'S,M,L,XL', 
     'sweatshirts/mast-harbour/1', 'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/12147970/2021/3/12/3dfc257f-f8ec-401c-a863-4aa748c4179d1615545454736-Mast--Harbour-Women-Red--White-Pure-Cotton-Printed-Sweatshir-1.jpg', 
     'sweatshirts', 'mast-harbour', 1170.0, '65'),
     
    (2, 'Classic Pure Cotton Tee', 'Mast & Harbour', '4.2', '45', 999.0, 449.0, 'M,L,XL', 
     'tshirts/mast-harbour/2', 'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/productimage/2021/5/31/e8e01634-cea3-4d7b-b153-6666a2bddb2b1622446265721-1.jpg', 
     'tshirts', 'mast-harbour', 550.0, '55'),
     
    (3, 'Polyester Training Jacket', 'Nike', '4.6', '128', 2999.0, 1999.0, 'S,M,L', 
     'jackets/nike/3', 'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/17860832/2022/5/4/687575b0-025e-492b-bfc2-f1229257ae481651661104393-HRX-by-Hrithik-Roshan-Men-Tshirts-3791651661103795-1.jpg', 
     'jackets', 'nike', 1000.0, '33'),
     
    (4, 'Slim Striped Cotton Shirt', 'HERE&NOW', '4.3', '161', 1899.0, 664.0, '38,40,42,44', 
     'shirts/herenow/4', 'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/14808552/2021/8/17/2bbe7a3a-1a4e-4cb9-9070-ff74f84136551629195319156-HERENOW-Men-Shirts-431629195318603-1.jpg', 
     'shirts', 'herenow', 1235.0, '65'),
     
    (5, 'Women Cotton Printed Kurta', 'Anouk', '4.2', '45', 1099.0, 494.0, 'XS,S,M,L,XL', 
     'kurtas/anouk/5', 'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/17102592/2022/5/20/e8d8a9b8-bcfb-4788-abe7-6b3236e248591653044811241-Anouk-Women-Mustard-Yellow--Off-White-Ethnic-Motifs-Printed--1.jpg', 
     'kurtas', 'anouk', 605.0, '55'),
     
    (6, 'Women Skinny Fit Jeans', 'Levis', '3.6', '8', 3699.0, 3329.0, '26,28,30', 
     'jeans/levis/6', 'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/16653778/2022/1/13/0f885fab-78ff-4332-a65b-fcf95b53b56e1642077404945-Levis-Women-Jeans-7491642077404254-1.jpg', 
     'jeans', 'levis', 370.0, '10'),
     
    (7, 'Men Slim Fit Denim Jeans', 'Greenfibre', '4.0', '12', 1999.0, 1199.0, '30,32,34,36', 
     'jeans/greenfibre/7', 'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/18427492/2022/5/26/e48026c4-e1d1-4210-a95c-cfc677c1bd791653557793694GreenfibreMensRawBlueCottonStretchSolidJeans1.jpg', 
     'jeans', 'greenfibre', 800.0, '40'),
     
    (8, 'Girls Self Design A-Line Dress', 'Stylo Bug', '4.2', '384', 2195.0, 658.0, '9-10Y,11-12Y', 
     'dresses/stylo-bug/8', 'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/productimage/2021/4/30/75270b7e-a81d-4f54-9405-9f8d1a204ffa1619779892847-1.jpg', 
     'dresses', 'stylo-bug', 1537.0, '70'),
     
    (9, 'Women Woven Design Sneakers', 'ASIAN', '4.6', '7', 999.0, 629.0, 'UK4,UK5,UK6', 
     'casual-shoes/asian/9', 'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/17888028/2022/4/14/c1f62570-aef0-4158-a630-280f53a1f9531649930470914ASIANWomenBlackWovenDesignSneakers1.jpg', 
     'casual-shoes', 'asian', 370.0, '37'),
     
    (10, 'Checked Slim Fit Casual Shirt', 'Park Avenue', '3.8', '14', 2099.0, 1469.0, '39,40,42', 
     'shirts/park-avenue/10', 'https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/16741992/2022/1/31/aaa1ae58-25aa-47ea-96f1-0cc8a08e61501643620303354-Park-Avenue-Men-Blue-Checked-Slim-Fit-Pure-Cotton-Casual-Shi-1.jpg', 
     'shirts', 'park-avenue', 630.0, '30'),
     
    (11, 'Organic Cotton Slim T-Shirt', 'Nike', '4.5', '16', 1299.0, 779.0, 'S,M,L,XL', 
     'tshirts/nike/11', 'https://rukminim2.flixcart.com/image/850/1000/k65d18w0/t-shirt/3/9/m/m-ck4268-100-nike-original-imafzhftpghfjkh3.jpeg?q=90&crop=false', 
     'tshirts', 'nike', 520.0, '40'),
     
    (12, 'Floral Linen Summer Dress', 'Zara', '4.4', '27', 1799.0, 899.0, 'XS,S,M,L', 
     'dresses/zara/12', 'https://i.etsystatic.com/12423450/r/il/bc6a5e/3320703189/il_570xN.3320703189_cq10.jpg', 
     'dresses', 'zara', 900.0, '50')
]

def init_sqlite_db(db_path: str):
    """Creates a local SQLite database schema and seeds it for fully functional portfolio fallback."""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)
        
        # 2. Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS amazon_products (
                id INTEGER PRIMARY KEY,
                product_name TEXT,
                brand_name TEXT,
                rating VARCHAR(20),
                rating_count VARCHAR(50),
                marked_price REAL,
                discounted_price REAL,
                sizes TEXT,
                product_link TEXT,
                img_link TEXT,
                product_tag TEXT,
                brand_tag TEXT,
                discount_amount REAL,
                discount_percent VARCHAR(50)
            )
        """)
        
        # 3. Seed product data
        cursor.executemany("""
            INSERT OR REPLACE INTO amazon_products 
            (id, product_name, brand_name, rating, rating_count, marked_price, discounted_price, sizes, product_link, img_link, product_tag, brand_tag, discount_amount, discount_percent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, SEED_PRODUCTS)
        
        conn.commit()
        conn.close()
        logger.info(f"✨ Successfully initialized and seeded SQLite database at {db_path}!")
    except Exception as e:
        logger.error(f"❌ Failed to initialize SQLite database: {e}")
