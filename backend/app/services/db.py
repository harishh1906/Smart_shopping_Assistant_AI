import logging
from flask import g, current_app
import pymysql
import pymysql.cursors

logger = logging.getLogger(__name__)

class DatabaseService:
    """Service to handle MySQL transactions cleanly using pure-Python PyMySQL."""

    def _get_connection(self):
        """
        Request-scoped connection caching using Flask 'g' context.
        Maintains a single open connection per HTTP request thread.
        """
        if 'db_conn' not in g:
            try:
                g.db_conn = pymysql.connect(
                    host=current_app.config['MYSQL_HOST'],
                    user=current_app.config['MYSQL_USER'],
                    password=current_app.config['MYSQL_PASSWORD'],
                    database=current_app.config['MYSQL_DB'],
                    cursorclass=pymysql.cursors.DictCursor,
                    charset='utf8mb4'
                )
                logger.info("🔌 Created a fresh PyMySQL database connection.")
            except Exception as e:
                logger.error(f"❌ Failed to connect to MySQL database: {e}")
                raise e
        return g.db_conn

    def execute_query(self, query: str, params: tuple = None, fetch: str = 'all'):
        """
        Execute a SQL query safely and return results.
        
        :param query: SQL query string.
        :param params: Optional parameters for SQL sanitization.
        :param fetch: 'all' to fetch all records, 'one' to fetch a single record, 'none' for write operations.
        :return: Fetched records or rows affected.
        """
        conn = self._get_connection()
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
            logger.error(f"❌ Database Query Exception: {e} | Query: {query} | Params: {params}")
            raise e
        finally:
            cursor.close()
