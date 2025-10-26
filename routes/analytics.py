"""
Analytics Routes Blueprint for IntellEvalPro
Handles faculty performance and response analytics endpoints
"""
from flask import Blueprint, render_template, request, session, redirect, url_for, make_response
from utils import admin_required, guidance_required
from models.analytics import FacultyAnalytics, AnalyticsScheduler
from models.database import get_db_connection
from utils.json_encoder import jsonify
import logging

# Create blueprint
analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')
logger = logging.getLogger(__name__)


@analytics_bp.route('/faculty-performance')
@guidance_required
def faculty_performance():
    """Faculty performance analytics dashboard"""
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
        
        # Get all periods for dropdown
        cursor.execute("""
            SELECT period_id, title, start_date, end_date, status
            FROM evaluation_periods 
            ORDER BY start_date DESC
        """)
        all_periods = cursor.fetchall()
        
        # Get period from request or use current
        period_id = request.args.get('period_id', type=int)
        if not period_id and current_period:
            period_id = current_period['period_id']
        
        faculty_analytics = []
        response_analytics = {}
        
        if period_id:
            # Get aggregated faculty performance analytics (combining all subjects)
            cursor.execute("""
                SELECT 
                    f.faculty_id,
                    CONCAT(f.first_name, ' ', f.last_name) as faculty_name,
                    f.email as faculty_email,
                    f.rank as faculty_rank,
                    f.specialization,
                    
                    -- Aggregate subjects taught
                    COUNT(DISTINCT cs.subject_id) as total_subjects,
                    GROUP_CONCAT(DISTINCT s.subject_code ORDER BY s.subject_code SEPARATOR ', ') as subjects_taught,
                    
                    -- Evaluation counts across ALL subjects
                    COUNT(DISTINCT e.evaluation_id) as total_evaluations,
                    COUNT(DISTINCT CASE WHEN e.status = 'Completed' THEN e.evaluation_id END) as completed_evaluations,
                    
                    -- Response rate calculation
                    CASE 
                        WHEN COUNT(DISTINCT e.evaluation_id) > 0 
                        THEN ROUND((COUNT(DISTINCT CASE WHEN e.status = 'Completed' THEN e.evaluation_id END) / 
                              COUNT(DISTINCT e.evaluation_id) * 100), 1)
                        ELSE 0 
                    END as response_rate,
                    
                    -- Average rating across ALL subjects and criteria (with null handling)
                    COALESCE(ROUND(AVG(er.rating), 2), 0) as average_rating,
                    
                    -- Comment counts across ALL subjects
                    COUNT(DISTINCT c.comment_id) as total_comments,
                    COUNT(DISTINCT CASE WHEN c.sentiment = 'Positive' THEN c.comment_id END) as positive_comments,
                    COUNT(DISTINCT CASE WHEN c.sentiment = 'Negative' THEN c.comment_id END) as negative_comments
                    
                FROM faculty f
                INNER JOIN class_sections cs ON f.faculty_id = cs.faculty_id
                INNER JOIN subjects s ON cs.subject_id = s.subject_id
                INNER JOIN evaluations e ON cs.section_id = e.section_id
                LEFT JOIN evaluation_responses er ON e.evaluation_id = er.evaluation_id AND er.rating IS NOT NULL
                LEFT JOIN comments c ON e.evaluation_id = c.evaluation_id
                WHERE e.period_id = %s
                  AND f.is_archived = 0
                GROUP BY f.faculty_id, f.first_name, f.last_name, f.email, f.rank, f.specialization
                ORDER BY COALESCE(AVG(er.rating), 0) DESC, completed_evaluations DESC
            """, (period_id,))
            
            faculty_analytics = cursor.fetchall()
            
            # Calculate overall score and performance grade for each faculty
            for analytics in faculty_analytics:
                # Ensure all numeric fields have default values
                analytics['average_rating'] = analytics.get('average_rating') or 0
                analytics['response_rate'] = analytics.get('response_rate') or 0
                analytics['total_evaluations'] = analytics.get('total_evaluations') or 0
                analytics['completed_evaluations'] = analytics.get('completed_evaluations') or 0
                analytics['positive_comments'] = analytics.get('positive_comments') or 0
                analytics['negative_comments'] = analytics.get('negative_comments') or 0
                analytics['total_comments'] = analytics.get('total_comments') or 0
                
                # Calculate overall score (70% rating + 30% response rate) with safe null handling
                try:
                    # Safely convert to float, defaulting to 0 for None/NULL values
                    rating_score = float(analytics['average_rating'])
                    response_rate = float(analytics['response_rate'])
                    response_score = (response_rate / 100.0) * 5.0
                    
                    analytics['overall_score'] = round((rating_score * 0.7) + (response_score * 0.3), 2)
                except (TypeError, ValueError) as e:
                    logger.warning(f"Error calculating score for faculty {analytics.get('faculty_id')}: {e}")
                    analytics['overall_score'] = 0.0
                
                # Determine performance grade
                score = analytics.get('overall_score', 0)
                if score >= 4.5:
                    analytics['performance_grade'] = 'Excellent'
                elif score >= 4.0:
                    analytics['performance_grade'] = 'Very Good'
                elif score >= 3.5:
                    analytics['performance_grade'] = 'Good'
                elif score >= 3.0:
                    analytics['performance_grade'] = 'Satisfactory'
                else:
                    analytics['performance_grade'] = 'Needs Improvement'
            
            # Get response analytics
            response_analytics = FacultyAnalytics.calculate_response_analytics(period_id)
        
        cursor.close()
        conn.close()
        
        return render_template('guidance/faculty-performance-analytics.html',
                             faculty_analytics=faculty_analytics,
                             response_analytics=response_analytics,
                             current_period=current_period,
                             all_periods=all_periods,
                             selected_period_id=period_id)
                             
    except Exception as e:
        logger.error(f"Error in faculty performance analytics: {str(e)}")
        return render_template('guidance/faculty-performance-analytics.html',
                             faculty_analytics=[],
                             response_analytics={},
                             current_period=None,
                             all_periods=[],
                             selected_period_id=None,
                             error="An error occurred while loading analytics data.")


