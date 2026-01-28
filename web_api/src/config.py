"""
Configuration management for different environments
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(32))
    DATABASE = os.getenv('DATABASE_PATH', 'web-note.db')
    
    # Rate limiting
    RATELIMIT_DEFAULT = "200 per day, 50 per hour"
    RATELIMIT_STRICT = "1 per second"
    
    # Pagination
    ITEMS_PER_PAGE = 20


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')  # Must be set in production


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE = 'sqlite:///:memory:'
    RATELIMIT_ENABLED = False


# Select config based on environment
ENV = os.getenv('FLASK_ENV', 'development').lower()
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

current_config = config.get(ENV, DevelopmentConfig)
