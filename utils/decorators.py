"""
Decorator utilities for IntellEvalPro
Provides route decorators for authentication and authorization
"""
from functools import wraps
from flask import session, redirect, url_for, flash, request, jsonify
from datetime import datetime, timedelta


def login_required(f):
    """
    Decorator to require login for a route
    Handles both regular requests and AJAX/API requests
    Also checks for session timeout (1 hour of inactivity)
    
    Usage:
        @app.route('/protected')
        @login_required
        def protected_route():
            return "Protected content"
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in
        if 'user_id' not in session:
            # Check if this is an AJAX/API request
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Return JSON error for AJAX requests
                return jsonify({'success': False, 'message': 'Authentication required', 'error': 'Not logged in'}), 401
            else:
                # Redirect to login for regular requests
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
        
        # Check for session timeout (1 hour of inactivity)
        last_activity = session.get('last_activity')
        if last_activity:
            try:
                last_activity_time = datetime.fromisoformat(last_activity)
                current_time = datetime.now()
                time_elapsed = current_time - last_activity_time
                
                # If more than 1 hour (3600 seconds) has passed, force logout
                if time_elapsed.total_seconds() > 3600:
                    # Log the auto-logout
                    try:
                        from models import get_db_connection
                        conn = get_db_connection()
                        if conn:
                            cursor = conn.cursor()
                            cursor.execute("""
                                INSERT INTO activity_logs 
                                (user_id, user_name, user_role, activity_type, description, ip_address)
                                VALUES (%s, %s, %s, %s, %s, %s)
                            """, (
                                session.get('user_id'),
                                f"{session.get('first_name', '')} {session.get('last_name', '')}".strip() or session.get('username', 'Unknown'),
                                session.get('role'),
                                'auto_logout',
                                'Session expired after 1 hour of inactivity',
                                request.remote_addr
                            ))
                            conn.commit()
                            cursor.close()
                            conn.close()
                    except Exception as e:
                        print(f"Error logging auto-logout: {e}")
                    
                    # Clear session
                    session.clear()
                    
                    # Handle AJAX vs regular request
                    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return jsonify({
                            'success': False, 
                            'message': 'Your session has expired. Please log in again.',
                            'error': 'Session expired',
                            'session_expired': True
                        }), 401
                    else:
                        flash('Your session has expired after 1 hour of inactivity. Please log in again.', 'warning')
                        return redirect(url_for('auth.login'))
            except (ValueError, TypeError) as e:
                print(f"Error checking session timeout: {e}")
                # If there's an error parsing the time, reset last_activity
                session['last_activity'] = datetime.now().isoformat()
        
        # Update last activity time for valid sessions
        session['last_activity'] = datetime.now().isoformat()
        
        return f(*args, **kwargs)
    return decorated_function


def role_required(role):
    """
    Decorator to require specific role for a route
    Also includes session timeout checking
    
    Args:
        role (str or list): Required role(s)
        
    Usage:
        @app.route('/admin-only')
        @role_required('admin')
        def admin_route():
            return "Admin content"
            
        @app.route('/admin-or-guidance')
        @role_required(['admin', 'guidance'])
        def multi_role_route():
            return "Admin or guidance content"
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is logged in
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            
            # Check for session timeout (1 hour of inactivity)
            last_activity = session.get('last_activity')
            if last_activity:
                try:
                    last_activity_time = datetime.fromisoformat(last_activity)
                    current_time = datetime.now()
                    time_elapsed = current_time - last_activity_time
                    
                    # If more than 1 hour (3600 seconds) has passed, force logout
                    if time_elapsed.total_seconds() > 3600:
                        # Log the auto-logout
                        try:
                            from models import get_db_connection
                            conn = get_db_connection()
                            if conn:
                                cursor = conn.cursor()
                                cursor.execute("""
                                    INSERT INTO activity_logs 
                                    (user_id, user_name, user_role, activity_type, description, ip_address)
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                """, (
                                    session.get('user_id'),
                                    f"{session.get('first_name', '')} {session.get('last_name', '')}".strip() or session.get('username', 'Unknown'),
                                    session.get('role'),
                                    'auto_logout',
                                    'Session expired after 1 hour of inactivity',
                                    request.remote_addr
                                ))
                                conn.commit()
                                cursor.close()
                                conn.close()
                        except Exception as e:
                            print(f"Error logging auto-logout: {e}")
                        
                        # Clear session
                        session.clear()
                        flash('Your session has expired after 1 hour of inactivity. Please log in again.', 'warning')
                        return redirect(url_for('auth.login'))
                except (ValueError, TypeError) as e:
                    print(f"Error checking session timeout: {e}")
                    # If there's an error parsing the time, reset last_activity
                    session['last_activity'] = datetime.now().isoformat()
            
            # Update last activity time
            session['last_activity'] = datetime.now().isoformat()
            
            # Check role permission
            user_role = session.get('role')
            
            # Check if role is a list or single value
            allowed_roles = role if isinstance(role, list) else [role]
            
            if user_role not in allowed_roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('auth.login'))
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """
    Decorator to require admin role
    Shortcut for @role_required('admin')
    """
    return role_required('admin')(f)


def student_required(f):
    """
    Decorator to require student role
    Shortcut for @role_required('student')
    """
    return role_required('student')(f)


def guidance_required(f):
    """
    Decorator to require guidance role
    Shortcut for @role_required('guidance')
    """
    return role_required('guidance')(f)
