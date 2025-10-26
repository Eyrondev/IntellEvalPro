"""
User model for IntellEvalPro
Handles user authentication and management
"""
from datetime import datetime
from .database import get_db_connection
from utils.security import generate_password_hash, check_password_hash


class User:
    """User model for authentication and profile management"""
    
    @staticmethod
    def create(username, password, email, first_name, last_name, role='student'):
        """
        Create a new user
        
        Args:
            username (str): User's username
            password (str): User's password (will be hashed)
            email (str): User's email
            first_name (str): User's first name
            last_name (str): User's last name
            role (str): User's role (admin, student, guidance)
            
        Returns:
            int: User ID of created user or None if failed
        """
        conn = get_db_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor()
            hashed_password = generate_password_hash(password)
            now = datetime.now()
            
            insert_query = """
            INSERT INTO users (username, password, email, first_name, last_name, 
                             role, is_active, is_verified, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (username, hashed_password, email, first_name, last_name,
                     role, 1, 1, now, now)
            
            cursor.execute(insert_query, values)
            conn.commit()
            user_id = cursor.lastrowid
            
            cursor.close()
            return user_id
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_by_username(username):
        """
        Get user by username
        
        Args:
            username (str): Username to search for
            
        Returns:
            dict: User data or None if not found
        """
        conn = get_db_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            return user
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(user_id):
        """
        Get user by ID
        
        Args:
            user_id (int): User ID to search for
            
        Returns:
            dict: User data or None if not found
        """
        conn = get_db_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            return user
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def authenticate(username, password):
        """
        Authenticate user with username and password
        
        Args:
            username (str): User's username
            password (str): User's password
            
        Returns:
            dict: User data if authentication successful, None otherwise
        """
        user = User.get_by_username(username)
        if user and check_password_hash(user['password'], password):
            return user
        return None
    
    @staticmethod
    def initialize_admin():
        """Initialize admin user if not exists"""
        conn = get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            admin = cursor.fetchone()
            
            if not admin:
                hashed_password = generate_password_hash('12345')
                now = datetime.now()
                
                insert_query = """
                INSERT INTO users (username, password, email, first_name, last_name, 
                                 role, is_active, is_verified, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                values = ('admin', hashed_password, 'admin@intellevalpro.com',
                         'System', 'Administrator', 'admin', 1, 1, now, now)
                
                cursor.execute(insert_query, values)
                conn.commit()
                print("Admin user created successfully")
            
            cursor.close()
        except Exception as e:
            print(f"Error initializing admin: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def update_last_login(user_id):
        """Update user's last login timestamp"""
        conn = get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET last_login = %s WHERE user_id = %s",
                (datetime.now(), user_id)
            )
            conn.commit()
            cursor.close()
        except Exception as e:
            print(f"Error updating last login: {e}")
        finally:
            conn.close()
