"""
Database Connection Tester for IntellEvalPro
Tests DATABASE_URL parsing and MySQL connectivity
"""
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import mysql.connector

# Load environment variables
load_dotenv()

def parse_database_url(url=None):
    """Parse DATABASE_URL into connection parameters"""
    if not url:
        url = os.getenv('DATABASE_URL')
    
    if url:
        # Parse the DATABASE_URL
        parsed = urlparse(url)
        return {
            'host': parsed.hostname or 'localhost',
            'user': parsed.username or 'root',
            'password': parsed.password or '',
            'database': parsed.path.lstrip('/') if parsed.path else 'IntellEvalPro_db',
            'port': parsed.port or 3306
        }
    else:
        # Fall back to individual environment variables
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'IntellEvalPro_db'),
            'port': int(os.getenv('DB_PORT', 3306))
        }

def test_database_connection():
    """Test database connection and display results"""
    print("=" * 70)
    print("IntellEvalPro Database Connection Tester")
    print("=" * 70)
    print()
    
    # Get DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    print(f"📋 DATABASE_URL from .env:")
    if database_url:
        # Mask password in display
        display_url = database_url
        if '@' in display_url:
            parts = display_url.split('@')
            if ':' in parts[0]:
                cred_parts = parts[0].split(':')
                if len(cred_parts) >= 3:
                    masked = f"{cred_parts[0]}:{cred_parts[1]}:****@{parts[1]}"
                    display_url = masked
        print(f"   {display_url}")
    else:
        print("   ❌ Not set! Using fallback parameters.")
    print()
    
    # Parse connection parameters
    db_config = parse_database_url(database_url)
    
    print("🔧 Parsed Connection Parameters:")
    print(f"   Host:     {db_config['host']}")
    print(f"   Port:     {db_config['port']}")
    print(f"   User:     {db_config['user']}")
    print(f"   Password: {'****' if db_config['password'] else '(empty)'}")
    print(f"   Database: {db_config['database']}")
    print()
    
    # Test connection
    print("🔌 Testing MySQL Connection...")
    print("-" * 70)
    
    try:
        # Attempt connection
        conn = mysql.connector.connect(**db_config)
        
        if conn.is_connected():
            print("✅ SUCCESS! Connected to MySQL server")
            
            # Get server info
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"   MySQL Version: {version[0]}")
            
            # Check if database exists
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            
            if db_config['database'] in databases:
                print(f"   ✅ Database '{db_config['database']}' exists")
                
                # Get table count
                cursor.execute(f"USE {db_config['database']}")
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f"   📊 Found {len(tables)} tables in database")
                
                if tables:
                    print(f"   📋 Tables: {', '.join([t[0] for t in tables[:5]])}")
                    if len(tables) > 5:
                        print(f"            ... and {len(tables) - 5} more")
            else:
                print(f"   ⚠️  Warning: Database '{db_config['database']}' does NOT exist")
                print(f"   Available databases: {', '.join(databases[:5])}")
            
            cursor.close()
            conn.close()
            print()
            print("=" * 70)
            print("✅ Database connection test PASSED!")
            print("=" * 70)
            return True
            
    except mysql.connector.Error as err:
        print(f"❌ FAILED! MySQL Error:")
        print(f"   Error Code: {err.errno}")
        print(f"   Error Message: {err.msg}")
        print()
        
        # Provide helpful suggestions
        print("💡 Troubleshooting Tips:")
        if err.errno == 2003:
            print("   • Check if MySQL/XAMPP is running")
            print("   • Verify the host address is correct")
            print("   • Check firewall settings")
        elif err.errno == 1045:
            print("   • Check username and password")
            print("   • Verify user has proper permissions")
        elif err.errno == 1049:
            print("   • Database does not exist")
            print("   • Create the database or check the name")
        else:
            print("   • Check your DATABASE_URL format")
            print("   • Ensure MySQL server is accessible")
        
        print()
        print("=" * 70)
        print("❌ Database connection test FAILED!")
        print("=" * 70)
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        print()
        print("=" * 70)
        print("❌ Database connection test FAILED!")
        print("=" * 70)
        return False

if __name__ == "__main__":
    test_database_connection()
    input("\nPress Enter to exit...")
