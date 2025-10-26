# Gmail App Password Setup Guide for IntellEvalPro

## 🎯 Goal
Enable Gmail SMTP to work from your AWS server using App Password

---

## 📋 Step-by-Step Instructions

### Step 1: Enable 2-Factor Authentication (2FA)

1. **Go to Google Account Security**
   - Visit: https://myaccount.google.com/security
   - Sign in with your Gmail account

2. **Find "2-Step Verification"**
   - Look for "How you sign in to Google" section
   - Click "2-Step Verification"

3. **Turn On 2-Step Verification**
   - Click "Get Started"
   - Follow the prompts (you'll need your phone)
   - Complete the setup

   **⚠️ IMPORTANT:** You MUST enable 2FA before you can create App Passwords!

---

### Step 2: Generate App Password

1. **Go to App Passwords Page**
   - Direct link: https://myaccount.google.com/apppasswords
   - Or: Google Account → Security → 2-Step Verification → App Passwords (at bottom)

2. **Create New App Password**
   - **Select app:** Mail
   - **Select device:** Other (Custom name)
   - **Name it:** IntellEvalPro AWS Server
   - Click "Generate"

3. **Copy the 16-Character Password**
   ```
   Example: abcd efgh ijkl mnop
   ```
   ⚠️ **SAVE THIS NOW!** You won't be able to see it again.

4. **Click "Done"**

---

### Step 3: Update Your AWS Server `.env` File

1. **Connect to your AWS server** (via SSH or EC2 console)

2. **Navigate to your project directory**
   ```bash
   cd /path/to/IntellEvalPro
   ```

3. **Edit the `.env` file**
   ```bash
   nano .env
   # or
   vim .env
   ```

4. **Update Email Configuration:**
   ```bash
   # Email Configuration - Gmail with App Password
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=intellevalpro@gmail.com
   MAIL_PASSWORD=abcdefghijklmnop
   ```
   
   **⚠️ IMPORTANT:** 
   - Remove ALL spaces from the App Password
   - Example: `abcd efgh ijkl mnop` → `abcdefghijklmnop`

5. **Save and exit**
   - For nano: `Ctrl + X`, then `Y`, then `Enter`
   - For vim: `:wq` then `Enter`

---

### Step 4: Update AWS Security Group

Your EC2 instance needs to allow outbound SMTP traffic:

1. **Go to AWS EC2 Console**
   - https://console.aws.amazon.com/ec2/

2. **Select Your Instance**
   - Click on your IntellEvalPro instance

3. **Click "Security" tab**
   - Find the Security Group name (e.g., `sg-xxxxx`)
   - Click on the security group

4. **Edit Outbound Rules**
   - Click "Outbound rules" tab
   - Click "Edit outbound rules"

5. **Add SMTP Rule** (if not exists)
   - Click "Add rule"
   - **Type:** Custom TCP
   - **Port range:** 587
   - **Destination:** 0.0.0.0/0
   - **Description:** Gmail SMTP
   - Click "Save rules"

---

### Step 5: Restart Your Application

1. **Stop the application** (if running)
   ```bash
   # If using systemd
   sudo systemctl stop intellevalpro
   
   # If running manually
   # Press Ctrl+C to stop
   ```

2. **Restart the application**
   ```bash
   # If using systemd
   sudo systemctl start intellevalpro
   
   # If running manually
   python app.py
   ```

---

### Step 6: Test Email Configuration

1. **Run the email tester on your AWS server**
   ```bash
   python test_email.py
   ```

2. **Enter a test email address** when prompted
   - Use your own email to receive the test

3. **Check results:**
   - ✅ **Success:** You'll see "Email sent successfully!"
   - ❌ **Failed:** Follow the troubleshooting tips below

---

## 🧪 Quick Test Command

Run this one-liner to test email from command line:

```bash
python -c "from test_email import test_email_configuration; test_email_configuration()"
```

---

## 🔍 Troubleshooting

### Error: "Username and Password not accepted"

**Possible causes:**
- App Password has spaces (remove them)
- App Password was copied incorrectly
- 2FA is not enabled
- Used regular password instead of App Password

**Solution:**
1. Generate a new App Password
2. Copy it WITHOUT spaces
3. Update `.env` file
4. Restart application

---

### Error: "Connection timed out" or "Connection refused"

**Possible causes:**
- AWS Security Group blocking port 587
- Firewall blocking SMTP

**Solution:**
1. Check AWS Security Group outbound rules
2. Ensure port 587 is allowed to 0.0.0.0/0
3. Check if UFW or iptables is blocking: `sudo ufw status`

---

### Error: "Suspicious sign-in prevented"

**Cause:**
Gmail detected login from new location (AWS server IP)

**Solution:**
1. Check your Gmail inbox for "Suspicious sign-in prevented" email
2. Click "Yes, it was me" to allow the server IP
3. Try sending email again within 10 minutes

---

### Email Sends but Goes to Spam

**Solutions:**
- Add SPF record to your domain DNS (if using custom domain)
- Use a professional email address (not just gmail.com)
- Consider using AWS SES for better deliverability

---

## 📝 Complete `.env` Example for AWS

```bash
# Flask Configuration
SECRET_KEY=your-production-secret-key-here
FLASK_ENV=production
DEBUG=False

# Database - AWS RDS
DATABASE_URL=mysql+pymysql://admin:password@your-rds-endpoint.rds.amazonaws.com:3306/intellevalpro_db

# Email - Gmail with App Password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=intellevalpro@gmail.com
MAIL_PASSWORD=abcdefghijklmnop

# Google Gemini AI
GEMINI_API_KEY=your-api-key-here
```

---

## ✅ Verification Checklist

Before deploying, make sure:

- [ ] 2-Factor Authentication enabled on Gmail
- [ ] App Password generated (16 characters)
- [ ] App Password copied WITHOUT spaces
- [ ] `.env` updated on AWS server
- [ ] AWS Security Group allows port 587 outbound
- [ ] Application restarted
- [ ] Test email sent successfully
- [ ] Test email received (check spam folder)

---

## 🎯 Summary

**What you did:**
1. ✅ Enabled 2FA on Gmail account
2. ✅ Generated App Password for server use
3. ✅ Updated `.env` with App Password (no spaces)
4. ✅ Configured AWS Security Group
5. ✅ Tested email functionality

**Result:**
Your IntellEvalPro system on AWS can now send emails via Gmail! 📧

---

## 💡 Pro Tips

1. **Keep App Password secure** - treat it like a password
2. **Name your App Passwords** - easy to revoke later if needed
3. **Use different App Passwords** - one per application/server
4. **Monitor Gmail activity** - check for suspicious logins
5. **Consider AWS SES** - for production use (better deliverability)

---

## 🆘 Still Not Working?

If you've followed all steps and email still doesn't work:

1. **Check application logs:**
   ```bash
   tail -f /var/log/intellevalpro/error.log
   ```

2. **Try sending test email manually:**
   ```bash
   python test_email.py
   ```

3. **Verify `.env` is loaded:**
   ```bash
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('MAIL_PASSWORD:', os.getenv('MAIL_PASSWORD')[:4] + '****')"
   ```

4. **Consider switching to AWS SES** (see `AWS_EMAIL_SETUP.md`)

---

## 📚 Additional Resources

- Gmail App Passwords: https://support.google.com/accounts/answer/185833
- Flask-Mail Documentation: https://pythonhosted.org/Flask-Mail/
- AWS SES Setup: See `AWS_EMAIL_SETUP.md` in this folder

---

**Good luck! Your email should now work on AWS! 🚀**
