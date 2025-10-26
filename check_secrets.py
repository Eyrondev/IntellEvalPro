"""
Check if environment variables are properly loaded
Debug tool for secret management
"""
import os
from dotenv import load_dotenv

# Try to load .env file
load_dotenv()

# List of required secrets
REQUIRED_SECRETS = [
    'SECRET_KEY',
    'DATABASE_URL',
    'GEMINI_API_KEY',
    'MAIL_SERVER',
    'MAIL_PORT',
    'MAIL_USE_TLS',
    'MAIL_USERNAME',
    'MAIL_PASSWORD'
]

def mask_value(value):
    """Mask secret value for display"""
    if not value:
        return "NOT SET"
    if len(value) <= 4:
        return "****"
    return value[:4] + '*' * (len(value) - 8) + value[-4:] if len(value) > 8 else value[:4] + '****'

def check_secrets():
    """Check all required environment variables"""
    print("="*70)
    print("Environment Variables Check")
    print("="*70)
    print()
    
    # Check .env file existence
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    print(f"📁 Working Directory: {os.getcwd()}")
    print(f"📄 .env file path: {env_file}")
    print(f"📄 .env exists: {'✅ YES' if os.path.exists(env_file) else '❌ NO'}")
    print()
    
    print("="*70)
    print("Environment Variables Status")
    print("="*70)
    print()
    
    missing = []
    found = []
    
    for secret in REQUIRED_SECRETS:
        value = os.getenv(secret)
        if value:
            masked = mask_value(value)
            print(f"✅ {secret:20s} : {masked}")
            found.append(secret)
        else:
            print(f"❌ {secret:20s} : NOT SET")
            missing.append(secret)
    
    print()
    print("="*70)
    print("Summary")
    print("="*70)
    print(f"✅ Found: {len(found)}/{len(REQUIRED_SECRETS)}")
    print(f"❌ Missing: {len(missing)}/{len(REQUIRED_SECRETS)}")
    
    if missing:
        print()
        print("Missing variables:")
        for var in missing:
            print(f"  - {var}")
    
    print("="*70)
    
    return len(missing) == 0

if __name__ == "__main__":
    success = check_secrets()
    print()
    
    if not success:
        print("💡 Troubleshooting Tips:")
        print()
        print("1. Make sure .env file exists in the project root")
        print("2. Check .env file has all required variables")
        print("3. On AWS, set environment variables via:")
        print("   - systemd service file")
        print("   - export in ~/.bashrc")
        print("   - AWS Parameter Store")
        print()
        print("See docs/AWS_SECRETS_MANAGEMENT.md for detailed guide")
    else:
        print("✅ All environment variables are properly set!")
    
    print()
    input("Press Enter to exit...")
