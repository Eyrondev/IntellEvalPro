"""
IntellEvalPro - Faculty Evaluation System
Main application file (Modular Architecture)

This is the refactored version using Flask blueprints for better organization.
For the legacy monolithic version, see app.py.backup
"""
import os
import logging

# Suppress gRPC/ALTS warnings for cleaner console output
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GRPC_TRACE'] = ''
logging.getLogger('grpc').setLevel(logging.ERROR)

from flask import Flask
from config import Config
from models.database import db, init_db
from models import init_drafts_table, User
from utils import DecimalJSONProvider

# Import route blueprints
from routes import auth_bp, admin_bp, student_bp, guidance_bp, api_bp
from routes.analytics import analytics_bp


def create_app(config_class=Config):
    """
    Application factory pattern
    Creates and configures the Flask application
    
    Args:
        config_class: Configuration class to use
        
    Returns:
        Flask application instance
    """
    # Initialize Flask app
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # Load configuration
    app.config.from_object(config_class)
    app.secret_key = config_class.SECRET_KEY
    
    # Initialize SQLAlchemy
    init_db(app)
    
    # Configure custom JSON encoder for Decimal types
    app.json = DecimalJSONProvider(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(guidance_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(analytics_bp)
    
    # Add compatibility routes for old template references
    # This allows templates with url_for('login') to work
    # TODO: Update templates to use blueprint endpoints (e.g., url_for('auth.login'))
    
    # Add cache control headers to prevent browser back button logout
    @app.after_request
    def add_cache_headers(response):
        """
        Add cache control headers to prevent browser caching of authenticated pages.
        This prevents the back button from showing stale/cached content that might
        trigger logout or show incorrect session state.
        """
        from flask import request, session
        
        # Only apply to HTML pages (not static files, API responses, etc.)
        if response.content_type and 'text/html' in response.content_type:
            # If user is logged in, prevent caching
            if 'user_id' in session:
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
            # For login page, allow normal caching
            elif request.path in ['/login', '/login.html', '/']:
                response.headers['Cache-Control'] = 'public, max-age=300'
        
        return response
    
    return app


# Create application instance
app = create_app()


if __name__ == '__main__':
    # Initialize database tables
    print("Initializing database tables...")
    init_drafts_table()
    
    # Initialize admin user
    print("Checking admin user...")
    User.initialize_admin()
    
    print(f"\n{'='*50}")
    print("IntellEvalPro - Faculty Evaluation System")
    print(f"{'='*50}")
    print(f"Server starting on http://{Config.HOST}:{Config.PORT}")
    print(f"Debug mode: {Config.DEBUG}")
    print(f"\nDefault login credentials:")
    print(f"  Admin    - Username: admin     Password: 12345")
    print(f"  Student  - Username: 2022-0215 Password: 12345")
    print(f"  Guidance - Username: guidance  Password: 12345")
    print(f"{'='*50}\n")
    
    # Run the Flask app
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
