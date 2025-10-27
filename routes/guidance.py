"""
Guidance routes blueprint for IntellEvalPro
Handles all guidance counselor-related routes and functionality
"""
from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from utils import guidance_required
from models.database import get_db_connection

# Create blueprint
guidance_bp = Blueprint('guidance', __name__, url_prefix='/guidance')


@guidance_bp.route('/dashboard')
@guidance_bp.route('/guidance-dashboard')  # Keep for backward compatibility
@guidance_required
def guidance_dashboard():
    """Guidance counselor dashboard page"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get current academic term with year info
        cursor.execute("""
            SELECT 
                at.acad_term_id,
                at.term_name,
                at.term_code,
                ay.year_code,
                ay.year_name,
                CONCAT(ay.year_code, ' - ', at.term_name) as display_term
            FROM academic_terms at
            INNER JOIN academic_years ay ON at.acad_year_id = ay.acad_year_id
            WHERE at.is_current = 1
            LIMIT 1
        """)
        current_term = cursor.fetchone()
        
        if not current_term:
            # Fallback to most recent term
            cursor.execute("""
                SELECT 
                    at.acad_term_id,
                    at.term_name,
                    at.term_code,
                    ay.year_code,
                    ay.year_name,
                    CONCAT(ay.year_code, ' - ', at.term_name) as display_term
                FROM academic_terms at
                INNER JOIN academic_years ay ON at.acad_year_id = ay.acad_year_id
                ORDER BY at.acad_term_id DESC
                LIMIT 1
            """)
            current_term = cursor.fetchone()
        
        # Get current active period
        cursor.execute("""
            SELECT period_id, title, start_date, end_date
            FROM evaluation_periods 
            WHERE status = 'Active' 
            ORDER BY start_date DESC 
            LIMIT 1
        """)
        current_period = cursor.fetchone()
        
        if not current_period:
            # Fallback to most recent period if no active period
            cursor.execute("""
                SELECT period_id, title, start_date, end_date
                FROM evaluation_periods 
                ORDER BY start_date DESC 
                LIMIT 1
            """)
            current_period = cursor.fetchone()
        
        # Get total faculty count
        cursor.execute("SELECT COUNT(*) as total_faculty FROM faculty WHERE status = 'Active'")
        total_faculty = cursor.fetchone()['total_faculty'] or 0
        
        # Get total departments count (count all programs/departments)
        cursor.execute("""
            SELECT COUNT(*) as total_departments 
            FROM programs
        """)
        total_departments = cursor.fetchone()['total_departments'] or 0
        
        # Get evaluation statistics
        if current_period:
            # Get faculty who have been evaluated in current period
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT cs.faculty_id) as evaluated_faculty,
                    COUNT(DISTINCT e.evaluation_id) as total_evaluations,
                    AVG(er.rating) as average_rating
                FROM evaluations e 
                JOIN class_sections cs ON e.section_id = cs.section_id
                LEFT JOIN evaluation_responses er ON e.evaluation_id = er.evaluation_id
                WHERE e.period_id = %s AND e.status = 'Completed'
            """, (current_period['period_id'],))
            eval_stats = cursor.fetchone()
            
            evaluated_faculty = eval_stats['evaluated_faculty'] or 0
            total_evaluations = eval_stats['total_evaluations'] or 0
            average_rating = float(eval_stats['average_rating'] or 0)
        else:
            evaluated_faculty = 0
            total_evaluations = 0
            average_rating = 0.0
        
        # Calculate completion rate
        completion_rate = round((evaluated_faculty / total_faculty * 100) if total_faculty > 0 else 0, 1)
        
        # Get top faculty rankings
        faculty_rankings = []
        if current_period:
            cursor.execute("""
                SELECT 
                    f.faculty_id,
                    CONCAT(f.first_name, ' ', f.last_name) as name,
                    p.name as department,
                    f.rank as position,
                    AVG(er.rating) as avg_rating,
                    COUNT(DISTINCT e.evaluation_id) as evaluation_count
                FROM faculty f
                JOIN programs p ON f.program_id = p.program_id
                JOIN class_sections cs ON f.faculty_id = cs.faculty_id
                JOIN evaluations e ON cs.section_id = e.section_id
                LEFT JOIN evaluation_responses er ON e.evaluation_id = er.evaluation_id
                WHERE f.status = 'Active' AND e.period_id = %s AND e.status = 'Completed'
                GROUP BY f.faculty_id, f.first_name, f.last_name, p.name, f.rank
                HAVING COUNT(DISTINCT e.evaluation_id) > 0
                ORDER BY avg_rating DESC, evaluation_count DESC
                LIMIT 10
            """, (current_period['period_id'],))
            faculty_rankings = cursor.fetchall() or []
        
        # Get department performance data (using programs as departments)
        department_stats = []
        if current_period:
            cursor.execute("""
                SELECT 
                    p.name as name,
                    COUNT(DISTINCT f.faculty_id) as faculty_count,
                    AVG(er.rating) as avg_rating,
                    COUNT(DISTINCT e.evaluation_id) as evaluation_count,
                    COUNT(DISTINCT CASE WHEN e.status = 'Completed' THEN e.evaluation_id END) as completed_evaluations,
                    COUNT(DISTINCT e.evaluation_id) as total_evaluations
                FROM programs p
                JOIN faculty f ON p.program_id = f.program_id
                LEFT JOIN class_sections cs ON f.faculty_id = cs.faculty_id
                LEFT JOIN evaluations e ON cs.section_id = e.section_id AND e.period_id = %s
                LEFT JOIN evaluation_responses er ON e.evaluation_id = er.evaluation_id
                WHERE f.status = 'Active'
                GROUP BY p.program_id, p.name
                ORDER BY avg_rating DESC
            """, (current_period['period_id'],))
            department_stats = cursor.fetchall() or []
        
        # Process department stats for charts
        processed_dept_stats = []
        dept_colors = ['blue', 'green', 'orange', 'purple', 'teal', 'indigo', 'red', 'yellow']
        dept_rgb_colors = ['59, 130, 246', '16, 185, 129', '245, 158, 11', '147, 51, 234', '20, 184, 166', '99, 102, 241', '239, 68, 68', '245, 158, 11']
        
        for i, dept in enumerate(department_stats):
            color_index = i % len(dept_colors)
            processed_dept = dict(dept)
            processed_dept['color'] = dept_colors[color_index]
            processed_dept['rgb_color'] = dept_rgb_colors[color_index]
            processed_dept['avg_rating'] = float(processed_dept['avg_rating'] or 0)
            processed_dept['completion_percentage'] = round(
                (processed_dept['completed_evaluations'] / processed_dept['total_evaluations'] * 100)
                if processed_dept['total_evaluations'] > 0 else 0, 1
            )
            processed_dept['trend_data'] = [
                round(max(3.0, processed_dept['avg_rating'] - 0.2 + (j * 0.05)), 1) 
                for j in range(6)
            ]
            processed_dept['trend_value'] = 0.2  # Default positive trend
            processed_dept['trend_direction'] = 'up'
            processed_dept_stats.append(processed_dept)
        
        # Chart labels for trends
        chart_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        
        # Rating distribution data - categorize faculty by their average ratings
        rating_distribution = {'labels': [], 'data': []}
        if current_period:
            # Get average rating for each faculty member
            cursor.execute("""
                SELECT 
                    cs.faculty_id,
                    CONCAT(f.first_name, ' ', f.last_name) as faculty_name,
                    AVG(er.rating) as avg_rating
                FROM class_sections cs
                JOIN faculty f ON cs.faculty_id = f.faculty_id
                JOIN evaluations e ON cs.section_id = e.section_id
                JOIN evaluation_responses er ON e.evaluation_id = er.evaluation_id
                WHERE e.period_id = %s AND e.status = 'Completed'
                GROUP BY cs.faculty_id, f.first_name, f.last_name
                HAVING AVG(er.rating) IS NOT NULL
            """, (current_period['period_id'],))
            
            faculty_ratings = cursor.fetchall() or []
            
            # Define rating categories to match the chart exactly
            rating_categories = {
                '5.0': 0,
                '4.5-4.9': 0,
                '4.0-4.4': 0,
                '3.5-3.9': 0,
                '3.0-3.4': 0,
                'Below 3.0': 0
            }
            
            # Categorize each faculty member's rating
            for faculty in faculty_ratings:
                avg = float(faculty['avg_rating'] or 0)
                if avg == 5.0:
                    rating_categories['5.0'] += 1
                elif avg >= 4.5:
                    rating_categories['4.5-4.9'] += 1
                elif avg >= 4.0:
                    rating_categories['4.0-4.4'] += 1
                elif avg >= 3.5:
                    rating_categories['3.5-3.9'] += 1
                elif avg >= 3.0:
                    rating_categories['3.0-3.4'] += 1
                else:
                    rating_categories['Below 3.0'] += 1
            
            rating_distribution = {
                'labels': list(rating_categories.keys()),
                'data': list(rating_categories.values())
            }
        
        dashboard_data = {
            'current_term': current_term,
            'current_period': current_period,
            'total_faculty': total_faculty,
            'total_departments': total_departments,
            'evaluated_faculty': evaluated_faculty,
            'total_evaluations': total_evaluations,
            'average_rating': round(average_rating, 1),
            'completion_rate': completion_rate,
            'faculty_rankings': faculty_rankings,
            'department_stats': processed_dept_stats,
            'chart_labels': chart_labels,
            'rating_distribution': rating_distribution
        }
        
        cursor.close()
        conn.close()
        
        return render_template('guidance/guidance-dashboard.html', dashboard_data=dashboard_data)
        
    except Exception as e:
        print(f"Error in guidance_dashboard: {str(e)}")
        import traceback
        traceback.print_exc()
        # Return template with empty data in case of error
        dashboard_data = {
            'current_term': None,
            'current_period': None,
            'total_faculty': 0,
            'total_departments': 0,
            'evaluated_faculty': 0,
            'total_evaluations': 0,
            'average_rating': 0.0,
            'completion_rate': 0.0,
            'faculty_rankings': [],
            'department_stats': [],
            'chart_labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'rating_distribution': {'labels': [], 'data': []}
        }
        return render_template('guidance/guidance-dashboard.html', dashboard_data=dashboard_data)


