"""
Database connection module for IntellEvalPro
Provides SQLAlchemy database instance and legacy mysql-connector support
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import mysql.connector
from urllib.parse import urlparse
from config import Config

# SQLAlchemy instance (to be initialized with app in app.py)
db = SQLAlchemy()


def init_db(app):
    """
    Initialize SQLAlchemy with Flask app
    
    Args:
        app: Flask application instance
    """
    db.init_app(app)
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        print("✅ SQLAlchemy database initialized")


def get_db_connection():
    """
    Legacy function: Create and return a MySQL database connection using mysql-connector
    This is kept for backward compatibility with existing code.
    
    Returns:
        mysql.connector.connection: Database connection object or None if failed
    """
    try:
        # Parse DATABASE_URL to extract connection parameters
        db_url = Config.SQLALCHEMY_DATABASE_URI
        parsed = urlparse(db_url)
        
        db_config = {
            'host': parsed.hostname or 'localhost',
            'user': parsed.username or 'root',
            'password': parsed.password or '',
            'database': parsed.path.lstrip('/') if parsed.path else 'IntellEvalPro_db',
            'port': parsed.port or 3306
        }
        
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None


def init_drafts_table():
    """Initialize evaluation_drafts table if it doesn't exist"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Create table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS evaluation_drafts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    evaluation_id INT NOT NULL,
                    draft_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (evaluation_id) REFERENCES evaluations(evaluation_id) ON DELETE CASCADE
                )
            """)
            
            # Check if index exists before creating (compatible with older MySQL/MariaDB)
            cursor.execute("""
                SELECT COUNT(1) as index_exists
                FROM information_schema.statistics
                WHERE table_schema = DATABASE()
                AND table_name = 'evaluation_drafts'
                AND index_name = 'idx_evaluation_drafts_evaluation_id'
            """)
            index_exists = cursor.fetchone()[0]
            
            if not index_exists:
                cursor.execute(
                    "CREATE INDEX idx_evaluation_drafts_evaluation_id "
                    "ON evaluation_drafts(evaluation_id)"
                )
            
            conn.commit()
            print("✅ Evaluation drafts table initialized successfully")
        except Exception as e:
            print(f"Error initializing drafts table: {e}")
        finally:
            cursor.close()
            conn.close()


def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
    """
    Execute a database query with proper error handling
    
    Args:
        query (str): SQL query to execute
        params (tuple): Query parameters
        fetch_one (bool): Whether to fetch one result
        fetch_all (bool): Whether to fetch all results
        commit (bool): Whether to commit the transaction
        
    Returns:
        Result of the query or None if failed
    """
    conn = get_db_connection()
    if not conn:
        return None
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if commit:
            conn.commit()
            result = cursor.lastrowid
        elif fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = True
            
        cursor.close()
        return result
    except Exception as e:
        print(f"Database query error: {e}")
        return None
    finally:
        conn.close()
