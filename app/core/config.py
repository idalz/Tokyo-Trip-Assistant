"""
Configuration management for Tokyo Trip Assistant.
Handles environment variables and application settings using Pydantic.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr
from typing import Optional, List
from functools import lru_cache
from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class Settings(BaseSettings):
    """Tokyo Trip Assistant configuration settings."""

    # Environment
    environment: Environment = Field(default=Environment.DEVELOPMENT, description="Runtime environment")
    debug: bool = Field(default=True, description="Debug mode")

    # Server
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")

    # Application
    app_name: str = Field(default="Tokyo Trip Assistant", description="Application name")
    version: str = Field(default="0.1.0", description="Application version")
    description: str = Field(default="A conversational AI travel guide for Tokyo", description="App description")

    # API Keys
    openai_api_key: Optional[SecretStr] = Field(default=None, description="OpenAI API key")
    pinecone_api_key: Optional[SecretStr] = Field(default=None, description="Pinecone API key")
    openweather_api_key: Optional[SecretStr] = Field(default=None, description="OpenWeather API key")

    # Pinecone
    pinecone_index_name: str = Field(default="your-pinecone-index", description="Pinecone index name")
    pinecone_namespace: str = Field(default="your-app-namespace", description="Pinecone namespace for organizing data")
    pinecone_environment: str = Field(default="aws-us-east-1", description="Pinecone environment")
    pinecone_cloud: str = Field(default="aws", description="Pinecone cloud provider")
    pinecone_region: str = Field(default="us-east-1", description="Pinecone region")

    # CORS
    cors_origins: List[str] = Field(default=["*"], description="CORS allowed origins")

    @property
    def APP_NAME(self) -> str:
        return self.app_name

    @property
    def VERSION(self) -> str:
        return self.version

    @property
    def DESCRIPTION(self) -> str:
        return self.description

    @property
    def DEBUG(self) -> bool:
        return self.debug

    @property
    def HOST(self) -> str:
        return self.host

    @property
    def PORT(self) -> int:
        return self.port

    @property
    def OPENAI_API_KEY(self) -> Optional[str]:
        return self.openai_api_key.get_secret_value() if self.openai_api_key else None

    @property
    def PINECONE_API_KEY(self) -> Optional[str]:
        return self.pinecone_api_key.get_secret_value() if self.pinecone_api_key else None

    @property
    def OPENWEATHER_API_KEY(self) -> Optional[str]:
        return self.openweather_api_key.get_secret_value() if self.openweather_api_key else None

    @property
    def PINECONE_INDEX_NAME(self) -> str:
        return self.pinecone_index_name

    @property
    def PINECONE_ENVIRONMENT(self) -> str:
        return self.pinecone_environment

    @property
    def PINECONE_CLOUD(self) -> str:
        return self.pinecone_cloud

    @property
    def PINECONE_REGION(self) -> str:
        return self.pinecone_region

    @property
    def PINECONE_NAMESPACE(self) -> str:
        return self.pinecone_namespace

    @property
    def CORS_ORIGINS(self) -> List[str]:
        return self.cors_origins

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="",
        validate_assignment=True,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()