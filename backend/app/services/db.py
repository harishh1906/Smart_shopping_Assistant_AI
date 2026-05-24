import logging
from flask import current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseService:
    """Service to handle MySQL transactions cleanly and prevent connection leaks."""
    
    def __init__(self, mysql_instance: MySQL):
        self.mysql = mysql_instance

    def execute_query(self, query: str, params: tuple = None, fetch: str = 'all'):
        """
        Execute a SQL query safely and return results.
        
        :param query: SQL query string.
        :param params: Optional parameters for SQL sanitization.
        :param fetch: 'all' to fetch all records, 'one' to fetch a single record, 'none' for write operations.
        :return: Fetched records or rows affected.
        """
        cursor = None
        try:
            # Get dict cursor
            cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            if fetch == 'all':
                results = cursor.fetchall()
            elif fetch == 'one':
                results = cursor.fetchone()
            else:
                self.mysql.connection.commit()
                results = cursor.rowcount
                
            return results
        except MySQLdb.Error as e:
            logger.error(f"❌ Database Exception encountered: {e} | Query: {query} | Params: {params}")
            raise e
        finally:
            if cursor:
                cursor.close()
