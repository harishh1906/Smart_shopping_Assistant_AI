import logging
import sqlite3
import os
from flask import g, current_app
import pymysql
import pymysql.cursors
from app.services.sqlite_seeder import init_sqlite_db

logger = logging.getLogger(__name__)

# Temporary directory for serverless environments (Vercel allows writes to /tmp)
SQLITE_PATH = "/tmp/smart_shopping_assistant.db"

class DatabaseService:
    """
    Resilient Database Service that manages connection pooling.
    If MySQL server is unavailable (standard on Vercel deployment), it seamlessly
    switches to a fully-seeded request-scoped SQLite instance to ensure zero-downtime.
    """

    def _get_connection(self):
        """
        Request-scoped connection manager. 
        Attempts MySQL first, transparently falls back to seeded SQLite on failure.
        """
        if 'db_conn' not in g:
            # 1. Attempt MySQL Connection
            try:
                g.db_conn = pymysql.connect(
                    host=current_app.config['MYSQL_HOST'],
                    user=current_app.config['MYSQL_USER'],
                    password=current_app.config['MYSQL_PASSWORD'],
                    database=current_app.config['MYSQL_DB'],
                    cursorclass=pymysql.cursors.DictCursor,
                    charset='utf8mb4',
                    connect_timeout=3  # Fast timeout to prevent blocking on Vercel
                )
                g.db_type = 'mysql'
                logger.info("🔌 Successfully connected to MySQL database.")
            except Exception as mysql_err:
                logger.warning(
                    f"⚠️ MySQL connection failed: {mysql_err}. "
                    "Triggering seamless SQLite failover mode for out-of-the-box hosting!"
                )
                
                # 2. SQLite Failover Execution
                try:
                    # Seed database if not yet created in Vercel's temporary directory
                    if not os.path.exists(SQLITE_PATH):
                        init_sqlite_db(SQLITE_PATH)
                        
                    g.db_conn = sqlite3.connect(SQLITE_PATH)
                    
                    # Convert SQLite rows into dictionary records matching MySQL DictCursor
                    def dict_factory(cursor, row):
                        d = {}
                        for idx, col in enumerate(cursor.description):
                            d[col[0]] = row[idx]
                        return d
                    g.db_conn.row_factory = dict_factory
                    
                    g.db_type = 'sqlite'
                    logger.info("⚡ Active Failover: PyMySQL successfully routed to SQLite.")
                except Exception as sqlite_err:
                    logger.error(f"❌ Critical Error initializing SQLite: {sqlite_err}")
                    raise mysql_err  # Raise the original MySQL error if fallback fails
                    
        return g.db_conn

    def execute_query(self, query: str, params: tuple = None, fetch: str = 'all'):
        """
        Executes database operations safely. 
        Auto-translates syntax placeholders if SQLite fallback is active.
        """
        conn = self._get_connection()
        db_type = g.get('db_type', 'mysql')
        
        # SQL Syntax Translation for SQLite Mode
        if db_type == 'sqlite':
            # Replace MySQL %s parameter tokens with SQLite ?
            query = query.replace('%s', '?')
            # Replace MySQL ORDER BY RAND() with SQLite RANDOM()
            query = query.replace('RAND()', 'RANDOM()')
            
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            if fetch == 'all':
                results = cursor.fetchall()
            elif fetch == 'one':
                results = cursor.fetchone()
            else:
                conn.commit()
                results = cursor.rowcount
                
            return results
        except Exception as e:
            logger.error(f"❌ Database Query Exception under {db_type.upper()}: {e} | Query: {query}")
            raise e
        finally:
            cursor.close()
