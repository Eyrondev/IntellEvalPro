"""
Student routes blueprint for IntellEvalPro
Handles all student-related routes and functionality
"""
from flask import Blueprint, render_template, session, redirect, url_for, request
from utils import student_required
from models import Student, Evaluation, get_db_connection
from utils.json_encoder import jsonify
from datetime import datetime

# Create blueprint
student_bp = Blueprint('student', __name__, url_prefix='/student')


@student_bp.route('/no-active-evaluation')
@student_required
def no_active_evaluation():
    """Display page when no active evaluation periods exist"""
    current_year = datetime.now().year
    return render_template('student/no-active-evaluation.html', current_year=current_year)


@student_bp.route('/dashboard')
@student_bp.route('/student-dashboard')  # Keep for backward compatibility
@student_required
def student_dashboard():
    """Student dashboard page"""
    from datetime import datetime
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        user_id = session.get('user_id')
        first_name = session.get('first_name', 'Student')
        last_name = session.get('last_name', '')
        student_name = f"{first_name} {last_name}".strip()
        
        # Get student_id from std_info using user_id
        cursor.execute("SELECT id FROM std_info WHERE user_id = %s", (user_id,))
        student_record = cursor.fetchone()
        
        print(f"DEBUG: user_id={user_id}, student_record={student_record}")
        
        if not student_record:
            # No student record found - return empty data
            print(f"WARNING: No student record found for user_id={user_id}")
            cursor.close()
            conn.close()
            data = {
                'student_name': student_name,
                'total_evaluations': 0,
                'completed_evaluations': 0,
                'progress_percentage': 0,
                'evaluation_period': None,
                'pending_evaluations': [],
                'recent_evaluations': []
            }
            return render_template('student/student-dashboard.html', data=data)
        
        student_id = student_record['id']
        print(f"DEBUG: student_id={student_id}")
        
        # Get current evaluation period
        cursor.execute("""
            SELECT period_id as id, title, start_date, end_date, status,
                   DATEDIFF(end_date, CURDATE()) as days_remaining
            FROM evaluation_periods
            WHERE status = 'Active'
            ORDER BY start_date DESC
            LIMIT 1
        """)
        period = cursor.fetchone()
        
        print(f"DEBUG: Active period found: {period}")
        
        # If no active evaluation period, redirect to no-active-evaluation page
        if not period:
            cursor.close()
            conn.close()
            return redirect(url_for('student.no_active_evaluation'))
        
        evaluation_period = None
        if period:
            start_date = period.get('start_date')
            end_date = period.get('end_date')
            days_remaining = period.get('days_remaining', 0)
            
            # Calculate time progress percentage
            time_progress = 0
            if start_date and end_date:
                if isinstance(start_date, str):
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                if isinstance(end_date, str):
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                
                total_days = (end_date - start_date).days
                elapsed_days = (datetime.now() - start_date).days
                
                if total_days > 0:
                    time_progress = int((elapsed_days / total_days) * 100)
                    time_progress = max(0, min(100, time_progress))
                
                evaluation_period = {
                    'title': period.get('title', 'Current Evaluation Period'),
                    'status': period.get('status', 'Active'),
                    'start_date': start_date.strftime('%B %d, %Y'),
                    'end_date': end_date.strftime('%B %d, %Y'),
                    'days_remaining': max(0, days_remaining) if days_remaining else 0,
                    'time_progress': time_progress
                }
        
        # Get evaluation statistics for current period
        if period:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed,
                    SUM(CASE WHEN status IN ('Pending', 'In Progress', 'Expired') THEN 1 ELSE 0 END) as pending
                FROM evaluations
                WHERE student_id = %s
                AND period_id = %s
            """, (student_id, period['id']))
            stats = cursor.fetchone()
            
            total_evaluations = stats['total'] or 0
            completed_evaluations = stats['completed'] or 0
            pending_count = stats['pending'] or 0
            
            print(f"DEBUG: Evaluation stats - total: {total_evaluations}, completed: {completed_evaluations}, pending: {pending_count}")
        else:
            total_evaluations = 0
            completed_evaluations = 0
            pending_count = 0
            print("DEBUG: No active period - setting stats to 0")
        
        progress_percentage = int((completed_evaluations / total_evaluations * 100)) if total_evaluations > 0 else 0
        
        # Get pending evaluations (limit to 5 for dashboard)
        cursor.execute("""
            SELECT e.evaluation_id, e.status,
                   CONCAT(f.first_name, ' ', f.last_name) as faculty_name,
                   s.subject_code as course_code, s.title as course_name,
                   p.name as department,
                   ep.end_date
            FROM evaluations e
            JOIN class_sections cs ON e.section_id = cs.section_id
            JOIN faculty f ON cs.faculty_id = f.faculty_id
            JOIN subjects s ON cs.subject_id = s.subject_id
            JOIN programs p ON f.program_id = p.program_id
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE e.student_id = %s
            AND e.status IN ('Pending', 'In Progress', 'Expired')
            AND ep.status = 'Active'
            ORDER BY ep.end_date ASC
            LIMIT 5
        """, (student_id,))
        pending_evaluations = cursor.fetchall()
        
        print(f"DEBUG: Found {len(pending_evaluations)} pending evaluations")
        
        # Get all completed evaluations for current period
        cursor.execute("""
            SELECT e.evaluation_id, e.completion_time,
                   CONCAT(f.first_name, ' ', f.last_name) as faculty_name,
                   s.subject_code as course_code, s.title as course_title,
                   p.name as department
            FROM evaluations e
            JOIN class_sections cs ON e.section_id = cs.section_id
            JOIN faculty f ON cs.faculty_id = f.faculty_id
            JOIN subjects s ON cs.subject_id = s.subject_id
            JOIN programs p ON f.program_id = p.program_id
            WHERE e.student_id = %s
            AND e.status = 'Completed'
            AND e.period_id = %s
            ORDER BY e.completion_time DESC
        """, (student_id, period['id'] if period else None))
        recent_evaluations = cursor.fetchall()
        
        print(f"DEBUG: Found {len(recent_evaluations)} recent evaluations")
        
        cursor.close()
        conn.close()
        
        # Prepare dashboard data
        data = {
            'student_name': student_name,
            'total_evaluations': total_evaluations,
            'completed_evaluations': completed_evaluations,
            'progress_percentage': progress_percentage,
            'evaluation_period': evaluation_period,
            'pending_evaluations': pending_evaluations,
            'recent_evaluations': recent_evaluations
        }
        
        return render_template('student/student-dashboard.html', data=data)
    
    except Exception as e:
        print(f"Error in student_dashboard: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return fallback data
        data = {
            'student_name': session.get('first_name', 'Student'),
            'total_evaluations': 0,
            'completed_evaluations': 0,
            'progress_percentage': 0,
            'evaluation_period': None,
            'pending_evaluations': [],
            'recent_evaluations': []
        }
        return render_template('student/student-dashboard.html', data=data)


@student_bp.route('/pending-evaluations')
@student_required
def pending_evaluations():
    """Pending evaluations page"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        user_id = session.get('user_id')
        
        # Get student_id from std_info using user_id
        cursor.execute("SELECT id FROM std_info WHERE user_id = %s", (user_id,))
        student_record = cursor.fetchone()
        
        if not student_record:
            # No student record found
            cursor.close()
            conn.close()
            return render_template('student/pending-evaluations.html',
                                 current_period=None,
                                 evaluations=[],
                                 completed_evaluations=[],
                                 total_evaluations=0,
                                 completed_count=0,
                                 pending_count=0,
                                 progress_percentage=0)
        
        student_id = student_record['id']
        
        # Get current evaluation period (check for Active status OR date-based active period)
        cursor.execute("""
            SELECT period_id as id, title, start_date, end_date, status,
                   DATEDIFF(end_date, CURDATE()) as days_remaining,
                   CASE 
                       WHEN CURDATE() < start_date THEN 'Upcoming'
                       WHEN CURDATE() > end_date THEN 'Completed'
                       WHEN CURDATE() BETWEEN start_date AND end_date THEN 'Active'
                       ELSE status
                   END as computed_status
            FROM evaluation_periods
            WHERE COALESCE(is_archived, 0) = 0
            AND (
                status = 'Active' 
                OR CURDATE() BETWEEN start_date AND end_date
            )
            ORDER BY 
                CASE WHEN CURDATE() BETWEEN start_date AND end_date THEN 1 ELSE 2 END,
                start_date DESC
            LIMIT 1
        """)
        current_period = cursor.fetchone()
        
        # Update the status to computed_status if available
        if current_period and current_period.get('computed_status'):
            current_period['status'] = current_period['computed_status']
        
        # If no active evaluation period, show empty state but don't redirect
        # (Allow students to see their completed evaluations even without active period)
        
        # Get pending evaluations with faculty and subject info
        # Check for both Active status and date-based active periods
        cursor.execute("""
            SELECT e.evaluation_id, e.status, e.created_at,
                   f.first_name, f.last_name,
                   CONCAT(f.first_name, ' ', f.last_name) as faculty_name,
                   s.subject_code, s.title as subject_title,
                   cs.section_name, cs.schedule, cs.room,
                   ep.title as period_title,
                   ep.end_date,
                   ets.session_id, ets.start_time, ets.time_limit_minutes,
                   CASE 
                       WHEN ets.session_id IS NOT NULL AND 
                            TIMESTAMPDIFF(SECOND, ets.start_time, NOW()) > (ets.time_limit_minutes * 60)
                       THEN 'Expired'
                       ELSE e.status
                   END as display_status
            FROM evaluations e
            JOIN class_sections cs ON e.section_id = cs.section_id
            JOIN faculty f ON cs.faculty_id = f.faculty_id
            JOIN subjects s ON cs.subject_id = s.subject_id
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            LEFT JOIN evaluation_timer_sessions ets ON e.evaluation_id = ets.evaluation_id
            WHERE e.student_id = %s
            AND e.status IN ('Pending', 'In Progress', 'Expired')
            AND COALESCE(ep.is_archived, 0) = 0
            AND (
                ep.status = 'Active'
                OR CURDATE() BETWEEN ep.start_date AND ep.end_date
            )
            ORDER BY ep.end_date ASC, f.last_name ASC
        """, (student_id,))
        evaluations_raw = cursor.fetchall()
        
        # Process evaluations and update expired ones
        evaluations = []
        for eval_data in evaluations_raw:
            # Update status in database if expired
            if eval_data['display_status'] == 'Expired' and eval_data['status'] != 'Expired':
                cursor.execute("""
                    UPDATE evaluations 
                    SET status = 'Expired' 
                    WHERE evaluation_id = %s
                """, (eval_data['evaluation_id'],))
                conn.commit()
                eval_data['status'] = 'Expired'
            else:
                eval_data['status'] = eval_data['display_status']
            
            evaluations.append(eval_data)
        
        # Get completed evaluations
        cursor.execute("""
            SELECT e.evaluation_id, e.status, e.completion_time,
                   CONCAT(f.first_name, ' ', f.last_name) as faculty_name,
                   s.subject_code, s.title as subject_title,
                   ep.title as period_title
            FROM evaluations e
            JOIN class_sections cs ON e.section_id = cs.section_id
            JOIN faculty f ON cs.faculty_id = f.faculty_id
            JOIN subjects s ON cs.subject_id = s.subject_id
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE e.student_id = %s
            AND e.status = 'Completed'
            ORDER BY e.completion_time DESC
            LIMIT 5
        """, (student_id,))
        completed_evaluations = cursor.fetchall()
        
        # Calculate statistics
        if current_period:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed,
                    SUM(CASE WHEN status IN ('Pending', 'In Progress', 'Expired') THEN 1 ELSE 0 END) as pending
                FROM evaluations
                WHERE student_id = %s
                AND period_id = %s
            """, (student_id, current_period['id']))
            stats = cursor.fetchone()
        else:
            stats = {'total': 0, 'completed': 0, 'pending': 0}
        
        total_evaluations = stats['total'] or 0
        completed_count = stats['completed'] or 0
        pending_count = stats['pending'] or 0
        progress_percentage = int((completed_count / total_evaluations * 100)) if total_evaluations > 0 else 0
        
        cursor.close()
        conn.close()
        
        return render_template('student/pending-evaluations.html',
                             current_period=current_period,
                             evaluations=evaluations,
                             completed_evaluations=completed_evaluations,
                             total_evaluations=total_evaluations,
                             completed_count=completed_count,
                             pending_count=pending_count,
                             progress_percentage=progress_percentage)
    
    except Exception as e:
        print(f"Error in pending_evaluations: {str(e)}")
        import traceback
        traceback.print_exc()
        return render_template('student/pending-evaluations.html',
                             current_period=None,
                             evaluations=[],
                             completed_evaluations=[],
                             total_evaluations=0,
                             completed_count=0,
                             pending_count=0,
                             progress_percentage=0)


@student_bp.route('/my-evaluations')
@student_required
def my_evaluations():
    """Student evaluations history page"""
    return render_template('student/my-evaluations.html')


@student_bp.route('/evaluation/<int:evaluation_id>')
@student_bp.route('/evaluation-form/<int:evaluation_id>')  # Keep for backward compatibility
@student_required
def evaluation_form(evaluation_id):
    """Evaluation form page"""
    from datetime import datetime
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        user_id = session.get('user_id')
        
        # Get evaluation details with student information and period status
        cursor.execute("""
            SELECT e.evaluation_id, e.section_id, e.period_id, e.status,
                   CONCAT(f.first_name, ' ', f.last_name) as faculty_name,
                   s.subject_code, s.title as subject_title,
                   cs.section_name,
                   ep.title as period_title,
                   ep.status as period_status,
                   ep.end_date as period_end_date,
                   si.std_Course, si.std_Level
            FROM evaluations e
            JOIN class_sections cs ON e.section_id = cs.section_id
            JOIN faculty f ON cs.faculty_id = f.faculty_id
            JOIN subjects s ON cs.subject_id = s.subject_id
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            LEFT JOIN std_info si ON si.user_id = %s
            WHERE e.evaluation_id = %s
        """, (user_id, evaluation_id,))
        
        evaluation = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not evaluation:
            return redirect(url_for('student.pending_evaluations'))
        
        # Check if evaluation period is still active
        period_status = evaluation.get('period_status', '')
        period_end_date = evaluation.get('period_end_date')
        current_datetime = datetime.now()
        
        # Validate period is active and not expired
        if period_status != 'Active':
            return redirect(url_for('student.no_active_evaluation'))
        
        # Check if period end date has passed
        if period_end_date:
            if isinstance(period_end_date, str):
                period_end_date = datetime.strptime(period_end_date, '%Y-%m-%d')
            
            if current_datetime.date() > period_end_date.date():
                return redirect(url_for('student.no_active_evaluation'))
        
        # Format current date
        current_date = current_datetime.strftime('%B %d, %Y')
        
        # Get section name from class_sections table
        section_name = evaluation.get('section_name', '')
        
        return render_template('student/evaluation-form.html', 
                             evaluation_id=evaluation_id,
                             section_id=evaluation['section_id'],
                             period_id=evaluation['period_id'],
                             faculty_name=evaluation['faculty_name'],
                             course_code=evaluation['subject_code'],
                             subject_title=evaluation['subject_title'],
                             section_name=section_name,
                             period_title=evaluation['period_title'],
                             current_date=current_date)
    except Exception as e:
        print(f"Error loading evaluation form: {str(e)}")
        return redirect(url_for('student.pending_evaluations'))


@student_bp.route('/settings', methods=['GET', 'POST'])
@student_required
def settings():
    """Student settings page"""
    return render_template('student/settings.html')


@student_bp.route('/help-support')
@student_required
def help_support():
    """Help and support page"""
    return render_template('student/help-support.html')


@student_bp.route('/evaluation-status/<int:evaluation_id>')
@student_required
def evaluation_status(evaluation_id):
    """Debug route to check evaluation status and timing"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get evaluation details with timing
        cursor.execute("""
            SELECT e.evaluation_id, e.status, e.start_time, e.completion_time,
                   e.created_at, e.updated_at,
                   CONCAT(f.first_name, ' ', f.last_name) as faculty_name,
                   s.subject_code, s.title as subject_title
            FROM evaluations e
            JOIN class_sections cs ON e.section_id = cs.section_id
            JOIN faculty f ON cs.faculty_id = f.faculty_id
            JOIN subjects s ON cs.subject_id = s.subject_id
            WHERE e.evaluation_id = %s
        """, (evaluation_id,))
        
        evaluation = cursor.fetchone()
        
        # Get comments for this evaluation
        cursor.execute("""
            SELECT comment_id, comment_text, sentiment, created_at
            FROM comments
            WHERE evaluation_id = %s
        """, (evaluation_id,))
        
        comments = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'evaluation': evaluation,
            'comments': comments
        })
        
    except Exception as e:
        print(f"Error getting evaluation status: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@student_bp.route('/navigation')
@student_required
def navigation():
    """Student navigation component"""
    pending_count = Student.get_pending_evaluation_count(session['user_id'])
    
    # Get student name and initial from session
    first_name = session.get('first_name', '')
    last_name = session.get('last_name', '')
    student_name = f"{first_name} {last_name}".strip() or 'Student'
    student_initial = first_name[0].upper() if first_name else 'S'
    
    return render_template('student/components/navigation.html', 
                         pending_count=pending_count,
                         student_name=student_name,
                         student_initial=student_initial)


@student_bp.route('/header')
@student_required
def header():
    """Student header component"""
    return render_template('student/components/header.html')


@student_bp.route('/footer')
@student_required
def footer():
    """Student footer component"""
    return render_template('student/footer.html')


@student_bp.route('/save-draft', methods=['POST'])
@student_required
def save_draft():
    """Save evaluation draft"""
    try:
        data = request.get_json()
        evaluation_id = data.get('evaluation_id')
        form_data = data.get('form_data')
        
        if not evaluation_id:
            return jsonify({'success': False, 'message': 'Evaluation ID is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Convert form data to JSON string
        import json
        draft_json = json.dumps(form_data)
        
        # Check if draft exists
        cursor.execute("SELECT id FROM evaluation_drafts WHERE evaluation_id = %s", (evaluation_id,))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing draft
            cursor.execute("""
                UPDATE evaluation_drafts 
                SET draft_data = %s, updated_at = NOW()
                WHERE evaluation_id = %s
            """, (draft_json, evaluation_id))
        else:
            # Insert new draft
            cursor.execute("""
                INSERT INTO evaluation_drafts (evaluation_id, draft_data)
                VALUES (%s, %s)
            """, (evaluation_id, draft_json))
        
        # Update evaluation status to In Progress
        cursor.execute("""
            UPDATE evaluations 
            SET status = 'In Progress', updated_at = NOW()
            WHERE evaluation_id = %s AND status = 'Pending'
        """, (evaluation_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Draft saved successfully'})
        
    except Exception as e:
        print(f"Error saving draft: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500


@student_bp.route('/load-draft/<int:evaluation_id>')
@student_required
def load_draft(evaluation_id):
    """Load evaluation draft"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT draft_data 
            FROM evaluation_drafts 
            WHERE evaluation_id = %s
        """, (evaluation_id,))
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result and result['draft_data']:
            import json
            draft_data = json.loads(result['draft_data'])
            return jsonify({'success': True, 'draft_data': draft_data})
        else:
            return jsonify({'success': False, 'message': 'No draft found'})
            
    except Exception as e:
        print(f"Error loading draft: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@student_bp.route('/start-evaluation', methods=['POST'])
@student_required
def start_evaluation():
    """Start an evaluation by recording start_time"""
    try:
        from datetime import datetime
        
        evaluation_id = request.form.get('evaluation_id') or request.json.get('evaluation_id')
        
        if not evaluation_id:
            return jsonify({'success': False, 'message': 'Evaluation ID is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get student_id from std_info using user_id
        user_id = session.get('user_id')
        cursor.execute("SELECT id FROM std_info WHERE user_id = %s", (user_id,))
        student_record = cursor.fetchone()
        
        if not student_record:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': 'Student record not found'}), 404
        
        student_id = student_record['id']
        
        # Verify this evaluation belongs to this student and check period status
        cursor.execute("""
            SELECT e.evaluation_id, e.status, e.start_time,
                   ep.status as period_status, ep.end_date as period_end_date
            FROM evaluations e
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE e.evaluation_id = %s AND e.student_id = %s
        """, (evaluation_id, student_id))
        
        eval_check = cursor.fetchone()
        if not eval_check:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': 'Evaluation not found or access denied'}), 403
        
        if eval_check['status'] == 'Completed':
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': 'This evaluation has already been completed'}), 400
        
        # Check if evaluation period is still active
        period_status = eval_check.get('period_status', '')
        period_end_date = eval_check.get('period_end_date')
        
        if period_status != 'Active':
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': 'This evaluation period is no longer active'}), 400
        
        # Check if period end date has passed
        if period_end_date:
            if isinstance(period_end_date, str):
                period_end_date = datetime.strptime(period_end_date, '%Y-%m-%d')
            
            if datetime.now().date() > period_end_date.date():
                cursor.close()
                conn.close()
                return jsonify({'success': False, 'message': 'This evaluation period has ended'}), 400
        
        # Update evaluation status to 'In Progress' and set start_time if not already set
        if not eval_check['start_time']:
            cursor.execute("""
                UPDATE evaluations 
                SET status = 'In Progress',
                    start_time = NOW(),
                    updated_at = NOW()
                WHERE evaluation_id = %s
            """, (evaluation_id,))
        else:
            # Just update status if start_time already exists
            cursor.execute("""
                UPDATE evaluations 
                SET status = 'In Progress',
                    updated_at = NOW()
                WHERE evaluation_id = %s
            """, (evaluation_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Evaluation started successfully!',
            'evaluation_id': evaluation_id
        })
        
    except Exception as e:
        print(f"Error starting evaluation: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'An error occurred while starting the evaluation. Please try again.'}), 500


@student_bp.route('/submit-evaluation', methods=['POST'])
@student_required
def submit_evaluation():
    """Submit completed evaluation"""
    try:
        from datetime import datetime
        import json
        
        evaluation_id = request.form.get('evaluation_id')
        section_id = request.form.get('section_id')
        period_id = request.form.get('period_id')
        
        if not evaluation_id:
            return jsonify({'success': False, 'message': 'Evaluation ID is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get student_id from std_info using user_id
        user_id = session.get('user_id')
        cursor.execute("SELECT id FROM std_info WHERE user_id = %s", (user_id,))
        student_record = cursor.fetchone()
        
        if not student_record:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': 'Student record not found'}), 404
        
        student_id = student_record['id']
        
        # Verify this evaluation belongs to this student and check period status
        cursor.execute("""
            SELECT e.evaluation_id, e.status,
                   ep.status as period_status, ep.end_date as period_end_date
            FROM evaluations e
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE e.evaluation_id = %s AND e.student_id = %s
        """, (evaluation_id, student_id))
        
        eval_check = cursor.fetchone()
        if not eval_check:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': 'Evaluation not found or access denied'}), 403
        
        if eval_check['status'] == 'Completed':
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': 'This evaluation has already been submitted'}), 400
        
        # Check if evaluation period is still active
        period_status = eval_check.get('period_status', '')
        period_end_date = eval_check.get('period_end_date')
        
        if period_status != 'Active':
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': 'This evaluation period is no longer active. Submission not allowed.'}), 400
        
        # Check if period end date has passed
        if period_end_date:
            if isinstance(period_end_date, str):
                period_end_date = datetime.strptime(period_end_date, '%Y-%m-%d')
            
            if datetime.now().date() > period_end_date.date():
                cursor.close()
                conn.close()
                return jsonify({'success': False, 'message': 'This evaluation period has ended. Submission not allowed.'}), 400
        
        # Collect all form responses from dynamic criteria fields
        # Fields are named: criteria_1, criteria_2, criteria_3, etc.
        responses_data = []
        total_rating = 0
        response_count = 0
        
        # Iterate through all form fields looking for criteria_* fields
        for field_name, value in request.form.items():
            # Check if this is a criteria rating field
            if field_name.startswith('criteria_') and field_name != 'criteria_id':
                try:
                    # Extract criteria_id from field name (e.g., criteria_15 -> 15)
                    criteria_id = int(field_name.split('_')[1])
                    rating_value = int(value)
                    
                    # Validate rating is in range
                    if 1 <= rating_value <= 5:
                        total_rating += rating_value
                        response_count += 1
                        
                        responses_data.append({
                            'criteria_id': criteria_id,
                            'rating': rating_value
                        })
                    else:
                        print(f"Warning: Invalid rating value {rating_value} for criteria {criteria_id}")
                        
                except (ValueError, IndexError) as e:
                    print(f"Warning: Could not parse field {field_name}: {e}")
                    continue
        
        # Calculate average rating
        average_rating = round(total_rating / response_count, 2) if response_count > 0 else 0
        
        # Collect comments - now using single comment field
        comments = request.form.get('comments', '').strip()
        
        # Update evaluation status
        cursor.execute("""
            UPDATE evaluations 
            SET status = 'Completed',
                completion_time = NOW(),
                updated_at = NOW()
            WHERE evaluation_id = %s
        """, (evaluation_id,))
        
        # Insert all responses
        for response in responses_data:
            cursor.execute("""
                INSERT INTO evaluation_responses (evaluation_id, criteria_id, rating)
                VALUES (%s, %s, %s)
            """, (evaluation_id, response['criteria_id'], response['rating']))
        
        # Delete any existing draft since evaluation is now completed
        cursor.execute("DELETE FROM evaluation_drafts WHERE evaluation_id = %s", (evaluation_id,))
        
        # Store comment in the comments table if provided
        if comments:
            cursor.execute("""
                INSERT INTO comments (evaluation_id, comment_text, sentiment, created_at)
                VALUES (%s, %s, %s, NOW())
            """, (evaluation_id, comments, 'Neutral'))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': 'Evaluation submitted successfully!',
            'redirect': url_for('student.pending_evaluations')
        })
        
    except Exception as e:
        print(f"Error submitting evaluation: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'An error occurred while submitting the evaluation. Please try again.'}), 500


# ========================================
# EVALUATION TIMER API ENDPOINTS
# ========================================
# EVALUATION TIMER API ENDPOINTS
# ========================================
# NOTE: Timer endpoints have been moved to routes/api.py
# - POST /api/evaluation/start
# - GET  /api/evaluation/check-time/<session_id>
# These endpoints use the evaluation_timer_sessions table
# ========================================
