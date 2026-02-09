import os

# VULNERABILITY: Hardcoded Secrets
# These should be in environment variables, not committed to code
class Config:
    SECRET_KEY = "super_secret_key_change_me"
    AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
    AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    DB_NAME = "vulnerable.db"
    UPLOAD_FOLDER = "uploads"
    
    # Intentionally weak JWT secret
    JWT_SECRET = "secret"
