"""
Authentication routes blueprint for IntellEvalPro
Handles login, logout, signup, and password recovery
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import User
from utils import check_password_hash

# Create blueprint
auth_bp = Blueprint('auth', __name__)


def log_activity(user_id=None, user_name=None, user_role=None, activity_type='', 
                description='', reason=None, target_user=None, ip_address=None, 
                additional_data=None):
    """
    Helper function to log activities
    Import log_activity from api routes to avoid circular imports
    """
    try:
        from models import get_db_connection
        import json
        
        conn = get_db_connection()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        # Convert additional_data to JSON string if it's a dict
        additional_data_json = None
        if additional_data:
            additional_data_json = json.dumps(additional_data) if isinstance(additional_data, dict) else additional_data
        
        cursor.execute("""
            INSERT INTO activity_logs 
            (user_id, user_name, user_role, activity_type, description, reason, 
             target_user, ip_address, additional_data)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, user_name, user_role, activity_type, description, reason, 
              target_user, ip_address, additional_data_json))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Error logging activity: {str(e)}")
        return False


@auth_bp.route('/')
def index():
    """Redirect to login page"""
    return redirect(url_for('auth.login'))


@auth_bp.route('/login.html', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    from datetime import datetime, timedelta
    from flask import make_response
    
    # If user is already logged in (GET request with active session), redirect to dashboard
    if request.method == 'GET' and 'user_id' in session and 'role' in session:
        role = session.get('role')
        if role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif role == 'guidance':
            return redirect(url_for('guidance.guidance_dashboard'))
        elif role == 'student':
            return redirect(url_for('student.student_dashboard'))
    
    error_message = None
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Authenticate user
        user = User.authenticate(username, password)
        
        if user:
            # Make session permanent (will use PERMANENT_SESSION_LIFETIME from config)
            session.permanent = True
            
            # Store user information in session
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['first_name'] = user.get('first_name', '')
            session['last_name'] = user.get('last_name', '')
            session['email'] = user.get('email', '')
            
            # Store login timestamp for session tracking
            session['login_time'] = datetime.now().isoformat()
            session['last_activity'] = datetime.now().isoformat()
            
            # Update last login
            User.update_last_login(user['user_id'])
            
            # Log successful login activity
            log_activity(
                user_id=user['user_id'],
                user_name=f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or username,
                user_role=user['role'],
                activity_type='login',
                description=f"User logged in successfully",
                ip_address=request.remote_addr
            )
            
            # Redirect based on role using url_for
            if user['role'] == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            elif user['role'] == 'student':
                return redirect(url_for('student.student_dashboard'))
            elif user['role'] == 'guidance':
                return redirect(url_for('guidance.guidance_dashboard'))
            else:
                error_message = "Invalid user role"
        else:
            # Log failed login attempt
            log_activity(
                user_name=username,
                activity_type='login',
                description=f"Failed login attempt for username: {username}",
                ip_address=request.remote_addr
            )
            error_message = "Invalid username or password"
    
    return render_template('public/login.html', error=error_message)


@auth_bp.route('/logout')
def logout():
    """Handle user logout - only if intentional (not browser back button)"""
    from flask import make_response
    
    # Check if this is an intentional logout or browser back button
    # Browser back will typically be a GET with referer from an authenticated page
    referer = request.headers.get('Referer', '')
    user_agent = request.headers.get('User-Agent', '')
    
    # Only proceed with logout if session exists
    if 'user_id' not in session:
        # Already logged out, just redirect to login
        return redirect(url_for('auth.login'))
    
    # Log logout activity before clearing session
    log_activity(
        user_id=session.get('user_id'),
        user_name=f"{session.get('first_name', '')} {session.get('last_name', '')}".strip() or session.get('username', 'Unknown'),
        user_role=session.get('role'),
        activity_type='logout',
        description='User logged out',
        ip_address=request.remote_addr
    )
    
    # Store user role before clearing session
    user_role = session.get('role', 'student')
    
    session.clear()
    
    # Create response with cache prevention headers
    response = make_response(redirect(url_for('auth.login')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    # Add header to indicate this was a logout
    response.set_cookie('just_logged_out', 'true', max_age=5)
    
    return response


@auth_bp.route('/forgot-password.html')
@auth_bp.route('/forgot-password')
def forgot_password():
    """Show forgot password page"""
    return render_template('public/forgot-password.html')


@auth_bp.route('/reset-password.html')
@auth_bp.route('/reset-password')
def reset_password():
    """Show reset password page"""
    return render_template('public/reset-password.html')


@auth_bp.route('/signup.html')
@auth_bp.route('/signup')
def signup():
    """Show signup page"""
    return render_template('public/signup.html')


@auth_bp.route('/signup', methods=['POST'])
def signup_post():
    """Handle student signup - automatically creates user account"""
    from models import get_db_connection
    from utils.security import generate_password_hash
    from datetime import datetime
    import json
    
    try:
        data = request.get_json()
        
        # Validate required fields (removed password from required since it's auto-generated)
        required_fields = ['student_number', 'first_name', 'last_name', 'email', 
                          'gender', 'birthdate', 'program_id', 'year_level', 'section_id']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return {
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }, 400
        
        conn = get_db_connection()
        if not conn:
            return {'success': False, 'message': 'Database connection failed'}, 500
        
        cursor = conn.cursor(dictionary=True)
        
        # Check if student number already exists in std_info table
        cursor.execute(
            "SELECT id, std_Surname, std_Firstname FROM std_info WHERE std_Number = %s",
            (data['student_number'],)
        )
        student = cursor.fetchone()
        
        # If student exists, verify name matches
        if student:
            if (student['std_Firstname'].lower() != data['first_name'].lower() or 
                student['std_Surname'].lower() != data['last_name'].lower()):
                cursor.close()
                conn.close()
                return {
                    'success': False,
                    'message': 'Student name does not match existing records. Please check your details.'
                }, 400
        
        # Check if username (student_number) already has an account
        cursor.execute(
            "SELECT user_id FROM users WHERE username = %s",
            (data['student_number'],)
        )
        existing_user = cursor.fetchone()
        
        if existing_user:
            cursor.close()
            conn.close()
            return {
                'success': False,
                'message': 'An account with this student number already exists. Please login or reset your password.'
            }, 400
        
        # Auto-generate password: lastname + student_number (no spaces)
        auto_password = f"{data['last_name']}{data['student_number']}"
        hashed_password = generate_password_hash(auto_password)
        now = datetime.now()
        
        # Create user account automatically
        user_insert_query = """
            INSERT INTO users (username, password, email, first_name, last_name, 
                             role, is_active, is_verified, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        user_values = (
            data['student_number'],  # username = student number
            hashed_password,
            data['email'],
            data['first_name'],
            data['last_name'],
            'student',
            1,  # is_active
            1,  # is_verified
            now,
            now
        )
        
        cursor.execute(user_insert_query, user_values)
        user_id = cursor.lastrowid
        
        # Insert or update student info in std_info table
        if student:
            # Update existing student record
            update_query = """
                UPDATE std_info SET 
                    std_Firstname = %s,
                    std_Middlename = %s,
                    std_Surname = %s,
                    std_Suffix = %s,
                    std_Gender = %s,
                    std_Birthdate = %s,
                    std_Age = %s,
                    std_EmailAdd = %s,
                    std_ContactNum = %s,
                    std_Address = %s
                WHERE std_Number = %s
            """
            update_values = (
                data['first_name'],
                data.get('middle_name', ''),
                data['last_name'],
                data.get('suffix', ''),
                data['gender'],
                data['birthdate'],
                data.get('age', 0),
                data['email'],
                data.get('phone', ''),
                data.get('address', ''),
                data['student_number']
            )
            cursor.execute(update_query, update_values)
        else:
            # Insert new student record
            insert_query = """
                INSERT INTO std_info (
                    std_Number, std_Firstname, std_Middlename, std_Surname, std_Suffix,
                    std_Gender, std_Birthdate, std_Age, std_EmailAdd, std_ContactNum, std_Address,
                    std_FatherName, std_MotherName, std_Status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            insert_values = (
                data['student_number'],
                data['first_name'],
                data.get('middle_name', ''),
                data['last_name'],
                data.get('suffix', ''),
                data['gender'],
                data['birthdate'],
                data.get('age', 0),
                data['email'],
                data.get('phone', ''),
                data.get('address', ''),
                data.get('guardian_name', ''),
                data.get('guardian_name', ''),  # Using same for mother if not specified
                data.get('status', 'Enrolled')
            )
            cursor.execute(insert_query, insert_values)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Log activity
        log_activity(
            user_id=user_id,
            user_name=f"{data['first_name']} {data['last_name']}",
            user_role='student',
            activity_type='signup',
            description=f"Student signed up: {data['student_number']} - Account auto-created",
            ip_address=request.remote_addr,
            additional_data={
                'auto_generated_password': True,
                'password_format': 'lastname+studentnumber'
            }
        )
        
        return {
            'success': True,
            'message': f'Account created successfully! Your password is: {data["last_name"]}{data["student_number"]} (Please save this password)',
            'username': data['student_number'],
            'auto_password': auto_password
        }, 201
        
    except Exception as e:
        print(f"Error in signup: {e}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'message': 'An error occurred during signup. Please try again.'
        }, 500


@auth_bp.route('/create-admin', methods=['GET'])
def create_admin():
    """Create admin user manually (development helper)"""
    existing = User.get_by_username('admin')
    if existing:
        return "Admin user already exists!"
    
    user_id = User.create(
        username='admin',
        password='12345',
        email='admin@intellevalpro.com',
        first_name='System',
        last_name='Administrator',
        role='admin'
    )
    
    if user_id:
        return "Admin user created successfully! Username: admin, Password: 12345"
    return "Error creating admin user"


@auth_bp.route('/create-guidance', methods=['GET'])
def create_guidance():
    """Create guidance counselor user manually (development helper)"""
    existing = User.get_by_username('guidance')
    if existing:
        return "Guidance user already exists!"
    
    user_id = User.create(
        username='guidance',
        password='12345',
        email='guidance@intellevalpro.com',
        first_name='Dr. Sarah',
        last_name='Brooks',
        role='guidance'
    )
    
    if user_id:
        return "Guidance user created successfully! Username: guidance, Password: 12345"
    return "Error creating guidance user"
