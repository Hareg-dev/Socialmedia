
# OAuth token creation and management functions
import secrets
import hashlib
import time
from datetime import datetime, timedelta

def generate_oauth_token(length=32):
    """Generate a secure random OAuth token"""
    return secrets.token_hex(length)

def create_access_token(user_id, expires_in=3600):
    """
    Create an OAuth access token
    
    Args:
        user_id: ID of the user
        expires_in: Token expiration time in seconds (default 1 hour)
    """
    token = generate_oauth_token()
    expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
    
    return {
        'access_token': token,
        'token_type': 'Bearer',
        'expires_in': expires_in,
        'expires_at': expires_at.timestamp(),
        'user_id': user_id
    }

def create_refresh_token(user_id):
    """Create a long-lived refresh token"""
    token = generate_oauth_token(length=48)
    return {
        'refresh_token': token,
        'user_id': user_id,
        'created_at': datetime.utcnow().timestamp()
    }

def verify_token(token, token_hash):
    """Verify an OAuth token against its hash"""
    calculated_hash = hashlib.sha256(token.encode()).hexdigest()
    return secrets.compare_digest(calculated_hash, token_hash)

def is_token_expired(expires_at):
    """Check if a token has expired"""
    return datetime.utcnow().timestamp() > expires_at

def revoke_token(token):
    """Revoke/invalidate an OAuth token"""
    # Add token to blacklist or mark as revoked in database
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    return {
        'token_hash': token_hash,
        'revoked_at': datetime.utcnow().timestamp()
    }

def refresh_access_token(refresh_token, user_id):
    """Refresh an access token using a refresh token"""
    if verify_token(refresh_token, user_id):
        return create_access_token(user_id)
    return None

