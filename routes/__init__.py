"""
Routes package for IntellEvalPro
Provides route blueprints for modular application structure
"""
from .auth import auth_bp
from .admin import admin_bp
from .student import student_bp
from .guidance import guidance_bp
from .api import api_bp

__all__ = [
    'auth_bp',
    'admin_bp',
    'student_bp',
    'guidance_bp',
    'api_bp'
]
