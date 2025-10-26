"""
Expired Evaluations Management
Handles automatic marking of evaluations as expired when time limits are exceeded
"""

from datetime import datetime, timedelta
from models.database import get_db_connection


def mark_expired_evaluations():
    """
    Mark evaluations as Expired if:
    1. Timer is enabled and time limit has been exceeded
    2. Evaluation period has ended and evaluation is still incomplete
    
    Returns:
        dict: Summary of expired evaluations marked
    """
    conn = get_db_connection()
    if not conn:
        return {'success': False, 'error': 'Database connection failed'}
    
    try:
        cursor = conn.cursor(dictionary=True)
        expired_count = 0
        
        # Get timer settings
        cursor.execute("SELECT enabled, time_limit FROM evaluation_timer_settings LIMIT 1")
        timer_settings = cursor.fetchone()
        
        if timer_settings and timer_settings['enabled']:
            time_limit = timer_settings['time_limit']
            
            # Mark evaluations as Expired if timer exceeded
            query_timer_expired = """
                UPDATE evaluations e
                LEFT JOIN evaluation_timer_sessions ets ON e.evaluation_id = ets.evaluation_id
                SET e.status = 'Expired'
                WHERE e.status IN ('Pending', 'In Progress')
                  AND e.start_time IS NOT NULL
                  AND e.completion_time IS NULL
                  AND TIMESTAMPDIFF(MINUTE, e.start_time, NOW()) > %s
            """
            cursor.execute(query_timer_expired, (time_limit,))
            timer_expired = cursor.rowcount
            expired_count += timer_expired
            
        # Mark evaluations as Expired if evaluation period has ended
        query_period_expired = """
            UPDATE evaluations e
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            SET e.status = 'Expired'
            WHERE e.status IN ('Pending', 'In Progress')
              AND ep.end_date < CURDATE()
              AND e.completion_time IS NULL
              AND e.status != 'Expired'
        """
        cursor.execute(query_period_expired)
        period_expired = cursor.rowcount
        expired_count += period_expired
        
        conn.commit()
        
        # Get detailed breakdown
        cursor.execute("""
            SELECT 
                ep.title as period_title,
                COUNT(*) as count
            FROM evaluations e
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE e.status = 'Expired'
            GROUP BY ep.title
            ORDER BY count DESC
        """)
        breakdown = cursor.fetchall()
        
        cursor.close()
        
        return {
            'success': True,
            'expired_count': expired_count,
            'timer_expired': timer_expired if timer_settings and timer_settings['enabled'] else 0,
            'period_expired': period_expired,
            'breakdown': breakdown,
            'message': f'Marked {expired_count} evaluation(s) as expired'
        }
        
    except Exception as e:
        print(f"Error marking expired evaluations: {e}")
        conn.rollback()
        return {'success': False, 'error': str(e)}
    finally:
        conn.close()


def get_expired_evaluations(period_id=None, student_id=None):
    """
    Get list of expired evaluations with details
    
    Args:
        period_id (int, optional): Filter by evaluation period
        student_id (int, optional): Filter by student
    
    Returns:
        dict: List of expired evaluations
    """
    conn = get_db_connection()
    if not conn:
        return {'success': False, 'error': 'Database connection failed'}
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        where_conditions = ["e.status = 'Expired'"]
        params = []
        
        if period_id:
            where_conditions.append("e.period_id = %s")
            params.append(period_id)
        
        if student_id:
            where_conditions.append("e.student_id = %s")
            params.append(student_id)
        
        where_clause = " AND ".join(where_conditions)
        
        query = f"""
            SELECT 
                e.evaluation_id,
                e.period_id,
                e.section_id,
                e.student_id,
                e.status,
                e.start_time,
                e.completion_time,
                CONCAT(s.std_Firstname, ' ', s.std_Surname) as student_name,
                s.std_Number as student_number,
                CONCAT(f.first_name, ' ', f.last_name) as faculty_name,
                sub.subject_code,
                sub.title as subject_title,
                cs.section_name,
                cs.schedule,
                cs.room,
                ep.title as period_title,
                ep.start_date as period_start,
                ep.end_date as period_end,
                TIMESTAMPDIFF(MINUTE, e.start_time, NOW()) as minutes_since_start,
                ts.time_limit
            FROM evaluations e
            LEFT JOIN std_info s ON e.student_id = s.id
            LEFT JOIN class_sections cs ON e.section_id = cs.section_id
            LEFT JOIN faculty f ON cs.faculty_id = f.faculty_id
            LEFT JOIN subjects sub ON cs.subject_id = sub.subject_id
            LEFT JOIN evaluation_periods ep ON e.period_id = ep.period_id
            LEFT JOIN evaluation_timer_settings ts ON 1=1
            WHERE {where_clause}
            ORDER BY e.start_time DESC
        """
        
        cursor.execute(query, params)
        evaluations = cursor.fetchall()
        
        cursor.close()
        
        return {
            'success': True,
            'data': evaluations,
            'count': len(evaluations)
        }
        
    except Exception as e:
        print(f"Error getting expired evaluations: {e}")
        return {'success': False, 'error': str(e)}
    finally:
        conn.close()


