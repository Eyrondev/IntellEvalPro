"""
Admin routes blueprint for IntellEvalPro
Handles all admin-related routes and functionality
"""
from flask import Blueprint, render_template, session, redirect, url_for
from utils import admin_required
from models import Faculty, Student, get_db_connection
from utils.json_encoder import jsonify

# Create blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@admin_bp.route('/admin-dashboard')  # Keep for backward compatibility
@admin_required
def admin_dashboard():
    """Admin dashboard page"""
    return render_template('admin/admin-dashboard.html')


@admin_bp.route('/faculty-list')
@admin_required
def faculty_list():
    """Faculty list page"""
    return render_template('admin/faculty-list.html')


@admin_bp.route('/student-list')
@admin_required
def student_list():
    """Student list page"""
    return render_template('admin/student-list.html')


@admin_bp.route('/subjects')
@admin_required
def subjects():
    """Subjects management page"""
    return render_template('admin/subjects.html')


@admin_bp.route('/academic-years')
@admin_required
def academic_years():
    """Academic years management page"""
    return render_template('admin/academic-years.html')


@admin_bp.route('/sections')
@admin_required
def sections():
    """Section management page"""
    return render_template('admin/sections.html')


@admin_bp.route('/classes')
@admin_required
def classes():
    """Classes management page"""
    return render_template('admin/classes.html')


@admin_bp.route('/evaluation-periods')
@admin_required
def evaluation_periods():
    """Evaluation periods management page"""
    return render_template('admin/evaluation-periods.html')


@admin_bp.route('/activity-logs')
@admin_required
def activity_logs():
    """Activity logs page"""
    return render_template('admin/activity-logs.html')


@admin_bp.route('/user-management')
@admin_required
def user_management():
    """User management page"""
    return render_template('admin/user-management.html')


@admin_bp.route('/archives')
@admin_required
def archives():
    """Archives page - view all archived records"""
    return render_template('admin/archives.html')


@admin_bp.route('/navigation')
@admin_required
def navigation():
    """Admin navigation component"""
    return render_template('admin/components/navigation.html')


@admin_bp.route('/header')
@admin_required
def header():
    """Admin header component"""
    # Get current academic year and term from database
    current_term_display = 'No Active Term'
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            
            # Get current academic year
            cursor.execute("""
                SELECT acad_year_id, year_code, year_name
                FROM academic_years
                WHERE is_current = 1
                LIMIT 1
            """)
            current_year = cursor.fetchone()
            
            if current_year:
                # Get current semester/term for this year
                cursor.execute("""
                    SELECT term_name, term_code
                    FROM academic_terms
                    WHERE acad_year_id = %s AND is_current = 1
                    LIMIT 1
                """, (current_year['acad_year_id'],))
                current_term = cursor.fetchone()
                
                if current_term:
                    current_term_display = f"{current_year['year_code']} - {current_term['term_name']}"
                else:
                    current_term_display = current_year['year_code']
            
            cursor.close()
            conn.close()
    except Exception as e:
        print(f"Error getting current term: {e}")
    
    return render_template('admin/components/header.html', current_term_title=current_term_display)


# ============================================================================
# TIMER MANAGEMENT API ENDPOINTS (Admin Access)
# ============================================================================

@admin_bp.route('/api/timer-settings', methods=['GET'])
@admin_required
def get_timer_settings():
    """Get current timer settings (Admin)"""
    from flask import jsonify, request
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Check if settings table exists, if not return defaults
        cursor.execute("""
            SELECT * FROM timer_settings 
            WHERE setting_id = 1
            LIMIT 1
        """)
        settings = cursor.fetchone()
        
        if not settings:
            # Return default settings
            settings = {
                'enabled': True,
                'time_limit': 30,
                'warning_1': 5,
                'warning_2': 1
            }
        
        # Ensure enabled is returned as integer (0 or 1) for JavaScript
        enabled_value = settings.get('enabled', 1)
        # Convert to integer: True/1/"1" -> 1, False/0/"0" -> 0
        enabled_int = 1 if (enabled_value == 1 or enabled_value == '1' or enabled_value is True) else 0
        
        return jsonify({
            'success': True,
            'data': {
                'enabled': enabled_int,  # Return as integer (0 or 1)
                'time_limit': int(settings.get('time_limit', 30)),
                'warning_1': int(settings.get('warning_1', 5)),
                'warning_2': int(settings.get('warning_2', 1))
            }
        })
        
    except Exception as e:
        print(f"Error loading timer settings: {str(e)}")
        # Return defaults on error
        return jsonify({
            'success': True,
            'data': {
                'enabled': 1,
                'time_limit': 30,
                'warning_1': 5,
                'warning_2': 1
            }
        })
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@admin_bp.route('/api/timer-settings', methods=['POST'])
@admin_required
def save_timer_settings():
    """Save timer settings (Admin)"""
    from flask import jsonify, request
    
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    # Convert enabled to integer (0 or 1) for database
    enabled_value = data.get('enabled', True)
    enabled = 1 if (enabled_value is True or enabled_value == 1 or enabled_value == '1' or enabled_value == 'true') else 0
    
    time_limit = int(data.get('time_limit', 30))
    warning_1 = int(data.get('warning_1', 5))
    warning_2 = int(data.get('warning_2', 1))
    
    print(f"Admin saving timer settings - Enabled: {enabled} (type: {type(enabled)}), Time Limit: {time_limit}")
    
    # Validate
    if time_limit < 5 or time_limit > 180:
        return jsonify({'success': False, 'error': 'Time limit must be between 5 and 180 minutes'}), 400
    
    if warning_1 > 0 and warning_2 > 0 and warning_2 >= warning_1:
        return jsonify({'success': False, 'error': 'Final warning must be less than first warning'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        
        # Try to create table if it doesn't exist
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS timer_settings (
                    setting_id INT PRIMARY KEY DEFAULT 1,
                    enabled TINYINT(1) DEFAULT 1,
                    time_limit INT DEFAULT 30,
                    warning_1 INT DEFAULT 5,
                    warning_2 INT DEFAULT 1,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    updated_by INT,
                    FOREIGN KEY (updated_by) REFERENCES users(user_id)
                )
            """)
            conn.commit()
        except Exception as e:
            print(f"Table creation skipped (might already exist): {e}")
            pass
        
        # Insert or update settings
        cursor.execute("""
            INSERT INTO timer_settings (setting_id, enabled, time_limit, warning_1, warning_2, updated_by)
            VALUES (1, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                enabled = VALUES(enabled),
                time_limit = VALUES(time_limit),
                warning_1 = VALUES(warning_1),
                warning_2 = VALUES(warning_2),
                updated_by = VALUES(updated_by),
                updated_at = CURRENT_TIMESTAMP
        """, (enabled, time_limit, warning_1, warning_2, session.get('user_id')))
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Timer settings saved successfully',
            'data': {
                'enabled': enabled,
                'time_limit': time_limit,
                'warning_1': warning_1,
                'warning_2': warning_2
            }
        })
        
    except Exception as e:
        print(f"Error saving timer settings: {str(e)}")
        if conn:
            conn.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Note: Additional admin routes should be migrated here from app.py
# Including: user management, evaluation management, etc.
