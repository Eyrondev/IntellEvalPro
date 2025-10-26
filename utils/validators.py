"""
Validation utilities for IntellEvalPro
Provides input validation functions
"""
import re
from datetime import datetime


def validate_email(email):
    """
    Validate email format
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_username(username):
    """
    Validate username format
    Username must be 3-50 characters, alphanumeric with optional dashes/underscores
    
    Args:
        username (str): Username to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not username or len(username) < 3 or len(username) > 50:
        return False
    pattern = r'^[a-zA-Z0-9_-]+$'
    return re.match(pattern, username) is not None


def validate_password(password):
    """
    Validate password strength
    Password must be at least 5 characters
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 5:
        return False, "Password must be at least 5 characters long"
    
    # Add more strength requirements if needed
    # if not re.search(r'[A-Z]', password):
    #     return False, "Password must contain at least one uppercase letter"
    
    return True, ""


def validate_student_number(student_number):
    """
    Validate student number format (e.g., 2022-0215)
    
    Args:
        student_number (str): Student number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^\d{4}-\d{4}$'
    return re.match(pattern, student_number) is not None


def validate_date(date_str, format='%Y-%m-%d'):
    """
    Validate date string
    
    Args:
        date_str (str): Date string to validate
        format (str): Expected date format
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        datetime.strptime(date_str, format)
        return True
    except (ValueError, TypeError):
        return False


def sanitize_input(text, max_length=None):
    """
    Sanitize user input
    
    Args:
        text (str): Text to sanitize
        max_length (int): Maximum allowed length
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Strip whitespace
    text = text.strip()
    
    # Limit length if specified
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text


def validate_file_extension(filename, allowed_extensions):
    """
    Validate file extension
    
    Args:
        filename (str): Filename to validate
        allowed_extensions (set): Set of allowed extensions (e.g., {'png', 'jpg'})
        
    Returns:
        bool: True if extension is allowed, False otherwise
    """
    if not filename or '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in allowed_extensions
