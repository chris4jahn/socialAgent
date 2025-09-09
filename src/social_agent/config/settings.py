"""Configuration management for Social Agent."""

try:
    from pydantic import BaseSettings, Field
except ImportError:
    # Fallback for pydantic v2
    from pydantic_settings import BaseSettings
    from pydantic import Field

from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # Azure AI Configuration
    azure_ai_endpoint: str = Field(..., env="AZURE_AI_ENDPOINT")
    azure_ai_api_key: Optional[str] = Field(None, env="AZURE_AI_API_KEY")
    azure_ai_deployment_name: str = Field("gpt-4", env="AZURE_AI_DEPLOYMENT_NAME")
    
    # Azure Identity (alternative to API key)
    azure_client_id: Optional[str] = Field(None, env="AZURE_CLIENT_ID")
    azure_client_secret: Optional[str] = Field(None, env="AZURE_CLIENT_SECRET")
    azure_tenant_id: Optional[str] = Field(None, env="AZURE_TENANT_ID")
    
    # Application Settings
    log_level: str = Field("INFO", env="LOG_LEVEL")
    workflow_timeout: int = Field(300, env="WORKFLOW_TIMEOUT")
    
    # Social Media Platform Settings (optional)
    twitter_api_key: Optional[str] = Field(None, env="TWITTER_API_KEY")
    linkedin_api_key: Optional[str] = Field(None, env="LINKEDIN_API_KEY")
    facebook_api_key: Optional[str] = Field(None, env="FACEBOOK_API_KEY")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()