def reset_expired_evaluation(evaluation_id):
    """
    Reset an expired evaluation back to Pending status
    This allows the student to retake the evaluation
    
    Args:
        evaluation_id (int): The evaluation ID to reset
    
    Returns:
        dict: Success status and message
    """
    conn = get_db_connection()
    if not conn:
        return {'success': False, 'error': 'Database connection failed'}
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Check if evaluation exists and is expired
        cursor.execute("""
            SELECT evaluation_id, status, start_time
            FROM evaluations
            WHERE evaluation_id = %s AND status = 'Expired'
        """, (evaluation_id,))
        
        evaluation = cursor.fetchone()
        
        if not evaluation:
            return {
                'success': False,
                'error': 'Evaluation not found or not in Expired status'
            }
        
        # Reset evaluation to Pending and clear start_time
        cursor.execute("""
            UPDATE evaluations
            SET status = 'Pending',
                start_time = NULL,
                updated_at = NOW()
            WHERE evaluation_id = %s
        """, (evaluation_id,))
        
        # Delete any timer session data
        cursor.execute("""
            DELETE FROM evaluation_timer_sessions
            WHERE evaluation_id = %s
        """, (evaluation_id,))
        
        # Delete any partial responses if they exist
        cursor.execute("""
            DELETE FROM evaluation_responses
            WHERE evaluation_id = %s
        """, (evaluation_id,))
        
        conn.commit()
        cursor.close()
        
        return {
            'success': True,
            'message': 'Evaluation reset successfully. Student can now retake the evaluation.'
        }
        
    except Exception as e:
        print(f"Error resetting expired evaluation: {e}")
        conn.rollback()
        return {'success': False, 'error': str(e)}
    finally:
        conn.close()


def reset_multiple_expired_evaluations(evaluation_ids):
    """
    Reset multiple expired evaluations at once
    
    Args:
        evaluation_ids (list): List of evaluation IDs to reset
    
    Returns:
        dict: Summary of reset operations
    """
    conn = get_db_connection()
    if not conn:
        return {'success': False, 'error': 'Database connection failed'}
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        success_count = 0
        failed_count = 0
        errors = []
        
        for eval_id in evaluation_ids:
            try:
                # Check if evaluation is expired
                cursor.execute("""
                    SELECT evaluation_id FROM evaluations
                    WHERE evaluation_id = %s AND status = 'Expired'
                """, (eval_id,))
                
                if cursor.fetchone():
                    # Reset evaluation
                    cursor.execute("""
                        UPDATE evaluations
                        SET status = 'Pending',
                            start_time = NULL,
                            updated_at = NOW()
                        WHERE evaluation_id = %s
                    """, (eval_id,))
                    
                    # Delete timer sessions
                    cursor.execute("""
                        DELETE FROM evaluation_timer_sessions
                        WHERE evaluation_id = %s
                    """, (eval_id,))
                    
                    # Delete partial responses
                    cursor.execute("""
                        DELETE FROM evaluation_responses
                        WHERE evaluation_id = %s
                    """, (eval_id,))
                    
                    success_count += 1
                else:
                    failed_count += 1
                    errors.append(f"Evaluation {eval_id} not found or not expired")
                    
            except Exception as e:
                failed_count += 1
                errors.append(f"Evaluation {eval_id}: {str(e)}")
        
        conn.commit()
        cursor.close()
        
        return {
            'success': True,
            'success_count': success_count,
            'failed_count': failed_count,
            'errors': errors if errors else None,
            'message': f'Successfully reset {success_count} evaluation(s). {failed_count} failed.'
        }
        
    except Exception as e:
        print(f"Error resetting multiple expired evaluations: {e}")
        conn.rollback()
        return {'success': False, 'error': str(e)}
    finally:
        conn.close()


def get_expired_evaluations_summary(period_id=None):
    """
    Get summary statistics of expired evaluations
    
    Args:
        period_id (int, optional): Filter by evaluation period
    
    Returns:
        dict: Summary statistics
    """
    conn = get_db_connection()
    if not conn:
        return {'success': False, 'error': 'Database connection failed'}
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        where_clause = "WHERE e.status = 'Expired'"
        params = []
        
        if period_id:
            where_clause += " AND e.period_id = %s"
            params.append(period_id)
        
        query = f"""
            SELECT 
                COUNT(DISTINCT e.evaluation_id) as total_expired,
                COUNT(DISTINCT e.student_id) as affected_students,
                COUNT(DISTINCT e.section_id) as affected_sections,
                COUNT(DISTINCT CASE WHEN e.start_time IS NOT NULL THEN e.evaluation_id END) as expired_in_progress,
                COUNT(DISTINCT CASE WHEN e.start_time IS NULL THEN e.evaluation_id END) as expired_never_started
            FROM evaluations e
            {where_clause}
        """
        
        cursor.execute(query, params)
        summary = cursor.fetchone()
        
        # Get breakdown by period
        period_query = """
            SELECT 
                ep.title as period_title,
                ep.period_id,
                COUNT(*) as expired_count,
                ep.start_date,
                ep.end_date
            FROM evaluations e
            JOIN evaluation_periods ep ON e.period_id = ep.period_id
            WHERE e.status = 'Expired'
        """
        
        if period_id:
            period_query += " AND e.period_id = %s"
        
        period_query += " GROUP BY ep.period_id ORDER BY expired_count DESC"
        
        cursor.execute(period_query, params if period_id else [])
        period_breakdown = cursor.fetchall()
        
        cursor.close()
        
        return {
            'success': True,
            'summary': summary,
            'period_breakdown': period_breakdown
        }
        
    except Exception as e:
        print(f"Error getting expired evaluations summary: {e}")
        return {'success': False, 'error': str(e)}
    finally:
        conn.close()