@guidance_bp.route('/student-management')
@guidance_required
def student_management():
    """Student management page"""
    return render_template('guidance/student-management.html')


@guidance_bp.route('/faculty-management')
@guidance_required
def faculty_management():
    """Faculty management page"""
    return render_template('guidance/faculty-management.html')


@guidance_bp.route('/faculty-performance')
@guidance_required
def faculty_performance():
    """Faculty performance analytics page"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get current active period
        cursor.execute("""
            SELECT period_id, title, start_date, end_date
            FROM evaluation_periods 
            WHERE status = 'Active' 
            ORDER BY start_date DESC 
            LIMIT 1
        """)
        current_period = cursor.fetchone()
        
        if not current_period:
            # No active period, return empty data
            analytics_data = {
                'total_faculty': 0,
                'total_evaluations': 0,
                'average_rating': 0,
                'completion_rate': 0,
                'faculty_rankings': [],
                'category_averages': [],
                'response_trends': [],
                'current_period': None
            }
            cursor.close()
            conn.close()
            return render_template('guidance/faculty-performance.html', analytics_data=analytics_data)
        
        period_id = current_period['period_id']
        
        # Get total faculty count
        cursor.execute("SELECT COUNT(*) as count FROM faculty WHERE is_archived = 0")
        total_faculty = cursor.fetchone()['count'] or 0
        
        # Get total evaluations for current period
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM evaluations e
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE ep.period_id = %s
        """, (period_id,))
        total_evaluations = cursor.fetchone()['count'] or 0
        
        # Get completion rate
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed
            FROM evaluations e
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE ep.period_id = %s
        """, (period_id,))
        completion_stats = cursor.fetchone()
        completion_rate = 0
        if completion_stats and completion_stats['total'] > 0:
            completion_rate = round((completion_stats['completed'] / completion_stats['total']) * 100, 1)
        
        # Get overall average rating
        cursor.execute("""
            SELECT AVG(rating) as avg_rating
            FROM evaluation_responses er
            JOIN evaluations e ON er.evaluation_id = e.evaluation_id
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE ep.period_id = %s AND er.rating IS NOT NULL
        """, (period_id,))
        avg_result = cursor.fetchone()
        average_rating = round(avg_result['avg_rating'] or 0, 2)
        
        # Get faculty rankings
        cursor.execute("""
            SELECT 
                f.faculty_id,
                CONCAT(f.first_name, ' ', f.last_name) as faculty_name,
                p.name as department,
                COUNT(DISTINCT e.evaluation_id) as total_evaluations,
                COUNT(DISTINCT CASE WHEN e.status = 'Completed' THEN e.evaluation_id END) as completed_evaluations,
                AVG(er.rating) as average_rating,
                ROUND((COUNT(DISTINCT CASE WHEN e.status = 'Completed' THEN e.evaluation_id END) / 
                       COUNT(DISTINCT e.evaluation_id)) * 100, 1) as completion_rate
            FROM faculty f
            LEFT JOIN programs p ON f.program_id = p.program_id
            LEFT JOIN class_sections cs ON f.faculty_id = cs.faculty_id
            LEFT JOIN evaluations e ON cs.section_id = e.section_id
            LEFT JOIN evaluation_periods ep ON e.period_id = ep.period_id
            LEFT JOIN evaluation_responses er ON e.evaluation_id = er.evaluation_id
            WHERE f.is_archived = 0 AND (ep.period_id = %s OR ep.period_id IS NULL)
            GROUP BY f.faculty_id, f.first_name, f.last_name, p.name
            ORDER BY average_rating DESC, completion_rate DESC
            LIMIT 20
        """, (period_id,))
        faculty_rankings = cursor.fetchall() or []
        
        # Process faculty rankings to handle None values
        for faculty in faculty_rankings:
            faculty['average_rating'] = round(faculty['average_rating'] or 0, 2)
            faculty['completion_rate'] = faculty['completion_rate'] or 0
            faculty['total_evaluations'] = faculty['total_evaluations'] or 0
            faculty['completed_evaluations'] = faculty['completed_evaluations'] or 0
        
        # Get category averages (if categories exist)
        cursor.execute("""
            SELECT 
                ec.name as category_name,
                AVG(er.rating) as average_rating,
                COUNT(er.response_id) as response_count
            FROM evaluation_categories ec
            LEFT JOIN evaluation_criteria ecr ON ec.category_id = ecr.category_id
            LEFT JOIN evaluation_responses er ON ecr.criteria_id = er.criteria_id
            LEFT JOIN evaluations e ON er.evaluation_id = e.evaluation_id
            LEFT JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE ep.period_id = %s AND er.rating IS NOT NULL
            GROUP BY ec.category_id, ec.name
            ORDER BY average_rating DESC
        """, (period_id,))
        category_averages = cursor.fetchall() or []
        
        # Process category averages
        for category in category_averages:
            category['average_rating'] = round(category['average_rating'] or 0, 2)
            category['response_count'] = category['response_count'] or 0
        
        # Get response trends (last 7 days)
        cursor.execute("""
            SELECT 
                DATE(e.completion_time) as completion_date,
                COUNT(*) as evaluations_completed
            FROM evaluations e
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE ep.period_id = %s 
            AND e.status = 'Completed'
            AND e.completion_time >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            GROUP BY DATE(e.completion_time)
            ORDER BY completion_date DESC
        """, (period_id,))
        response_trends = cursor.fetchall() or []
        
        analytics_data = {
            'total_faculty': total_faculty,
            'total_evaluations': total_evaluations,
            'average_rating': average_rating,
            'completion_rate': completion_rate,
            'faculty_rankings': faculty_rankings,
            'category_averages': category_averages,
            'response_trends': response_trends,
            'current_period': current_period
        }
        
        cursor.close()
        conn.close()
        
        return render_template('guidance/faculty-performance.html', analytics_data=analytics_data)
        
    except Exception as e:
        print(f"Error in faculty_performance: {str(e)}")
        # Return empty data in case of error
        analytics_data = {
            'total_faculty': 0,
            'total_evaluations': 0,
            'average_rating': 0,
            'completion_rate': 0,
            'faculty_rankings': [],
            'category_averages': [],
            'response_trends': [],
            'current_period': None
        }
        return render_template('guidance/faculty-performance.html', analytics_data=analytics_data)


@guidance_bp.route('/rankings')
@guidance_required
def rankings():
    """Faculty and department rankings page"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get all evaluation periods for the dropdown
        cursor.execute("""
            SELECT period_id, title, start_date, end_date, status
            FROM evaluation_periods 
            ORDER BY start_date DESC
        """)
        all_periods = cursor.fetchall() or []
        
        # Get current active period or most recent period
        cursor.execute("""
            SELECT period_id, title, start_date, end_date, status
            FROM evaluation_periods 
            WHERE status = 'Active' 
            ORDER BY start_date DESC 
            LIMIT 1
        """)
        current_period = cursor.fetchone()
        
        if not current_period and all_periods:
            # If no active period, use the most recent one
            current_period = all_periods[0]
        
        selected_period_id = current_period['period_id'] if current_period else None
        
        cursor.close()
        conn.close()
        
        return render_template('guidance/rankings.html',
                             all_periods=all_periods,
                             current_period=current_period,
                             selected_period_id=selected_period_id)
    except Exception as e:
        print(f"Error loading rankings page: {str(e)}")
        return render_template('guidance/rankings.html',
                             all_periods=[],
                             current_period=None,
                             selected_period_id=None)


