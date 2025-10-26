"""
Utilities package for IntellEvalPro
Provides helper functions and decorators
"""
from .security import generate_password_hash, check_password_hash
from .decorators import (
    login_required, 
    role_required, 
    admin_required, 
    student_required, 
    guidance_required
)
from .json_encoder import DecimalEncoder, DecimalJSONProvider, jsonify
from .validators import (
    validate_email,
    validate_username,
    validate_password,
    validate_student_number,
    validate_date,
    sanitize_input,
    validate_file_extension
)
from .email_utils import (
    send_email,
    send_bulk_emails,
    send_evaluation_start_notification,
    send_evaluation_reminder
)

__all__ = [
    'generate_password_hash',
    'check_password_hash',
    'login_required',
    'role_required',
    'admin_required',
    'student_required',
    'guidance_required',
    'DecimalEncoder',
    'DecimalJSONProvider',
    'jsonify',
    'validate_email',
    'validate_username',
    'validate_password',
    'validate_student_number',
    'validate_date',
    'sanitize_input',
    'validate_file_extension',
    'send_email',
    'send_bulk_emails',
    'send_evaluation_start_notification',
    'send_evaluation_reminder'
]

