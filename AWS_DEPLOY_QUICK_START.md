# 🚀 AWS Deployment Quick Start

## Problem: .env file not working on AWS

Your system now has **3 ways** to load secrets on AWS!

---

## ✅ Solution 1: Manual .env File (Easiest) ⭐

### On your AWS EC2 instance:

```bash
# 1. SSH into EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# 2. Navigate to project
cd /home/ubuntu/IntellEvalPro

# 3. Create .env file
nano .env

# 4. Paste your production secrets (see template below)

# 5. Save and set permissions
chmod 600 .env

# 6. Test
python check_secrets.py

# 7. Restart application
sudo systemctl restart intellevalpro
```

### .env Template for AWS:
```bash
SECRET_KEY=your-production-secret-key-here
DATABASE_URL=mysql+pymysql://admin:password@rds-host.amazonaws.com/intellevalpro_db
GEMINI_API_KEY=your-api-key-here
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
DEBUG=False
```

---

## ✅ Solution 2: Run Setup Script (Automated) 🤖

I created a helper script that will ask you for each secret:

```bash
# 1. SSH into EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# 2. Make script executable
chmod +x /home/ubuntu/IntellEvalPro/setup_aws_env.sh

# 3. Run setup script
./IntellEvalPro/setup_aws_env.sh
```

The script will:
- ✅ Prompt you for each secret
- ✅ Create .env file with secure permissions
- ✅ Add to ~/.bashrc for persistence
- ✅ Restart your application
- ✅ Test the configuration

---

## ✅ Solution 3: AWS Parameter Store (Advanced) 🏆

For production, use AWS Systems Manager Parameter Store:

### Setup:

```bash
# Install boto3
pip install boto3

# Store secrets in AWS
aws ssm put-parameter --name "/intellevalpro/SECRET_KEY" --value "your-key" --type "SecureString"
aws ssm put-parameter --name "/intellevalpro/DATABASE_URL" --value "mysql+pymysql://..." --type "SecureString"
aws ssm put-parameter --name "/intellevalpro/GEMINI_API_KEY" --value "your-key" --type "SecureString"
aws ssm put-parameter --name "/intellevalpro/MAIL_PASSWORD" --value "your-pass" --type "SecureString"
```

Your `config.py` is already configured to automatically load from AWS Parameter Store if boto3 is available!

---

## 🧪 Test Your Configuration

Run this on your EC2 to verify secrets are loaded:

```bash
python check_secrets.py
```

Expected output:
```
✅ SECRET_KEY         : prod****
✅ DATABASE_URL       : mysql****
✅ GEMINI_API_KEY     : AIza****
✅ MAIL_PASSWORD      : abcd****
```

---

## 🔍 Debug Commands

### Check if .env exists:
```bash
ls -la /home/ubuntu/IntellEvalPro/.env
```

### Check environment variables:
```bash
printenv | grep -E 'SECRET_KEY|DATABASE_URL'
```

### Test from Python:
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('SECRET_KEY:', os.getenv('SECRET_KEY', 'NOT SET')[:10])"
```

---

## 📋 What Changed in Your Code

### `config.py` is now smart:
1. ✅ Tries to load `.env` file first
2. ✅ Falls back to system environment variables
3. ✅ Optionally loads from AWS Parameter Store
4. ✅ Prints what source it used

### New files created:
- ✅ `aws_config.py` - AWS Parameter Store integration
- ✅ `check_secrets.py` - Verify secrets are loaded
- ✅ `setup_aws_env.sh` - Automated setup script
- ✅ `docs/AWS_SECRETS_MANAGEMENT.md` - Full documentation

---

## 🎯 Recommended Workflow

### For Local Development:
```bash
# Use .env file (already working)
python app.py
```

### For AWS Deployment:
```bash
# Option A: Use setup script (easiest)
./setup_aws_env.sh

# Option B: Manually create .env
nano .env
# paste secrets
chmod 600 .env

# Option C: Use AWS Parameter Store (most secure)
# Install boto3 and configure AWS CLI
pip install boto3
aws configure
# Store secrets in Parameter Store (see Solution 3 above)
```

---

## ✅ Deployment Checklist

- [ ] SSH into EC2 instance
- [ ] Choose a solution (1, 2, or 3)
- [ ] Set up secrets using chosen method
- [ ] Run `python check_secrets.py` to verify
- [ ] Set `.env` permissions: `chmod 600 .env`
- [ ] Restart application: `sudo systemctl restart intellevalpro`
- [ ] Test login, database, email functionality
- [ ] Check logs: `sudo journalctl -u intellevalpro -f`

---

## 🆘 Still Not Working?

1. **Check working directory:**
   ```bash
   python -c "import os; print(os.getcwd())"
   ```

2. **Check .env location:**
   ```bash
   python -c "import os; print(os.path.exists('.env'))"
   ```

3. **Check loaded values:**
   ```bash
   python check_secrets.py
   ```

4. **Check application logs:**
   ```bash
   sudo journalctl -u intellevalpro -n 50
   ```

---

## 📚 Full Documentation

See `docs/AWS_SECRETS_MANAGEMENT.md` for complete details!

---

**Your system is now ready for AWS deployment! 🚀**
