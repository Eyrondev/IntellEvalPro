# 🔐 Managing Secrets on AWS - Multiple Solutions

## ❌ Problem: AWS doesn't read `.env` file automatically

When you deploy to AWS (EC2, Elastic Beanstalk, Lambda), your application might not read the `.env` file because:
1. `.env` file is in `.gitignore` (not in repository)
2. Environment variables need to be set differently on servers
3. Cloud platforms use their own secret management systems

---

## ✅ Solution 1: AWS Systems Manager Parameter Store (RECOMMENDED) 🏆

Store secrets in AWS and load them at runtime.

### Setup:

1. **Store secrets in AWS Parameter Store**
   ```bash
   # Using AWS CLI
   aws ssm put-parameter --name "/intellevalpro/SECRET_KEY" --value "your-secret-key" --type "SecureString"
   aws ssm put-parameter --name "/intellevalpro/DATABASE_URL" --value "mysql+pymysql://..." --type "SecureString"
   aws ssm put-parameter --name "/intellevalpro/GEMINI_API_KEY" --value "your-api-key" --type "SecureString"
   aws ssm put-parameter --name "/intellevalpro/MAIL_PASSWORD" --value "your-password" --type "SecureString"
   ```

2. **Install boto3 (AWS SDK)**
   ```bash
   pip install boto3
   ```

3. **Create `aws_config.py`** (see code below)

4. **Update `config.py`** to use AWS secrets

### Code Implementation:

**Create `aws_config.py`:**
```python
"""
AWS Secrets Manager Integration
Loads secrets from AWS Systems Manager Parameter Store
"""
import os
import boto3
from botocore.exceptions import ClientError

def get_aws_secret(parameter_name, default=None):
    """
    Retrieve secret from AWS Parameter Store
    
    Args:
        parameter_name: Name of the parameter (e.g., '/intellevalpro/SECRET_KEY')
        default: Default value if parameter not found
        
    Returns:
        Secret value or default
    """
    # Check if running on AWS (has AWS credentials)
    if not os.getenv('AWS_REGION') and not os.path.exists(os.path.expanduser('~/.aws/credentials')):
        return default
    
    try:
        ssm = boto3.client('ssm', region_name=os.getenv('AWS_REGION', 'ap-southeast-1'))
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        return response['Parameter']['Value']
    except ClientError as e:
        print(f"Warning: Could not retrieve {parameter_name} from AWS: {e}")
        return default
    except Exception as e:
        print(f"Warning: Error accessing AWS Parameter Store: {e}")
        return default

def load_aws_secrets():
    """Load all secrets from AWS Parameter Store"""
    secrets = {
        'SECRET_KEY': get_aws_secret('/intellevalpro/SECRET_KEY'),
        'DATABASE_URL': get_aws_secret('/intellevalpro/DATABASE_URL'),
        'GEMINI_API_KEY': get_aws_secret('/intellevalpro/GEMINI_API_KEY'),
        'MAIL_USERNAME': get_aws_secret('/intellevalpro/MAIL_USERNAME'),
        'MAIL_PASSWORD': get_aws_secret('/intellevalpro/MAIL_PASSWORD'),
    }
    
    # Set as environment variables
    for key, value in secrets.items():
        if value:
            os.environ[key] = value
    
    return secrets
```

**Update `config.py`:**
```python
import os
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

# Try to load AWS secrets if on AWS
try:
    from aws_config import load_aws_secrets
    load_aws_secrets()
    print("✅ Loaded secrets from AWS Parameter Store")
except ImportError:
    print("ℹ️ AWS config not available, using .env file")
except Exception as e:
    print(f"⚠️ Could not load AWS secrets: {e}")

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
    # ... rest of config
```

---

## ✅ Solution 2: Export Environment Variables Directly on EC2

Set environment variables directly on your EC2 instance.

### Method A: Using ~/.bashrc (Persistent)

1. **SSH into your EC2 instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

2. **Edit ~/.bashrc**
   ```bash
   nano ~/.bashrc
   ```

3. **Add environment variables at the end:**
   ```bash
   # IntellEvalPro Environment Variables
   export SECRET_KEY="your-secret-key-here"
   export DATABASE_URL="mysql+pymysql://admin:password@host/db"
   export GEMINI_API_KEY="your-api-key"
   export MAIL_SERVER="smtp.gmail.com"
   export MAIL_PORT="587"
   export MAIL_USE_TLS="True"
   export MAIL_USERNAME="your-email@gmail.com"
   export MAIL_PASSWORD="your-app-password"
   export DEBUG="False"
   ```

4. **Save and reload**
   ```bash
   source ~/.bashrc
   ```

5. **Verify**
   ```bash
   echo $SECRET_KEY
   ```

### Method B: Using systemd service file

If running as a systemd service:

1. **Edit your service file**
   ```bash
   sudo nano /etc/systemd/system/intellevalpro.service
   ```

2. **Add Environment variables:**
   ```ini
   [Unit]
   Description=IntellEvalPro Faculty Evaluation System
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/IntellEvalPro
   Environment="SECRET_KEY=your-secret-key"
   Environment="DATABASE_URL=mysql+pymysql://admin:password@host/db"
   Environment="GEMINI_API_KEY=your-api-key"
   Environment="MAIL_SERVER=smtp.gmail.com"
   Environment="MAIL_PORT=587"
   Environment="MAIL_USE_TLS=True"
   Environment="MAIL_USERNAME=your-email@gmail.com"
   Environment="MAIL_PASSWORD=your-app-password"
   Environment="DEBUG=False"
   ExecStart=/usr/bin/python3 /home/ubuntu/IntellEvalPro/app.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. **Reload and restart**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart intellevalpro
   ```