@guidance_bp.route('/faculty-performance-analytics')
@guidance_required
def faculty_performance_analytics():
    """Faculty performance analytics page"""
    return render_template('guidance/faculty-performance-analytics.html')


@guidance_bp.route('/evaluation-periods')
@guidance_required
def evaluation_periods():
    """Evaluation periods management page"""
    return render_template('guidance/evaluation-periods.html')


@guidance_bp.route('/evaluation-results')
@guidance_required
def evaluation_results():
    """Evaluation results page"""
    return render_template('guidance/evaluation-results.html')


@guidance_bp.route('/evaluation-reports')
@guidance_required
def evaluation_reports():
    """Evaluation reports page"""
    return render_template('guidance/evaluation-reports.html')


@guidance_bp.route('/response-analytics')
@guidance_required
def response_analytics():
    """Response analytics page"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get all periods for the dropdown
        cursor.execute("""
            SELECT period_id, title, start_date, end_date, status
            FROM evaluation_periods 
            ORDER BY start_date DESC
        """)
        all_periods = cursor.fetchall() or []
        
        # Get selected period (from URL parameter or default to active)
        selected_period_id = request.args.get('period_id')
        current_period = None
        
        if selected_period_id:
            cursor.execute("""
                SELECT period_id, title, start_date, end_date, status
                FROM evaluation_periods 
                WHERE period_id = %s
            """, (selected_period_id,))
            current_period = cursor.fetchone()
        else:
            cursor.execute("""
                SELECT period_id, title, start_date, end_date
                FROM evaluation_periods 
                WHERE status = 'Active' 
                ORDER BY start_date DESC 
                LIMIT 1
            """)
            current_period = cursor.fetchone()
            if current_period:
                selected_period_id = current_period['period_id']
        
        if not current_period:
            # No active period, return empty data
            analytics_data = {
                'overall_response_rate': 0,
                'completed_evaluations': 0,
                'in_progress': 0,
                'pending': 0,
                'faculty_stats': [],
                'subject_stats': []
            }
            cursor.close()
            conn.close()
            return render_template('guidance/response-analytics.html', 
                                 analytics_data=analytics_data, 
                                 all_periods=all_periods,
                                 selected_period_id=selected_period_id)
        
        period_id = current_period['period_id']
        
        # Get total responses for current period
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM evaluation_responses er
            JOIN evaluations e ON er.evaluation_id = e.evaluation_id
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE ep.period_id = %s
        """, (period_id,))
        total_responses = cursor.fetchone()['count'] or 0
        
        # Get total possible responses (total evaluations * total criteria)
        cursor.execute("""
            SELECT COUNT(*) * (SELECT COUNT(*) FROM evaluation_criteria) as total_possible
            FROM evaluations e
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE ep.period_id = %s
        """, (period_id,))
        total_possible = cursor.fetchone()['total_possible'] or 1
        response_rate = round((total_responses / total_possible) * 100, 1) if total_possible > 0 else 0
        
        # Get average completion time (in minutes)
        cursor.execute("""
            SELECT AVG(TIMESTAMPDIFF(MINUTE, start_time, completion_time)) as avg_time
            FROM evaluations e
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE ep.period_id = %s 
            AND e.status = 'Completed' 
            AND start_time IS NOT NULL 
            AND completion_time IS NOT NULL
        """, (period_id,))
        avg_time_result = cursor.fetchone()
        average_completion_time = round(avg_time_result['avg_time'] or 0, 1)
        
        # Get peak response hours
        cursor.execute("""
            SELECT 
                HOUR(completion_time) as hour,
                COUNT(*) as response_count
            FROM evaluations e
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE ep.period_id = %s 
            AND e.status = 'Completed'
            AND completion_time IS NOT NULL
            GROUP BY HOUR(completion_time)
            ORDER BY response_count DESC
            LIMIT 5
        """, (period_id,))
        peak_response_hours = cursor.fetchall() or []
        
        # Get daily responses for the last 14 days
        cursor.execute("""
            SELECT 
                DATE(completion_time) as response_date,
                COUNT(*) as response_count
            FROM evaluations e
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE ep.period_id = %s 
            AND e.status = 'Completed'
            AND completion_time >= DATE_SUB(CURDATE(), INTERVAL 14 DAY)
            GROUP BY DATE(completion_time)
            ORDER BY response_date DESC
        """, (period_id,))
        daily_responses = cursor.fetchall() or []
        
        # Get response distribution by rating
        cursor.execute("""
            SELECT 
                rating,
                COUNT(*) as count,
                ROUND((COUNT(*) * 100.0 / %s), 1) as percentage
            FROM evaluation_responses er
            JOIN evaluations e ON er.evaluation_id = e.evaluation_id
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE ep.period_id = %s AND rating IS NOT NULL
            GROUP BY rating
            ORDER BY rating DESC
        """, (total_responses if total_responses > 0 else 1, period_id))
        response_distribution = cursor.fetchall() or []
        
        # Get sentiment analysis from comments (simplified version)
        cursor.execute("""
            SELECT 
                COUNT(*) as total_comments,
                SUM(CASE WHEN sentiment = 'Positive' THEN 1 ELSE 0 END) as positive,
                SUM(CASE WHEN sentiment = 'Neutral' THEN 1 ELSE 0 END) as neutral,
                SUM(CASE WHEN sentiment = 'Negative' THEN 1 ELSE 0 END) as negative
            FROM comments c
            JOIN evaluations e ON c.evaluation_id = e.evaluation_id
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE ep.period_id = %s
        """, (period_id,))
        sentiment_result = cursor.fetchone()
        sentiment_analysis = {
            'positive': sentiment_result['positive'] or 0,
            'neutral': sentiment_result['neutral'] or 0,
            'negative': sentiment_result['negative'] or 0
        } if sentiment_result else {'positive': 0, 'neutral': 0, 'negative': 0}
        
        # Get evaluation status counts
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN e.status = 'Completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN e.status = 'In Progress' THEN 1 ELSE 0 END) as in_progress,
                SUM(CASE WHEN e.status = 'Pending' THEN 1 ELSE 0 END) as pending
            FROM evaluations e
            WHERE e.period_id = %s
        """, (period_id,))
        status_counts = cursor.fetchone() or {}
        
        # Get faculty response statistics
        cursor.execute("""
            SELECT 
                CONCAT(f.first_name, ' ', f.last_name) as faculty_name,
                COUNT(DISTINCT e.evaluation_id) as total_evaluations,
                COUNT(DISTINCT CASE WHEN e.status = 'Completed' THEN e.evaluation_id END) as completed,
                ROUND((COUNT(DISTINCT CASE WHEN e.status = 'Completed' THEN e.evaluation_id END) / 
                       COUNT(DISTINCT e.evaluation_id) * 100), 1) as response_rate
            FROM faculty f
            INNER JOIN class_sections cs ON f.faculty_id = cs.faculty_id
            INNER JOIN evaluations e ON cs.section_id = e.section_id
            WHERE e.period_id = %s
            GROUP BY f.faculty_id, f.first_name, f.last_name
            ORDER BY response_rate DESC
        """, (period_id,))
        faculty_stats = cursor.fetchall() or []
        
        # Get subject response statistics
        cursor.execute("""
            SELECT 
                s.subject_code,
                s.title as subject_title,
                COUNT(DISTINCT e.evaluation_id) as total_evaluations,
                COUNT(DISTINCT CASE WHEN e.status = 'Completed' THEN e.evaluation_id END) as completed,
                ROUND((COUNT(DISTINCT CASE WHEN e.status = 'Completed' THEN e.evaluation_id END) / 
                       COUNT(DISTINCT e.evaluation_id) * 100), 1) as response_rate
            FROM subjects s
            INNER JOIN class_sections cs ON s.subject_id = cs.subject_id
            INNER JOIN evaluations e ON cs.section_id = e.section_id
            WHERE e.period_id = %s
            GROUP BY s.subject_id, s.subject_code, s.title
            ORDER BY response_rate DESC
        """, (period_id,))
        subject_stats = cursor.fetchall() or []
        
        analytics_data = {
            'overall_response_rate': response_rate,
            'completed_evaluations': status_counts.get('completed', 0),
            'in_progress': status_counts.get('in_progress', 0),
            'pending': status_counts.get('pending', 0),
            'faculty_stats': faculty_stats,
            'subject_stats': subject_stats
        }
        
        cursor.close()
        conn.close()
        
        return render_template('guidance/response-analytics.html', 
                             analytics_data=analytics_data,
                             all_periods=all_periods,
                             selected_period_id=selected_period_id)
        
    except Exception as e:
        print(f"Error in response_analytics: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Get periods even if there's an error
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT period_id, title, start_date, end_date, status
                FROM evaluation_periods 
                ORDER BY start_date DESC
            """)
            all_periods = cursor.fetchall() or []
            cursor.close()
            conn.close()
        except:
            all_periods = []
        
        # Return empty data in case of error
        analytics_data = {
            'overall_response_rate': 0,
            'completed_evaluations': 0,
            'in_progress': 0,
            'pending': 0,
            'faculty_stats': [],
            'subject_stats': []
        }
        return render_template('guidance/response-analytics.html', 
                             analytics_data=analytics_data,
                             all_periods=all_periods,
                             selected_period_id=None)


