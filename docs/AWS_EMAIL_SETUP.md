# 📧 Email Configuration for AWS Deployment

## 🚨 Problem: Email not working on AWS

When you host on AWS, Gmail SMTP often fails due to:
1. AWS security restrictions
2. Gmail blocking server IPs
3. Missing SSL certificates
4. Firewall/security group blocking ports

## ✅ Solutions (3 Options)

---

## **Option 1: Use AWS SES (RECOMMENDED)** 🏆

AWS Simple Email Service is designed for sending emails from AWS servers.

### Setup Steps:

1. **Go to AWS SES Console**
   - https://console.aws.amazon.com/ses

2. **Verify Your Email**
   - Click "Verified identities"
   - Add your sender email (e.g., noreply@yourdomain.com)
   - Verify via email link

3. **Request Production Access** (if needed)
   - By default, SES is in "Sandbox mode" (can only send to verified emails)
   - Request production access to send to anyone

4. **Get SMTP Credentials**
   - Go to "SMTP Settings"
   - Click "Create SMTP credentials"
   - Save the username and password

5. **Update `.env` on AWS**:
```bash
# AWS SES SMTP Configuration
MAIL_SERVER=email-smtp.ap-southeast-1.amazonaws.com  # Your AWS region
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=AKIAIOSFODNN7EXAMPLE  # SES SMTP username
MAIL_PASSWORD=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY  # SES SMTP password
```

### Advantages:
- ✅ Built for AWS - no blocking
- ✅ High deliverability
- ✅ Free tier: 62,000 emails/month
- ✅ Better reputation

---

## **Option 2: Configure Gmail for Server Access** 📧

If you want to keep using Gmail:

### Step 1: Enable 2-Factor Authentication
1. Go to Google Account Settings
2. Enable 2-Step Verification

### Step 2: Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Other (Custom name)"
3. Name it "IntellEvalPro AWS"
4. Copy the 16-character password (e.g., `xxxx xxxx xxxx xxxx`)

### Step 3: Update `.env` on AWS
```bash
# Gmail with App Password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=intellevalpro@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx  # ← App Password (no spaces in actual .env)
```

### Step 4: Allow Gmail from Server IP
1. Try sending an email
2. If blocked, check your Gmail inbox for "Suspicious sign-in prevented"
3. Click "Yes, it was me" to allow the server IP

### Step 5: Check AWS Security Group
Make sure **outbound port 587** is allowed:
```
Type: Custom TCP
Port: 587
Destination: 0.0.0.0/0
```

---

## **Option 3: Use SendGrid (Alternative)** 🚀

SendGrid is another email service provider:

### Setup:
1. Sign up at https://sendgrid.com (Free: 100 emails/day)
2. Create API Key
3. Use SMTP relay

```bash
# SendGrid SMTP
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey  # Literally the word "apikey"
MAIL_PASSWORD=SG.xxxxxxxxxxxxxxxxxxxxxxx  # Your SendGrid API key
```

---

## 🧪 Test Email Configuration

Create this test script to verify email works:

```python
# test_email.py
from flask import Flask
from flask_mail import Mail, Message
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Print configuration (masked password)
print("="*70)
print("Email Configuration Test")
print("="*70)
print(f"MAIL_SERVER: {app.config['MAIL_SERVER']}")
print(f"MAIL_PORT: {app.config['MAIL_PORT']}")
print(f"MAIL_USE_TLS: {app.config['MAIL_USE_TLS']}")
print(f"MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
print(f"MAIL_PASSWORD: {'*' * len(app.config['MAIL_PASSWORD']) if app.config['MAIL_PASSWORD'] else 'Not set'}")
print("="*70)

mail = Mail(app)

with app.app_context():
    try:
        msg = Message(
            subject="IntellEvalPro Test Email",
            sender=app.config['MAIL_USERNAME'],
            recipients=["your-test-email@gmail.com"]  # Change this
        )
        msg.body = """
        This is a test email from IntellEvalPro.
        
        If you receive this, your email configuration is working correctly!
        
        Server: {server}
        Port: {port}
        """.format(
            server=app.config['MAIL_SERVER'],
            port=app.config['MAIL_PORT']
        )
        
        mail.send(msg)
        print("✅ Email sent successfully!")
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
```

Run on your AWS server:
```bash
python test_email.py
```

---

## 🔍 Troubleshooting Common Errors

### Error: "Connection refused"
**Solution:** Check AWS Security Group - allow outbound port 587

### Error: "Username and Password not accepted"
**Solution:** 
- Use Gmail App Password (not regular password)
- Or switch to AWS SES

### Error: "timed out"
**Solution:** AWS might be blocking the port. Use AWS SES instead.

### Error: "Certificate verify failed"
**Solution:** Add to config.py:
```python
MAIL_USE_SSL = False
MAIL_USE_TLS = True
```

---

## 📝 Production `.env` Template for AWS

```bash
# Flask Configuration
SECRET_KEY=your-production-secret-key-here
DEBUG=False

# Database - AWS RDS
DATABASE_URL=mysql+pymysql://admin:password@your-rds-endpoint.rds.amazonaws.com:3306/intellevalpro_db

# Email - AWS SES (RECOMMENDED)
MAIL_SERVER=email-smtp.ap-southeast-1.amazonaws.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-ses-smtp-username
MAIL_PASSWORD=your-ses-smtp-password

# OR Email - Gmail with App Password (ALTERNATIVE)
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME=your-email@gmail.com
# MAIL_PASSWORD=your-app-password-here

# Google Gemini AI
GEMINI_API_KEY=your-api-key
```

---

## 🎯 Quick Fix Checklist

If email not working on AWS:

1. ✅ Check AWS Security Group allows port 587 outbound
2. ✅ Use Gmail App Password (not regular password)
3. ✅ Verify .env has correct MAIL_USERNAME and MAIL_PASSWORD
4. ✅ Test with test_email.py script
5. ✅ Check Gmail "Less secure apps" settings
6. ✅ Consider switching to AWS SES for better reliability

---

## 💡 My Recommendation

**For AWS Deployment:**
1. Use **AWS SES** - it's designed for this and won't have blocking issues
2. Keep Gmail for local development
3. Use different `.env` files for dev vs production

**Sagot sa tanong mo:** Gmail is being blocked by AWS or Gmail's security. Switch to AWS SES or use Gmail App Password! 🚀
