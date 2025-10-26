"""
Student model for IntellEvalPro
Handles student-specific data and operations
"""
from .database import get_db_connection


class Student:
    """Student model for managing student information"""
    
    @staticmethod
    def get_by_user_id(user_id):
        """
        Get student information by user ID
        
        Args:
            user_id (int): User ID
            
        Returns:
            dict: Student data or None if not found
        """
        conn = get_db_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM std_info WHERE user_id = %s", (user_id,))
            student = cursor.fetchone()
            cursor.close()
            return student
        except Exception as e:
            print(f"Error getting student: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(student_id):
        """
        Get student information by student ID
        
        Args:
            student_id (int): Student ID
            
        Returns:
            dict: Student data or None if not found
        """
        conn = get_db_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM std_info WHERE id = %s", (student_id,))
            student = cursor.fetchone()
            cursor.close()
            return student
        except Exception as e:
            print(f"Error getting student: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_all():
        """
        Get all students with their user information
        
        Returns:
            list: List of student dictionaries
        """
        conn = get_db_connection()
        if not conn:
            return []
            
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT s.*, u.username, u.email, u.is_active
                FROM std_info s
                JOIN users u ON s.user_id = u.user_id
                ORDER BY s.std_Surname, s.std_Firstname
            """
            cursor.execute(query)
            students = cursor.fetchall()
            cursor.close()
            return students
        except Exception as e:
            print(f"Error getting students: {e}")
            return []
        finally:
            conn.close()
    
    @staticmethod
    def get_pending_evaluation_count(user_id):
        """
        Get count of pending evaluations for a student
        
        Args:
            user_id (int): User ID of the student
            
        Returns:
            int: Count of pending evaluations
        """
        conn = get_db_connection()
        if not conn:
            return 0
            
        try:
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT COUNT(*) as pending_count
                FROM evaluations e
                JOIN std_info s ON e.student_id = s.id
                WHERE s.user_id = %s 
                AND e.status IN ('Pending', 'In Progress')
                AND EXISTS (
                    SELECT 1 FROM evaluation_periods ep 
                    WHERE ep.period_id = e.period_id 
                    AND ep.status = 'Active'
                )
            """
            
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            pending_count = result['pending_count'] if result else 0
            
            cursor.close()
            return pending_count
        except Exception as e:
            print(f"Error getting pending count: {e}")
            return 0
        finally:
            conn.close()
