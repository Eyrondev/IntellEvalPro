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
        print(f"ℹ️ Not on AWS, skipping Parameter Store for {parameter_name}")
        return default
    
    try:
        ssm = boto3.client('ssm', region_name=os.getenv('AWS_REGION', 'ap-southeast-1'))
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        print(f"✅ Loaded {parameter_name} from AWS Parameter Store")
        return response['Parameter']['Value']
    except ClientError as e:
        if e.response['Error']['Code'] == 'ParameterNotFound':
            print(f"⚠️ Parameter {parameter_name} not found in AWS Parameter Store")
        else:
            print(f"⚠️ Could not retrieve {parameter_name} from AWS: {e}")
        return default
    except Exception as e:
        print(f"⚠️ Error accessing AWS Parameter Store: {e}")
        return default

def load_aws_secrets():
    """
    Load all secrets from AWS Parameter Store
    
    Returns:
        dict: Dictionary of loaded secrets
    """
    print("🔐 Attempting to load secrets from AWS Parameter Store...")
    
    secrets = {
        'SECRET_KEY': get_aws_secret('/intellevalpro/SECRET_KEY'),
        'DATABASE_URL': get_aws_secret('/intellevalpro/DATABASE_URL'),
        'GEMINI_API_KEY': get_aws_secret('/intellevalpro/GEMINI_API_KEY'),
        'MAIL_SERVER': get_aws_secret('/intellevalpro/MAIL_SERVER'),
        'MAIL_PORT': get_aws_secret('/intellevalpro/MAIL_PORT'),
        'MAIL_USE_TLS': get_aws_secret('/intellevalpro/MAIL_USE_TLS'),
        'MAIL_USERNAME': get_aws_secret('/intellevalpro/MAIL_USERNAME'),
        'MAIL_PASSWORD': get_aws_secret('/intellevalpro/MAIL_PASSWORD'),
    }
    
    # Set as environment variables (only if value exists)
    loaded_count = 0
    for key, value in secrets.items():
        if value:
            os.environ[key] = value
            loaded_count += 1
    
    if loaded_count > 0:
        print(f"✅ Loaded {loaded_count} secrets from AWS Parameter Store")
    else:
        print("ℹ️ No secrets loaded from AWS Parameter Store")
    
    return secrets

if __name__ == "__main__":
    # Test the AWS secrets loading
    print("="*70)
    print("AWS Secrets Manager Test")
    print("="*70)
    print()
    
    secrets = load_aws_secrets()
    
    print()
    print("="*70)
    print("Loaded Secrets:")
    print("="*70)
    
    for key, value in secrets.items():
        if value:
            masked = value[:4] + '*' * (len(value) - 4) if len(value) > 4 else '****'
            print(f"✅ {key}: {masked}")
        else:
            print(f"❌ {key}: NOT LOADED")
    
    print("="*70)
