"""
Email Configuration Tester for IntellEvalPro
Tests email sending functionality with detailed diagnostics
"""
import os
from flask import Flask
from flask_mail import Mail, Message
from config import Config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_email_configuration():
    """Test email sending with detailed error reporting"""
    
    print("="*70)
    print("IntellEvalPro Email Configuration Tester")
    print("="*70)
    print()
    
    # Create Flask app with config
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Display configuration (mask password)
    print("📧 Current Email Configuration:")
    print(f"   MAIL_SERVER:   {app.config['MAIL_SERVER']}")
    print(f"   MAIL_PORT:     {app.config['MAIL_PORT']}")
    print(f"   MAIL_USE_TLS:  {app.config['MAIL_USE_TLS']}")
    print(f"   MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
    
    password = app.config.get('MAIL_PASSWORD', '')
    if password:
        masked = '*' * (len(password) - 4) + password[-4:] if len(password) > 4 else '****'
        print(f"   MAIL_PASSWORD: {masked} (last 4 chars shown)")
    else:
        print(f"   MAIL_PASSWORD: ❌ NOT SET")
    print()
    
    # Check if credentials are set
    if not app.config['MAIL_USERNAME'] or not password:
        print("❌ Email credentials not configured!")
        print()
        print("💡 Please update your .env file with:")
        print("   MAIL_USERNAME=your-email@gmail.com")
        print("   MAIL_PASSWORD=your-app-password")
        print()
        print("   For Gmail, use App Password:")
        print("   https://myaccount.google.com/apppasswords")
        print()
        return False
    
    # Initialize Flask-Mail
    mail = Mail(app)
    
    # Get test recipient
    print("📨 Email Test")
    print("-"*70)
    test_recipient = input("Enter test recipient email (or press Enter for sender): ").strip()
    
    if not test_recipient:
        test_recipient = app.config['MAIL_USERNAME']
    
    print(f"\n📤 Sending test email to: {test_recipient}")
    print("   Please wait...")
    print()
    
    # Try sending email
    with app.app_context():
        try:
            msg = Message(
                subject="IntellEvalPro Email Test",
                sender=app.config['MAIL_USERNAME'],
                recipients=[test_recipient]
            )
            
            msg.body = f"""
Hello!

This is a test email from IntellEvalPro Faculty Evaluation System.

If you receive this message, your email configuration is working correctly!

Configuration Details:
- MAIL SERVER: {app.config['MAIL_SERVER']}
- MAIL PORT: {app.config['MAIL_PORT']}
- TLS ENABLED: {app.config['MAIL_USE_TLS']}
- SENDER: {app.config['MAIL_USERNAME']}

Test performed on: {os.getenv('COMPUTERNAME', 'Unknown')}

---
IntellEvalPro Team
            """
            
            msg.html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #0059cc;">IntellEvalPro Email Test</h2>
                <p>Hello!</p>
                <p>This is a test email from <strong>IntellEvalPro Faculty Evaluation System</strong>.</p>
                <p style="background-color: #d4edda; padding: 15px; border-radius: 5px; color: #155724;">
                    ✅ If you receive this message, your email configuration is working correctly!
                </p>
                
                <h3>Configuration Details:</h3>
                <ul>
                    <li><strong>Mail Server:</strong> {app.config['MAIL_SERVER']}</li>
                    <li><strong>Mail Port:</strong> {app.config['MAIL_PORT']}</li>
                    <li><strong>TLS Enabled:</strong> {app.config['MAIL_USE_TLS']}</li>
                    <li><strong>Sender:</strong> {app.config['MAIL_USERNAME']}</li>
                </ul>
                
                <hr>
                <p style="color: #666; font-size: 12px;">
                    IntellEvalPro Team<br>
                    Test performed on: {os.getenv('COMPUTERNAME', 'Unknown')}
                </p>
            </body>
            </html>
            """
            
            mail.send(msg)
            
            print("="*70)
            print("✅ SUCCESS! Email sent successfully!")
            print("="*70)
            print()
            print(f"📬 Check {test_recipient} for the test email.")
            print()
            print("💡 Tips:")
            print("   • Check spam/junk folder if not in inbox")
            print("   • It may take a few seconds to arrive")
            print("   • If using Gmail, check 'All Mail' folder")
            print()
            return True
            
        except Exception as e:
            print("="*70)
            print("❌ FAILED! Email could not be sent")
            print("="*70)
            print()
            print(f"Error: {str(e)}")
            print()
            print("💡 Troubleshooting Tips:")
            print()
            
            error_str = str(e).lower()
            
            if 'authentication failed' in error_str or 'username and password not accepted' in error_str:
                print("🔐 Authentication Error:")
                print("   • For Gmail, use App Password (not your regular password)")
                print("   • Get it from: https://myaccount.google.com/apppasswords")
                print("   • Enable 2-Factor Authentication first")
                print()
            elif 'connection refused' in error_str or 'timed out' in error_str:
                print("🌐 Connection Error:")
                print("   • Check if firewall is blocking port 587")
                print("   • If on AWS, check Security Group outbound rules")
                print("   • Verify MAIL_SERVER address is correct")
                print()
            elif 'ssl' in error_str or 'certificate' in error_str:
                print("🔒 SSL/TLS Error:")
                print("   • Verify MAIL_USE_TLS is set to True")
                print("   • Try using port 465 with SSL instead")
                print("   • Check server supports TLS")
                print()
            else:
                print("❓ General Troubleshooting:")
                print("   • Verify all credentials in .env file")
                print("   • Check internet connection")
                print("   • Try a different email provider (e.g., AWS SES)")
                print()
            
            print("📚 For AWS deployment, see: docs/AWS_EMAIL_SETUP.md")
            print()
            return False

if __name__ == "__main__":
    success = test_email_configuration()
    print()
    input("Press Enter to exit...")