@analytics_bp.route('/response-analytics')
@guidance_required
def response_analytics():
    """Response rate analytics dashboard"""
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
        
        # Get all periods for dropdown
        cursor.execute("""
            SELECT period_id, title, start_date, end_date, status
            FROM evaluation_periods 
            ORDER BY start_date DESC
        """)
        all_periods = cursor.fetchall()
        
        # Get period from request or use current
        period_id = request.args.get('period_id', type=int)
        if not period_id and current_period:
            period_id = current_period['period_id']
        
        analytics_data = {}
        if period_id:
            analytics_data = FacultyAnalytics.calculate_response_analytics(period_id)
        
        cursor.close()
        conn.close()
        
        return render_template('guidance/response-analytics.html',
                             analytics_data=analytics_data,
                             current_period=current_period,
                             all_periods=all_periods,
                             selected_period_id=period_id)
                             
    except Exception as e:
        logger.error(f"Error in response analytics: {str(e)}")
        return render_template('guidance/response-analytics.html',
                             analytics_data={},
                             current_period=None,
                             all_periods=[],
                             selected_period_id=None,
                             error="An error occurred while loading response analytics.")


@analytics_bp.route('/faculty/<int:faculty_id>/details')
@guidance_required
def faculty_details(faculty_id):
    """Detailed analytics for a specific faculty member"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get faculty information
        cursor.execute("""
            SELECT faculty_id, first_name, last_name, email, department
            FROM faculty 
            WHERE faculty_id = %s
        """, (faculty_id,))
        faculty = cursor.fetchone()
        
        if not faculty:
            return redirect(url_for('analytics.faculty_performance'))
        
        # Get period from request
        period_id = request.args.get('period_id', type=int)
        
        # Get current active period if none specified
        if not period_id:
            cursor.execute("""
                SELECT period_id 
                FROM evaluation_periods 
                WHERE status = 'Active' 
                ORDER BY start_date DESC 
                LIMIT 1
            """)
            period_result = cursor.fetchone()
            if period_result:
                period_id = period_result['period_id']
        
        # Calculate detailed analytics
        performance_data = {}
        category_performance = []
        trends_data = {}
        
        if period_id:
            performance_data = FacultyAnalytics.calculate_faculty_performance(faculty_id, period_id)
            
            # Get category performance details
            cursor.execute("""
                SELECT 
                    cpa.*,
                    ec.name as category_name,
                    ec.description as category_description
                FROM category_performance_analytics cpa
                JOIN evaluation_categories ec ON cpa.category_id = ec.category_id
                JOIN faculty_performance_analytics fpa ON cpa.analytics_id = fpa.analytics_id
                WHERE fpa.faculty_id = %s AND fpa.period_id = %s
                ORDER BY cpa.average_score DESC
            """, (faculty_id, period_id))
            
            category_performance = cursor.fetchall()
            
            # Get performance trends
            trends_data = FacultyAnalytics.get_performance_trends(faculty_id)
        
        # Get all periods for comparison
        cursor.execute("""
            SELECT period_id, title, start_date, end_date, status
            FROM evaluation_periods 
            ORDER BY start_date DESC
        """)
        all_periods = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('guidance/faculty-details-analytics.html',
                             faculty=faculty,
                             performance_data=performance_data,
                             category_performance=category_performance,
                             trends_data=trends_data,
                             all_periods=all_periods,
                             selected_period_id=period_id)
                             
    except Exception as e:
        logger.error(f"Error in faculty details analytics: {str(e)}")
        return redirect(url_for('analytics.faculty_performance'))


@analytics_bp.route('/api/calculate-analytics', methods=['POST'])
@admin_required
def calculate_analytics():
    """API endpoint to trigger analytics calculation"""
    try:
        data = request.get_json() or {}
        period_id = data.get('period_id')
        faculty_id = data.get('faculty_id')
        
        if not period_id:
            return jsonify({
                'success': False,
                'message': 'Period ID is required'
            }), 400
        
        if faculty_id:
            # Calculate for specific faculty
            analytics = FacultyAnalytics.calculate_faculty_performance(faculty_id, period_id)
            if analytics and FacultyAnalytics.save_analytics_to_db(analytics):
                return jsonify({
                    'success': True,
                    'message': 'Analytics calculated successfully for faculty member'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Failed to calculate analytics for faculty member'
                }), 500
        else:
            # Calculate for all faculty in period
            success = AnalyticsScheduler.calculate_all_faculty_analytics(period_id)
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Analytics calculated successfully for all faculty'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Failed to calculate analytics for some faculty members'
                }), 500
                
    except Exception as e:
        logger.error(f"Error in calculate analytics API: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while calculating analytics'
        }), 500


@analytics_bp.route('/api/faculty/<int:faculty_id>/performance')
@guidance_required
def api_faculty_performance(faculty_id):
    """API endpoint to get faculty performance data"""
    try:
        period_id = request.args.get('period_id', type=int)
        subject_id = request.args.get('subject_id', type=int)
        
        if not period_id:
            return jsonify({
                'success': False,
                'message': 'Period ID is required'
            }), 400
        
        performance_data = FacultyAnalytics.calculate_faculty_performance(faculty_id, period_id, subject_id)
        
        if performance_data:
            return jsonify({
                'success': True,
                'data': performance_data
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No performance data found'
            }), 404
            
    except Exception as e:
        logger.error(f"Error in faculty performance API: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching performance data'
        }), 500


@analytics_bp.route('/api/response-analytics/<int:period_id>')
@guidance_required
def api_response_analytics(period_id):
    """API endpoint to get response analytics data"""
    try:
        analytics_data = FacultyAnalytics.calculate_response_analytics(period_id)
        
        if analytics_data:
            return jsonify({
                'success': True,
                'data': analytics_data
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No response analytics data found'
            }), 404
            
    except Exception as e:
        logger.error(f"Error in response analytics API: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching response analytics'
        }), 500


@analytics_bp.route('/export/faculty-performance')
@guidance_required
def export_faculty_performance():
    """Export faculty performance analytics to CSV"""
    try:
        import csv
        from io import StringIO
        from flask import Response
        
        period_id = request.args.get('period_id', type=int)
        if not period_id:
            return jsonify({
                'success': False,
                'message': 'Period ID is required'
            }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get faculty performance data
        cursor.execute("""
            SELECT 
                CONCAT(f.first_name, ' ', f.last_name) as faculty_name,
                f.email as faculty_email,
                COALESCE(s.subject_code, 'Overall') as subject_code,
                COALESCE(s.title, 'All Subjects') as subject_title,
                fpa.total_evaluations,
                fpa.completed_evaluations,
                fpa.response_rate,
                fpa.average_rating,
                fpa.overall_score,
                fpa.performance_grade,
                fpa.total_comments,
                fpa.positive_comments,
                fpa.negative_comments,
                fpa.strengths_summary,
                fpa.improvement_areas,
                fpa.last_calculated
            FROM faculty_performance_analytics fpa
            JOIN faculty f ON fpa.faculty_id = f.faculty_id
            LEFT JOIN subjects s ON fpa.subject_id = s.subject_id
            WHERE fpa.period_id = %s
            ORDER BY fpa.overall_score DESC, f.last_name ASC
        """, (period_id,))
        
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data found for export'
            }), 404
        
        # Create CSV
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        
        # Create response
        csv_data = output.getvalue()
        output.close()
        
        response = Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=faculty_performance_period_{period_id}.csv'}
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error exporting faculty performance: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while exporting data'
        }), 500

@analytics_bp.route('/rankings')
@guidance_required
def rankings():
    """Display rankings page"""
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
        
        # Get all periods for dropdown
        cursor.execute("""
            SELECT period_id, title, start_date, end_date, status
            FROM evaluation_periods 
            ORDER BY start_date DESC
        """)
        all_periods = cursor.fetchall()
        
        # Get period from request or use current
        period_id = request.args.get('period_id', type=int)
        if not period_id and current_period:
            period_id = current_period['period_id']
        
        cursor.close()
        conn.close()
        
        return render_template('guidance/rankings.html',
                             current_period=current_period,
                             all_periods=all_periods,
                             selected_period_id=period_id)
                             
    except Exception as e:
        logger.error(f"Error loading rankings page: {str(e)}")
        return render_template('guidance/rankings.html',
                             current_period=None,
                             all_periods=[],
                             selected_period_id=None)

@analytics_bp.route('/get-rankings-data', methods=['GET'])
@guidance_required
def get_rankings_data():
    """Get rankings data for faculty or department"""
    try:
        ranking_type = request.args.get('view_type', 'faculty')
        period_id = request.args.get('period_id')
        
        if not period_id:
            return jsonify({
                'success': False,
                'message': 'Period ID is required'
            }), 400
        
        if ranking_type == 'faculty':
            rankings_data = get_faculty_rankings(period_id)
        else:
            rankings_data = get_department_rankings(period_id)
        
        return jsonify({
            'success': True,
            'data': rankings_data
        })
        
    except Exception as e:
        logger.error(f"Error getting rankings data: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while loading rankings data'
        }), 500

@analytics_bp.route('/export-rankings')
def export_rankings():
    """Export rankings data as CSV"""
    try:
        ranking_type = request.args.get('type', 'faculty')
        period_id = request.args.get('period_id')
        
        if not period_id:
            return jsonify({
                'success': False,
                'message': 'Period ID is required'
            }), 400
        
        if ranking_type == 'faculty':
            data = get_faculty_rankings(period_id)
            filename = f'faculty_rankings_period_{period_id}.csv'
        else:
            data = get_department_rankings(period_id)
            filename = f'department_rankings_period_{period_id}.csv'
        
        # Create CSV content
        csv_data = []
        if ranking_type == 'faculty':
            csv_data.append('Rank,Faculty Name,Department,Overall Score,Teaching,Communication,Professionalism,Total Evaluations')
            for i, faculty in enumerate(data, 1):
                csv_data.append(f"{i},{faculty['name']},{faculty['department']},{faculty['overall_score']:.2f},{faculty['teaching_score']:.2f},{faculty['communication_score']:.2f},{faculty['professionalism_score']:.2f},{faculty['total_evaluations']}")
        else:
            csv_data.append('Rank,Department,Average Score,Total Faculty,Total Evaluations,Performance Level')
            for i, dept in enumerate(data, 1):
                csv_data.append(f"{i},{dept['department']},{dept['average_score']:.2f},{dept['total_faculty']},{dept['total_evaluations']},{dept['performance_level']}")
        
        csv_content = '\n'.join(csv_data)
        
        response = make_response(csv_content)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        
        return response
        
    except Exception as e:
        logger.error(f"Error exporting rankings: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while exporting rankings'
        }), 500

def get_faculty_rankings(period_id):
    """Get faculty rankings with detailed metrics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            f.faculty_id,
            CONCAT(f.first_name, ' ', f.last_name) as name,
            f.program_id,
            p.name as department,
            COUNT(DISTINCT e.evaluation_id) as total_evaluations,
            AVG(er.rating) as overall_score,
            AVG(er.rating) as teaching_score,
            AVG(er.rating) as communication_score,
            AVG(er.rating) as professionalism_score
        FROM faculty f
        LEFT JOIN programs p ON f.program_id = p.program_id
        LEFT JOIN class_sections cs ON f.faculty_id = cs.faculty_id
        LEFT JOIN evaluations e ON cs.section_id = e.section_id 
            AND e.period_id = %s
            AND e.status = 'Completed'
        LEFT JOIN evaluation_responses er ON e.evaluation_id = er.evaluation_id
        GROUP BY f.faculty_id, f.first_name, f.last_name, f.program_id, p.name
        HAVING total_evaluations > 0
        ORDER BY overall_score DESC, total_evaluations DESC
        """
        
        cursor.execute(query, (period_id,))
        results = cursor.fetchall()
        
        # Add ranking and performance level
        for i, faculty in enumerate(results):
            faculty['rank'] = i + 1
            faculty['medal_type'] = get_medal_type(i + 1)
            faculty['performance_level'] = get_performance_level(faculty['overall_score'])
            
            # Round scores to 2 decimal places and convert to float
            faculty['overall_score'] = round(float(faculty['overall_score']) if faculty['overall_score'] else 0, 2)
            faculty['teaching_score'] = round(float(faculty['teaching_score']) if faculty['teaching_score'] else 0, 2)
            faculty['communication_score'] = round(float(faculty['communication_score']) if faculty['communication_score'] else 0, 2)
            faculty['professionalism_score'] = round(float(faculty['professionalism_score']) if faculty['professionalism_score'] else 0, 2)
        
        cursor.close()
        conn.close()
        
        return results
        
    except Exception as e:
        logger.error(f"Error getting faculty rankings: {str(e)}")
        return []

def get_department_rankings(period_id):
    """Get department rankings with aggregated metrics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            p.name as department,
            COUNT(DISTINCT f.faculty_id) as total_faculty,
            COUNT(DISTINCT e.evaluation_id) as total_evaluations,
            AVG(er.rating) as average_score
        FROM programs p
        LEFT JOIN faculty f ON p.program_id = f.program_id
        LEFT JOIN class_sections cs ON f.faculty_id = cs.faculty_id
        LEFT JOIN evaluations e ON cs.section_id = e.section_id 
            AND e.period_id = %s
            AND e.status = 'Completed'
        LEFT JOIN evaluation_responses er ON e.evaluation_id = er.evaluation_id
        GROUP BY p.program_id, p.name
        HAVING total_evaluations > 0
        ORDER BY average_score DESC, total_evaluations DESC
        """
        
        cursor.execute(query, (period_id,))
        results = cursor.fetchall()
        
        # Add ranking and performance level
        for i, dept in enumerate(results):
            dept['rank'] = i + 1
            dept['medal_type'] = get_medal_type(i + 1)
            dept['performance_level'] = get_performance_level(dept['average_score'])
            
            # Round score to 2 decimal places and convert to float
            dept['average_score'] = round(float(dept['average_score']) if dept['average_score'] else 0, 2)
        
        cursor.close()
        conn.close()
        
        return results
        
    except Exception as e:
        logger.error(f"Error getting department rankings: {str(e)}")
        return []

def get_medal_type(rank):
    """Get medal type based on rank"""
    if rank == 1:
        return 'gold'
    elif rank == 2:
        return 'silver'
    elif rank == 3:
        return 'bronze'
    else:
        return 'none'

def get_performance_level(score):
    """Get performance level based on score"""
    if score >= 4.5:
        return 'Excellent'
    elif score >= 4.0:
        return 'Very Good'
    elif score >= 3.5:
        return 'Good'
    elif score >= 3.0:
        return 'Satisfactory'
    else:
        return 'Needs Improvement'