@guidance_bp.route('/ai-analytics')
@guidance_required
def ai_analytics_dashboard():
    """AI Analytics Dashboard with Gemini AI integration"""
    try:
        # Optional: Load any initial data needed for the dashboard
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get basic stats for initialization
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT f.faculty_id) as total_faculty,
                COUNT(DISTINCT p.program_id) as total_departments
            FROM faculty f 
            LEFT JOIN programs p ON f.program_id = p.program_id
            WHERE f.is_archived = 0
        """)
        basic_stats = cursor.fetchone() or {'total_faculty': 0, 'total_departments': 0}
        
        cursor.close()
        conn.close()
        
        return render_template('guidance/ai-analytics-dashboard.html', 
                             basic_stats=basic_stats)
        
    except Exception as e:
        print(f"Error loading AI analytics dashboard: {str(e)}")
        # Return template with empty data on error
        return render_template('guidance/ai-analytics-dashboard.html', 
                             basic_stats={'total_faculty': 0, 'total_departments': 0})


@guidance_bp.route('/questionnaire-builder')
@guidance_required
def questionnaire_builder():
    """Questionnaire builder page"""
    return render_template('guidance/questionnaire-builder.html')


@guidance_bp.route('/questionnaire-management')
@guidance_required
def questionnaire_management():
    """Questionnaire management page"""
    return render_template('guidance/questionnaire-management.html')


@guidance_bp.route('/questionnaire-templates')
@guidance_required
def questionnaire_templates():
    """Questionnaire templates page"""
    return render_template('guidance/questionnaire-templates.html')


@guidance_bp.route('/my-profile')
@guidance_required
def my_profile():
    """Guidance profile page"""
    return render_template('guidance/my-profile.html')


@guidance_bp.route('/settings')
@guidance_required
def settings():
    """Guidance settings page"""
    return render_template('guidance/settings.html')


@guidance_bp.route('/help-support')
@guidance_required
def help_support():
    """Help and support page"""
    return render_template('guidance/help-support.html')


@guidance_bp.route('/evaluation-monitoring')
@guidance_required
def evaluation_monitoring():
    """Evaluation monitoring page - track progress by department and section"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get all evaluation periods
        cursor.execute("""
            SELECT period_id, title, start_date, end_date, status
            FROM evaluation_periods 
            ORDER BY start_date DESC
        """)
        all_periods = cursor.fetchall()
        
        # Get current active period
        cursor.execute("""
            SELECT period_id 
            FROM evaluation_periods 
            WHERE status = 'Active' 
            ORDER BY start_date DESC 
            LIMIT 1
        """)
        current_period = cursor.fetchone()
        selected_period_id = current_period['period_id'] if current_period else None
        
        cursor.close()
        conn.close()
        
        return render_template('guidance/evaluation-monitoring.html', 
                             all_periods=all_periods,
                             selected_period_id=selected_period_id)
    except Exception as e:
        print(f"Error in evaluation_monitoring: {str(e)}")
        return render_template('guidance/evaluation-monitoring.html', 
                             all_periods=[],
                             selected_period_id=None)


