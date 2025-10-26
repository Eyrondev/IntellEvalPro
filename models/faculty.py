"""
Faculty model for IntellEvalPro
Handles faculty-specific data and operations
"""
from .database import get_db_connection


class Faculty:
    """Faculty model for managing faculty information"""
    
    @staticmethod
    def get_by_id(faculty_id):
        """
        Get faculty information by ID
        
        Args:
            faculty_id (int): Faculty ID
            
        Returns:
            dict: Faculty data or None if not found
        """
        conn = get_db_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT f.*, d.name as department_name, c.name as college_name
                FROM faculty f
                LEFT JOIN departments d ON f.department_id = d.department_id
                LEFT JOIN colleges c ON d.college_id = c.college_id
                WHERE f.faculty_id = %s
            """
            cursor.execute(query, (faculty_id,))
            faculty = cursor.fetchone()
            cursor.close()
            return faculty
        except Exception as e:
            print(f"Error getting faculty: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_all():
        """
        Get all faculty members with department and college information
        
        Returns:
            list: List of faculty dictionaries
        """
        conn = get_db_connection()
        if not conn:
            return []
            
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT f.*, 
                       d.name as department_name,
                       c.name as college_name
                FROM faculty f
                LEFT JOIN departments d ON f.department_id = d.department_id
                LEFT JOIN colleges c ON d.college_id = c.college_id
                ORDER BY f.last_name, f.first_name
            """
            cursor.execute(query)
            faculty = cursor.fetchall()
            cursor.close()
            return faculty
        except Exception as e:
            print(f"Error getting faculty: {e}")
            return []
        finally:
            conn.close()