---

## ✅ Solution 3: Use .env file on EC2 (Simple but Manual)

Manually create `.env` file on your EC2 instance.

### Steps:

1. **SSH into EC2**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

2. **Navigate to project directory**
   ```bash
   cd /home/ubuntu/IntellEvalPro
   ```

3. **Create .env file**
   ```bash
   nano .env
   ```

4. **Paste your production secrets:**
   ```bash
   # Production Configuration
   SECRET_KEY=your-production-secret-key
   DATABASE_URL=mysql+pymysql://admin:password@rds-host.amazonaws.com/intellevalpro_db
   GEMINI_API_KEY=your-api-key
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=intellevalpro@gmail.com
   MAIL_PASSWORD=your-app-password
   DEBUG=False
   ```

5. **Save and set permissions**
   ```bash
   chmod 600 .env  # Only owner can read/write
   ```

6. **Restart application**
   ```bash
   sudo systemctl restart intellevalpro
   ```

---

## ✅ Solution 4: AWS Elastic Beanstalk Environment Variables

If using Elastic Beanstalk:

### Via Console:

1. Go to Elastic Beanstalk Console
2. Select your application
3. Go to **Configuration** → **Software**
4. Under **Environment properties**, add:
   - `SECRET_KEY` = `your-secret-key`
   - `DATABASE_URL` = `mysql+pymysql://...`
   - `GEMINI_API_KEY` = `your-api-key`
   - `MAIL_PASSWORD` = `your-password`
5. Click **Apply**

### Via EB CLI:

```bash
eb setenv SECRET_KEY="your-secret-key" \
         DATABASE_URL="mysql+pymysql://..." \
         GEMINI_API_KEY="your-api-key" \
         MAIL_PASSWORD="your-password"
```

---

## ✅ Solution 5: Docker Environment Variables

If using Docker on AWS:

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  intellevalpro:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - MAIL_PASSWORD=${MAIL_PASSWORD}
    env_file:
      - .env.production
```

**.env.production** (on EC2):
```bash
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://...
GEMINI_API_KEY=your-api-key
MAIL_PASSWORD=your-password
```

---

## 🎯 Recommended Approach for Your Project

### For Production (AWS EC2):

**Use Solution 2B (systemd) + Solution 3 (.env backup)**

1. **Primary:** Store secrets in systemd service file (Solution 2B)
2. **Backup:** Also create `.env` file on server (Solution 3)
3. **Future:** Migrate to AWS Parameter Store (Solution 1)

### Implementation:

**Update `config.py` to be smart about loading:**

```python
"""
Configuration module for IntellEvalPro
Loads environment variables from .env file OR system environment
"""
import os
from dotenv import load_dotenv

# Try to load .env file (works locally and as backup on server)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print(f"✅ Loaded environment from .env file")
else:
    print(f"ℹ️ No .env file found, using system environment variables")

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY') or os.environ.get('SECRET_KEY', 'fallback-key')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or os.environ.get('DATABASE_URL', 'mysql+pymysql://root:@localhost:3306/intellevalpro_db')
    
    # ... rest of config
```

---

## 📋 Deployment Checklist

When deploying to AWS:

- [ ] Choose a secret management solution (recommend: systemd + .env)
- [ ] Set all environment variables on EC2
- [ ] Verify secrets are loaded: `python -c "import os; print(os.getenv('SECRET_KEY')[:5] + '***')"`
- [ ] Update security: `chmod 600 .env` (if using .env file)
- [ ] Test application startup
- [ ] Check logs for "Loaded environment" message
- [ ] Test functionality (login, database, email)

---

## 🔍 Debugging: Check if secrets are loaded

**Create `check_secrets.py`:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

secrets = ['SECRET_KEY', 'DATABASE_URL', 'GEMINI_API_KEY', 'MAIL_PASSWORD']

print("="*70)
print("Environment Variables Check")
print("="*70)

for secret in secrets:
    value = os.getenv(secret)
    if value:
        masked = value[:4] + '*' * (len(value) - 4) if len(value) > 4 else '****'
        print(f"✅ {secret}: {masked}")
    else:
        print(f"❌ {secret}: NOT SET")

print("="*70)
```

Run on AWS:
```bash
python check_secrets.py
```

---

## 💡 Best Practices

1. **Never commit .env to git** ✅ Already in `.gitignore`
2. **Use different secrets for dev/prod** - Don't reuse production keys
3. **Rotate secrets regularly** - Change passwords periodically
4. **Use IAM roles on EC2** - For AWS Parameter Store access
5. **Set proper file permissions** - `chmod 600 .env`
6. **Log secret loading** - Know where secrets came from

---

## 🆘 Still Not Working?

Run this debug command on your AWS server:

```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('SECRET_KEY:', os.getenv('SECRET_KEY', 'NOT SET')[:10] + '...')
print('DATABASE_URL:', os.getenv('DATABASE_URL', 'NOT SET')[:30] + '...')
print('Working dir:', os.getcwd())
print('.env exists:', os.path.exists('.env'))
"
```

This will show you exactly what's being loaded! 🔍