@guidance_bp.route('/navigation')
@guidance_required
def navigation():
    """Guidance navigation component"""
    return render_template('guidance/components/navigation.html')


@guidance_bp.route('/header')
@guidance_required
def header():
    """Guidance header component"""
    return render_template('guidance/components/header.html')


# ============================================================================
# TIMER MANAGEMENT API ENDPOINTS
# ============================================================================

@guidance_bp.route('/api/timer-settings', methods=['GET'])
@guidance_required
def get_timer_settings():
    """Get current timer settings"""
    from flask import jsonify
    
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
                'enabled': True,
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


@guidance_bp.route('/api/timer-settings', methods=['POST'])
@guidance_required
def save_timer_settings():
    """Save timer settings"""
    from flask import jsonify
    
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    # Convert enabled to integer (0 or 1) for database
    enabled_value = data.get('enabled', True)
    enabled = 1 if (enabled_value is True or enabled_value == 1 or enabled_value == '1' or enabled_value == 'true') else 0
    
    time_limit = int(data.get('time_limit', 30))
    warning_1 = int(data.get('warning_1', 5))
    warning_2 = int(data.get('warning_2', 1))
    
    print(f"Saving timer settings - Enabled: {enabled} (type: {type(enabled)}), Time Limit: {time_limit}")
    
    # Validate
    if time_limit < 5 or time_limit > 120:
        return jsonify({'success': False, 'error': 'Time limit must be between 5 and 120 minutes'}), 400
    
    if warning_1 > 0 and warning_2 > 0 and warning_2 >= warning_1:
        return jsonify({'success': False, 'error': 'Final warning must be less than first warning'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        
        # Check if settings row exists
        cursor.execute("SELECT COUNT(*) as count FROM timer_settings WHERE setting_id = 1")
        result = cursor.fetchone()
        row_exists = result[0] > 0 if result else False
        
        if row_exists:
            # UPDATE existing row
            cursor.execute("""
                UPDATE timer_settings 
                SET enabled = %s, 
                    time_limit = %s, 
                    warning_1 = %s, 
                    warning_2 = %s,
                    updated_by = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE setting_id = 1
            """, (enabled, time_limit, warning_1, warning_2, session.get('user_id')))
        else:
            # INSERT new row (first time only)
            cursor.execute("""
                INSERT INTO timer_settings (setting_id, enabled, time_limit, warning_1, warning_2, updated_by)
                VALUES (1, %s, %s, %s, %s, %s)
            """, (enabled, time_limit, warning_1, warning_2, session.get('user_id')))
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Timer settings saved successfully',
            'settings': {
                'enabled': enabled,
                'time_limit': time_limit,
                'warning_1': warning_1,
                'warning_2': warning_2
            }
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error saving timer settings: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'Error saving settings: {str(e)}'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@guidance_bp.route('/api/timer-stats', methods=['GET'])
@guidance_required
def get_timer_stats():
    """Get timer statistics"""
    from flask import jsonify
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get active sessions count
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM evaluation_timer_sessions
            WHERE status = 'active'
        """)
        active_result = cursor.fetchone()
        active_sessions = active_result['count'] if active_result else 0
        
        # Get completed today count
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM evaluation_timer_sessions
            WHERE status = 'completed'
            AND DATE(end_time) = CURDATE()
        """)
        completed_result = cursor.fetchone()
        completed_today = completed_result['count'] if completed_result else 0
        
        # Get expired sessions count (today)
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM evaluation_timer_sessions
            WHERE status = 'expired'
            AND DATE(end_time) = CURDATE()
        """)
        expired_result = cursor.fetchone()
        expired_sessions = expired_result['count'] if expired_result else 0
        
        # Get average completion time (in minutes)
        cursor.execute("""
            SELECT AVG(TIMESTAMPDIFF(MINUTE, start_time, end_time)) as avg_time
            FROM evaluation_timer_sessions
            WHERE status = 'completed'
            AND DATE(end_time) >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
        """)
        avg_result = cursor.fetchone()
        avg_time = round(avg_result['avg_time']) if avg_result and avg_result['avg_time'] else 0
        
        return jsonify({
            'success': True,
            'stats': {
                'active_sessions': active_sessions,
                'completed_today': completed_today,
                'expired_sessions': expired_sessions,
                'avg_completion_time': avg_time
            }
        })
        
    except Exception as e:
        print(f"Error loading timer stats: {str(e)}")
        # Return zeros on error
        return jsonify({
            'success': True,
            'stats': {
                'active_sessions': 0,
                'completed_today': 0,
                'expired_sessions': 0,
                'avg_completion_time': 0
            }
        })
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@guidance_bp.route('/api/timer-sessions', methods=['GET'])
@guidance_required
def get_timer_sessions():
    """Get timer session history"""
    from flask import jsonify
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get recent sessions with student names
        cursor.execute("""
            SELECT 
                es.session_id,
                es.user_id as student_id,
                es.evaluation_id,
                es.start_time,
                es.end_time as completed_at,
                es.status,
                es.time_limit_minutes as time_limit,
                TIMESTAMPDIFF(MINUTE, es.start_time, COALESCE(es.end_time, NOW())) as duration_minutes,
                CONCAT(u.first_name, ' ', u.last_name) as student_name
            FROM evaluation_timer_sessions es
            LEFT JOIN users u ON es.user_id = u.user_id
            ORDER BY es.created_at DESC
            LIMIT 50
        """)
        sessions = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'sessions': sessions
        })
        
    except Exception as e:
        print(f"Error loading timer sessions: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Note: Additional guidance routes should be migrated here from app.py


# ============================================================================
# NEW DASHBOARD API ENDPOINTS
# ============================================================================

@guidance_bp.route('/api/dashboard-stats', methods=['GET'])
@guidance_required
def get_dashboard_stats():
    """Get dashboard statistics"""
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get total faculty count (using correct column name)
        cursor.execute("SELECT COUNT(*) as total_faculty FROM faculty WHERE is_archived = 0")
        total_faculty = cursor.fetchone()['total_faculty'] or 0
        
        # Get total departments/programs count
        cursor.execute("SELECT COUNT(*) as total_departments FROM programs")
        total_departments = cursor.fetchone()['total_departments'] or 0
        
        # Get current active period
        cursor.execute("""
            SELECT period_id 
            FROM evaluation_periods 
            WHERE status = 'Active' 
            ORDER BY start_date DESC 
            LIMIT 1
        """)
        current_period = cursor.fetchone()
        period_id = current_period['period_id'] if current_period else None
        
        # Get student evaluation statistics for the current active period
        if period_id:
            # Get total students who should evaluate (students with evaluations assigned for this period)
            cursor.execute("""
                SELECT COUNT(DISTINCT student_id) as total_students
                FROM evaluations
                WHERE period_id = %s
            """, (period_id,))
            total_students_result = cursor.fetchone()
            total_students = total_students_result['total_students'] if total_students_result else 0
            
            # Get students who have completed ALL their evaluations for this period
            cursor.execute("""
                SELECT COUNT(DISTINCT student_id) as completed_students
                FROM evaluations e1
                WHERE period_id = %s
                AND NOT EXISTS (
                    SELECT 1 
                    FROM evaluations e2 
                    WHERE e2.student_id = e1.student_id 
                    AND e2.period_id = %s
                    AND e2.status != 'Completed'
                )
            """, (period_id, period_id))
            completed_result = cursor.fetchone()
            completed_students = completed_result['completed_students'] if completed_result else 0
            
            # Get total evaluations needed vs completed
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_evaluations,
                    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed_evaluations
                FROM evaluations
                WHERE period_id = %s
            """, (period_id,))
            eval_counts = cursor.fetchone()
            total_evaluations = eval_counts['total_evaluations'] if eval_counts else 0
            completed_evaluations = eval_counts['completed_evaluations'] if eval_counts else 0
        else:
            # No active period - use all-time stats
            cursor.execute("SELECT COUNT(DISTINCT student_id) as total_students FROM evaluations")
            total_students_result = cursor.fetchone()
            total_students = total_students_result['total_students'] if total_students_result else 0
            
            cursor.execute("""
                SELECT COUNT(DISTINCT student_id) as completed_students
                FROM evaluations e1
                WHERE NOT EXISTS (
                    SELECT 1 
                    FROM evaluations e2 
                    WHERE e2.student_id = e1.student_id 
                    AND e2.status != 'Completed'
                )
            """)
            completed_result = cursor.fetchone()
            completed_students = completed_result['completed_students'] if completed_result else 0
            
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_evaluations,
                    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed_evaluations
                FROM evaluations
            """)
            eval_counts = cursor.fetchone()
            total_evaluations = eval_counts['total_evaluations'] if eval_counts else 0
            completed_evaluations = eval_counts['completed_evaluations'] if eval_counts else 0
        
        # Calculate student completion rate
        student_completion_rate = round((completed_students / total_students * 100) if total_students > 0 else 0, 1)
        
        # Calculate overall evaluation completion rate
        evaluation_completion_rate = round((completed_evaluations / total_evaluations * 100) if total_evaluations > 0 else 0, 1)
        
        # Get average rating from completed evaluations
        cursor.execute("""
            SELECT AVG(er.rating) as average_rating
            FROM evaluation_responses er
            JOIN evaluations e ON er.evaluation_id = e.evaluation_id
            WHERE e.status = 'Completed'
            {}
        """.format("AND e.period_id = %s" if period_id else ""), (period_id,) if period_id else ())
        avg_result = cursor.fetchone()
        average_rating = float(avg_result['average_rating'] or 0)
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'totalFaculty': total_faculty,
                'totalDepartments': total_departments,
                'totalStudents': total_students,
                'completedStudents': completed_students,
                'studentCompletionRate': student_completion_rate,
                'totalEvaluations': total_evaluations,
                'completedEvaluations': completed_evaluations,
                'evaluationCompletionRate': evaluation_completion_rate,
                'averageRating': round(average_rating, 1),
                'completionRate': student_completion_rate  # For backward compatibility
            }
        })
        
    except Exception as e:
        print(f"Error loading dashboard stats: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@guidance_bp.route('/api/faculty-rankings', methods=['GET'])
@guidance_required
def get_faculty_rankings():
    """Get faculty rankings"""
    
    limit = request.args.get('limit', 10, type=int)
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get faculty rankings with correct column names
        cursor.execute("""
            SELECT 
                f.faculty_id,
                CONCAT(f.first_name, ' ', f.last_name) as name,
                p.name as department,
                f.rank as position,
                AVG(er.rating) as avg_rating,
                COUNT(DISTINCT e.evaluation_id) as evaluation_count
            FROM faculty f
            LEFT JOIN programs p ON f.program_id = p.program_id
            LEFT JOIN class_sections cs ON f.faculty_id = cs.faculty_id
            LEFT JOIN evaluations e ON cs.section_id = e.section_id
            LEFT JOIN evaluation_responses er ON e.evaluation_id = er.evaluation_id
            WHERE f.is_archived = 0 AND e.status = 'Completed'
            GROUP BY f.faculty_id, f.first_name, f.last_name, p.name, f.rank
            HAVING COUNT(DISTINCT e.evaluation_id) > 0
            ORDER BY avg_rating DESC, evaluation_count DESC
            LIMIT %s
        """, (limit,))
        
        rankings = cursor.fetchall() or []
        
        # Process rankings to handle None values
        for faculty in rankings:
            faculty['avg_rating'] = round(faculty['avg_rating'] or 0, 2)
            faculty['evaluation_count'] = faculty['evaluation_count'] or 0
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'rankings': rankings
        })
        
    except Exception as e:
        print(f"Error loading faculty rankings: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@guidance_bp.route('/api/departments-list', methods=['GET'])
@guidance_required
def get_departments_list():
    """Get list of departments"""
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT DISTINCT name FROM programs ORDER BY name")
        departments = [row['name'] for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'departments': departments
        })
        
    except Exception as e:
        print(f"Error loading departments: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@guidance_bp.route('/api/performance-trends', methods=['GET'])
@guidance_required
def get_performance_trends():
    """Get performance trends data for charts"""
    
    period = request.args.get('period', 'all')
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Build query with period filter
        query = """
            SELECT 
                ep.title as period_name,
                AVG(er.rating) as avg_rating,
                COUNT(DISTINCT e.evaluation_id) as evaluation_count
            FROM evaluation_periods ep
            LEFT JOIN evaluations e ON ep.period_id = e.period_id AND e.status = 'Completed'
            LEFT JOIN evaluation_responses er ON e.evaluation_id = er.evaluation_id
        """
        
        params = []
        if period != 'all':
            query += " WHERE ep.period_id = %s"
            params.append(period)
            
        query += """
            GROUP BY ep.period_id, ep.title
            ORDER BY ep.start_date DESC
            LIMIT 6
        """
        
        cursor.execute(query, params)
        trends = cursor.fetchall() or []
        
        # Process data for chart
        labels = []
        ratings = []
        
        for trend in reversed(trends):  # Reverse to show chronological order
            labels.append(trend['period_name'] or 'No Data')
            ratings.append(round(trend['avg_rating'] or 0, 2))
        
        # If no data, provide sample data
        if not labels:
            labels = ['Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5', 'Period 6']
            ratings = [0, 0, 0, 0, 0, 0]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'labels': labels,
                'datasets': [{
                    'label': 'Average Rating',
                    'data': ratings,
                    'borderColor': 'rgb(59, 130, 246)',
                    'backgroundColor': 'rgba(59, 130, 246, 0.1)',
                    'borderWidth': 3,
                    'fill': True,
                    'tension': 0.4
                }]
            }
        })
        
    except Exception as e:
        print(f"Error loading performance trends: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@guidance_bp.route('/api/rating-distribution', methods=['GET'])
@guidance_required
def get_rating_distribution():
    """Get rating distribution data for charts"""
    
    department = request.args.get('department', 'all')
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Build query with department filter
        query = """
            SELECT 
                AVG(er.rating) as avg_rating
            FROM faculty f
            LEFT JOIN programs p ON f.program_id = p.program_id
            JOIN class_sections cs ON f.faculty_id = cs.faculty_id
            JOIN evaluations e ON cs.section_id = e.section_id
            JOIN evaluation_responses er ON e.evaluation_id = er.evaluation_id
            WHERE f.is_archived = 0 AND e.status = 'Completed'
        """
        
        params = []
        if department != 'all':
            query += " AND p.name = %s"
            params.append(department)
            
        query += " GROUP BY f.faculty_id HAVING AVG(er.rating) IS NOT NULL"
        
        cursor.execute(query, params)
        faculty_ratings = cursor.fetchall() or []
        
        # Categorize ratings
        categories = {
            'Outstanding': 0,      # 4.50-5.00
            'Highly Satisfactory': 0,  # 3.50-4.49
            'Satisfactory': 0,     # 2.50-3.49
            'Needs Improvement': 0,     # 1.50-2.49
            'Poor': 0              # 1.00-1.49
        }
        
        for faculty in faculty_ratings:
            rating = faculty['avg_rating'] or 0
            if rating >= 4.50:
                categories['Outstanding'] += 1
            elif rating >= 3.50:
                categories['Highly Satisfactory'] += 1
            elif rating >= 2.50:
                categories['Satisfactory'] += 1
            elif rating >= 1.50:
                categories['Needs Improvement'] += 1
            else:
                categories['Poor'] += 1
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'labels': list(categories.keys()),
                'datasets': [{
                    'data': list(categories.values()),
                    'backgroundColor': [
                        'rgba(34, 197, 94, 0.8)',   # Outstanding - Green
                        'rgba(59, 130, 246, 0.8)',  # Highly Satisfactory - Blue
                        'rgba(251, 191, 36, 0.8)',  # Satisfactory - Yellow
                        'rgba(249, 115, 22, 0.8)',  # Needs Improvement - Orange
                        'rgba(239, 68, 68, 0.8)'    # Poor - Red
                    ],
                    'borderColor': [
                        'rgb(34, 197, 94)',
                        'rgb(59, 130, 246)', 
                        'rgb(251, 191, 36)',
                        'rgb(249, 115, 22)',
                        'rgb(239, 68, 68)'
                    ],
                    'borderWidth': 2
                }]
            }
        })
        
    except Exception as e:
        print(f"Error loading rating distribution: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
