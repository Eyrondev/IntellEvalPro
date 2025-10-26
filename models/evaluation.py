"""
Evaluation model for IntellEvalPro
Handles evaluation-specific data and operations
"""
from .database import get_db_connection


class Evaluation:
    """Evaluation model for managing evaluations"""
    
    @staticmethod
    def get_by_id(evaluation_id):
        """
        Get evaluation by ID
        
        Args:
            evaluation_id (int): Evaluation ID
            
        Returns:
            dict: Evaluation data or None if not found
        """
        conn = get_db_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT e.*, 
                       ep.title as period_title,
                       s.std_Firstname, s.std_Surname,
                       f.first_name as faculty_first_name,
                       f.last_name as faculty_last_name,
                       c.title as course_title
                FROM evaluations e
                LEFT JOIN evaluation_periods ep ON e.period_id = ep.period_id
                LEFT JOIN std_info s ON e.student_id = s.id
                LEFT JOIN class_sections cs ON e.section_id = cs.section_id
                LEFT JOIN faculty f ON cs.faculty_id = f.faculty_id
                LEFT JOIN courses c ON cs.course_id = c.course_id
                WHERE e.evaluation_id = %s
            """
            cursor.execute(query, (evaluation_id,))
            evaluation = cursor.fetchone()
            cursor.close()
            return evaluation
        except Exception as e:
            print(f"Error getting evaluation: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_student_evaluations(student_id, status=None):
        """
        Get evaluations for a specific student
        
        Args:
            student_id (int): Student ID
            status (str): Filter by status (optional)
            
        Returns:
            list: List of evaluation dictionaries
        """
        conn = get_db_connection()
        if not conn:
            return []
            
        try:
            cursor = conn.cursor(dictionary=True)
            
            if status:
                query = """
                    SELECT e.*, 
                           ep.title as period_title,
                           f.first_name as faculty_first_name,
                           f.last_name as faculty_last_name,
                           c.title as course_title,
                           cs.section_name
                    FROM evaluations e
                    LEFT JOIN evaluation_periods ep ON e.period_id = ep.period_id
                    LEFT JOIN class_sections cs ON e.section_id = cs.section_id
                    LEFT JOIN faculty f ON cs.faculty_id = f.faculty_id
                    LEFT JOIN courses c ON cs.course_id = c.course_id
                    WHERE e.student_id = %s AND e.status = %s
                    ORDER BY e.created_at DESC
                """
                cursor.execute(query, (student_id, status))
            else:
                query = """
                    SELECT e.*, 
                           ep.title as period_title,
                           f.first_name as faculty_first_name,
                           f.last_name as faculty_last_name,
                           c.title as course_title,
                           cs.section_name
                    FROM evaluations e
                    LEFT JOIN evaluation_periods ep ON e.period_id = ep.period_id
                    LEFT JOIN class_sections cs ON e.section_id = cs.section_id
                    LEFT JOIN faculty f ON cs.faculty_id = f.faculty_id
                    LEFT JOIN courses c ON cs.course_id = c.course_id
                    WHERE e.student_id = %s
                    ORDER BY e.created_at DESC
                """
                cursor.execute(query, (student_id,))
            
            evaluations = cursor.fetchall()
            cursor.close()
            return evaluations
        except Exception as e:
            print(f"Error getting student evaluations: {e}")
            return []
        finally:
            conn.close()
