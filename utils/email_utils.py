"""
Email utility functions for IntellEvalPro
Handles sending emails for notifications, reminders, and alerts
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
from flask import current_app
import logging

logger = logging.getLogger(__name__)


def send_email(to_email, subject, body_html, body_text=None, from_name='IntellEvalPro'):
    """
    Send an email using SMTP
    
    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        body_html (str): HTML body content
        body_text (str, optional): Plain text body content
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Get email configuration from Flask config
        mail_server = current_app.config.get('MAIL_SERVER')
        mail_port = current_app.config.get('MAIL_PORT')
        mail_use_tls = current_app.config.get('MAIL_USE_TLS')
        mail_username = current_app.config.get('MAIL_USERNAME')
        mail_password = current_app.config.get('MAIL_PASSWORD')

        # Validate email configuration
        if not mail_username or not mail_password:
            logger.error('Email credentials not configured (MAIL_USERNAME or MAIL_PASSWORD missing)')
            return False

        # Create message
        msg = MIMEMultipart('alternative')
        # Use a friendly From header for better trust (Name <email>)
        msg['From'] = f"{from_name} <{mail_username}>"
        # Optional headers for deliverability and user trust
        reply_to = current_app.config.get('MAIL_REPLY_TO')
        if reply_to:
            msg['Reply-To'] = reply_to
        list_unsub = current_app.config.get('MAIL_LIST_UNSUBSCRIBE')
        if list_unsub:
            msg['List-Unsubscribe'] = list_unsub
        msg['To'] = to_email
        msg['Subject'] = subject

        # Add plain text part if provided
        if body_text:
            part1 = MIMEText(body_text, 'plain')
            msg.attach(part1)

        # Add HTML part
        part2 = MIMEText(body_html, 'html')
        msg.attach(part2)

        # Embed logo inline if the static logo exists - reduces image blocking
        try:
            logo_path = current_app.config.get('LOGO_PATH', 'static/images/nclogo.png')
            with open(logo_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', '<logo>')
                img.add_header('Content-Disposition', 'inline', filename='nclogo.png')
                msg.attach(img)
        except Exception:
            # It's non-fatal if logo embedding fails; external URL will be used instead
            logger.debug('Failed to embed logo inline; falling back to URL')

        # Send email
        with smtplib.SMTP(mail_server, mail_port, timeout=30) as server:
            # Advertise ourselves and start TLS if configured
            try:
                server.ehlo()
                if mail_use_tls:
                    server.starttls()
                    server.ehlo()
            except Exception as tls_err:
                # Non-fatal: log and continue (login may still fail later)
                logger.debug(f'TLS handshake issue: {tls_err}')

            # Enable SMTP debug level when running in debug mode
            try:
                if getattr(current_app, 'debug', False):
                    server.set_debuglevel(1)
            except Exception:
                pass

            server.login(mail_username, mail_password)
            server.send_message(msg)

        logger.info(f'Email sent successfully to {to_email} via {mail_server}:{mail_port}')
        return True

    except Exception as e:
        # Log full exception with stack trace for easier debugging (do not expose sensitive info)
        logger.exception(f'Failed to send email to {to_email}: {e}')
        return False


def send_bulk_emails(recipients, subject, body_html, body_text=None):
    """
    Send emails to multiple recipients using optimized batch processing
    
    Args:
        recipients (list): List of recipient email addresses
        subject (str): Email subject
        body_html (str): HTML body content
        body_text (str, optional): Plain text body content
        
    Returns:
        dict: Statistics about email sending (sent, failed)
    """
    import concurrent.futures
    from threading import Lock
    
    stats = {
        'sent': 0,
        'failed': 0,
        'total': len(recipients)
    }
    
    stats_lock = Lock()
    
    def send_single_email(email):
        """Send email and update stats thread-safely"""
        success = send_email(email, subject, body_html, body_text)
        with stats_lock:
            if success:
                stats['sent'] += 1
            else:
                stats['failed'] += 1
        return success
    
    # Use ThreadPoolExecutor for parallel email sending (max 5 concurrent connections)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(send_single_email, recipients)
    
    return stats


def _render_reset_template(user_name, reset_url, expiry_hours=1):
    """
    Render a polished password reset HTML and plain text template.
    """
    app_url = current_app.config.get('APP_URL', 'http://localhost:5000')
    logo_url = f"{app_url.rstrip('/')}/static/images/nclogo.png"
    # Keep the reset email minimal and clean for better deliverability
    body_html = f"""<!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Password Reset</title>
        <style>
            body {{ font-family: Arial, Helvetica, sans-serif; background: #f6f8fb; margin: 0; padding: 0; color: #222 }}
            .container {{ max-width: 600px; margin: 28px auto; background: #fff; border-radius: 6px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.06) }}
            .header {{ background: #0059cc; padding: 18px; text-align: center; color: #fff }}
            .header img {{ height: 40px; vertical-align: middle }}
            .content {{ padding: 20px; font-size: 14px; line-height: 1.6 }}
            .btn {{ display: inline-block; padding: 10px 18px; background: #0059cc; color: #fff !important; text-decoration: none; border-radius: 6px; font-weight: 600 }}
            .footer {{ padding: 14px; text-align: center; font-size: 12px; color: #6b7280; background: #fbfdff }}
            a {{ color: #0059cc }}
            h2 {{ color: #0f172a }}
            p, a {{ color: #0f172a }}
        </style>
    </head>
    <body>
        <div class="container">
                    <div class="header">
                        <img src="cid:logo" alt="Norzagaray College">
                    </div>
            <div class="content">
                <h2 style="margin-top:0;color:#0f172a">Password Reset</h2>
                <p>Hi {user_name or 'there'},</p>
                <p>We've received a request to reset your password for your IntellEvalPro account. Click the button below to reset it. This link will expire in {expiry_hours} hour(s).</p>
                <p style="text-align:center; margin: 22px 0;">
                    <a href="{reset_url}" class="btn" style="color:#ffffff; background:#0059cc; display:inline-block; padding:10px 18px; text-decoration:none; border-radius:6px;">Reset Password</a>
                </p>
                <p>If you didn't request this, you can ignore this email and no changes will be made.</p>
                <p style="font-size:12px; color:#6b7280;">If the button doesn't work, copy and paste this URL into your browser:</p>
                <p style="font-size:12px;"><a href="{reset_url}">{reset_url}</a></p>
            </div>
            <div class="footer">IntellEvalPro - Norzagaray College<br>If you need help, contact: <a href="mailto:guidance@norzagaraycollege.edu.ph">guidance@norzagaraycollege.edu.ph</a></div>
        </div>
    </body>
    </html>"""

    body_text = f"""
    Hi {user_name or 'there'},

    We received a request to reset your IntellEvalPro account password. Visit the following link to reset it (expires in {expiry_hours} hour(s)):

    {reset_url}

    If you didn't request this, you can ignore this message.

    IntellEvalPro - Norzagaray College
    """

    return body_html, body_text


def send_evaluation_start_notification(student_email, student_name, period_title, start_date, end_date):
    """
    Send notification to user when evaluation period starts
    
    Args:
        student_email (str): User's email address
        student_name (str): User's full name
        period_title (str): Evaluation period title
        start_date (str): Start date of evaluation period
        end_date (str): End date of evaluation period
        
    Returns:
        bool: True if email sent successfully
    """
    subject = f"📝 Evaluation Period Started: {period_title}"
    
    # Format dates for display
    start_formatted = datetime.strptime(start_date, '%Y-%m-%d').strftime('%B %d, %Y')
    end_formatted = datetime.strptime(end_date, '%Y-%m-%d').strftime('%B %d, %Y')
    
    # HTML body
    body_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #0059cc 0%, #004099 100%);
                color: white;
                padding: 30px 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
                font-weight: 600;
            }}
            .content {{
                padding: 30px 20px;
            }}
            .greeting {{
                font-size: 18px;
                margin-bottom: 20px;
                color: #333;
            }}
            .message {{
                margin-bottom: 25px;
                color: #555;
                font-size: 15px;
            }}
            .info-box {{
                background-color: #e6f0ff;
                border-left: 4px solid #0059cc;
                padding: 15px;
                margin: 20px 0;
                border-radius: 4px;
            }}
            .info-box h3 {{
                margin: 0 0 10px 0;
                color: #0059cc;
                font-size: 16px;
            }}
            .info-box p {{
                margin: 5px 0;
                color: #333;
            }}
            .deadline {{
                background-color: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 20px 0;
                border-radius: 4px;
            }}
            .deadline strong {{
                color: #d97706;
                font-size: 16px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 30px;
                background-color: #0059cc;
                color: white !important;
                text-decoration: none;
                border-radius: 5px;
                font-weight: 600;
                margin: 20px 0;
                text-align: center;
            }}
            .button:hover {{
                background-color: #004099;
            }}
            .footer {{
                background-color: #f8f9fa;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #6c757d;
                border-top: 1px solid #dee2e6;
            }}
            .important {{
                color: #d97706;
                font-weight: 600;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎓 Faculty Evaluation Period</h1>
            </div>
            
            <div class="content">
                <div class="greeting">
                    Hello <strong>{student_name}</strong>,
                </div>
                
                <div class="message">
                    <p>A new evaluation period has officially started! This is an important opportunity to assess faculty performance and contribute to improving the quality of education at Norzagaray College.</p>
                </div>
                
                <div class="info-box">
                    <h3>📋 Evaluation Details</h3>
                    <p><strong>Period:</strong> {period_title}</p>
                    <p><strong>Start Date:</strong> {start_formatted}</p>
                    <p><strong>End Date:</strong> {end_formatted}</p>
                </div>
                
                <div class="deadline">
                    <p><strong>⏰ Important Deadline: {end_formatted}</strong></p>
                    <p>Please ensure all evaluations are completed before the deadline expires.</p>
                </div>
                
                <div style="text-align: center;">
                    <a href="http://localhost:5000/student/pending-evaluations" class="button">
                        Start Evaluation Now →
                    </a>
                </div>
                
                <div class="message" style="margin-top: 25px;">
                    <p><strong>Important Reminders:</strong></p>
                    <ul style="color: #555;">
                        <li>Your responses are completely <span class="important">anonymous</span></li>
                        <li>Please provide honest and constructive feedback</li>
                        <li>Evaluate all your enrolled faculty members</li>
                        <li>Complete the evaluation before the deadline</li>
                    </ul>
                </div>
                
                <div class="message" style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #e0e0e0;">
                    <p style="font-size: 14px; color: #666;">
                        If you have any questions or concerns, please contact the Guidance Office.
                    </p>
                </div>
            </div>
            
            <div class="footer">
                <p><strong>IntellEvalPro - Faculty Evaluation System</strong></p>
                <p>Norzagaray College</p>
                <p style="margin-top: 10px; font-size: 11px;">
                    This is an automated message. Please do not reply to this email.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text alternative
    body_text = f"""
    Hello {student_name},
    
    The evaluation period has officially started!
    
    EVALUATION DETAILS
    Period: {period_title}
    Started: {start_formatted}
    Deadline: {end_formatted}
    
    Please complete your evaluations before the deadline expires.
    
    IMPORTANT REMINDERS:
    - Your responses are completely anonymous
    - Please provide honest and constructive feedback
    - Evaluate all your enrolled faculty members
    - Complete the evaluation before the deadline
    
    Visit http://localhost:5000/student/pending-evaluations to start your evaluation.
    
    If you have any questions, please contact the Guidance Office.
    
    ---
    IntellEvalPro - Faculty Evaluation System
    Norzagaray College
    """
    
    return send_email(student_email, subject, body_html, body_text)


def send_evaluation_reminder(student_email, student_name, period_title, end_date, pending_count):
    """
    Send reminder to student about pending evaluations
    
    Args:
        student_email (str): Student's email address
        student_name (str): Student's full name
        period_title (str): Evaluation period title
        end_date (str): End date of evaluation period
        pending_count (int): Number of pending evaluations
        
    Returns:
        bool: True if email sent successfully
    """
    subject = f"⏰ Reminder: {pending_count} Pending Evaluation(s) - {period_title}"
    
    end_formatted = datetime.strptime(end_date, '%Y-%m-%d').strftime('%B %d, %Y')
    
    body_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                color: white;
                padding: 30px 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
                font-weight: 600;
            }}
            .content {{
                padding: 30px 20px;
            }}
            .alert-box {{
                background-color: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 20px;
                margin: 20px 0;
                border-radius: 4px;
                text-align: center;
            }}
            .alert-box h2 {{
                margin: 0 0 10px 0;
                color: #d97706;
                font-size: 32px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 30px;
                background-color: #f59e0b;
                color: white !important;
                text-decoration: none;
                border-radius: 5px;
                font-weight: 600;
                margin: 20px 0;
            }}
            .footer {{
                background-color: #f8f9fa;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #6c757d;
                border-top: 1px solid #dee2e6;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⏰ Evaluation Reminder</h1>
            </div>
            
            <div class="content">
                <p>Hello <strong>{student_name}</strong>,</p>
                
                <div class="alert-box">
                    <h2>{pending_count}</h2>
                    <p style="font-size: 18px; margin: 0;">Pending Evaluation(s)</p>
                </div>
                
                <p style="text-align: center; font-size: 16px; color: #d97706; font-weight: 600;">
                    Deadline: {end_formatted}
                </p>
                
                <p style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:5000/student/pending-evaluations" class="button">
                        Complete Evaluations Now
                    </a>
                </p>
                
                <p style="text-align: center; color: #666;">
                    Please complete your evaluations before the deadline to ensure your voice is heard.
                </p>
            </div>
            
            <div class="footer">
                <p><strong>IntellEvalPro - Faculty Evaluation System</strong></p>
                <p>Norzagaray College</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    body_text = f"""
    Hello {student_name},
    
    REMINDER: You have {pending_count} pending evaluation(s)
    
    Period: {period_title}
    Deadline: {end_formatted}
    
    Please visit http://localhost:5000/student/pending-evaluations to complete your evaluations.
    
    ---
    IntellEvalPro - Norzagaray College
    """
    
    return send_email(student_email, subject, body_html, body_text)
