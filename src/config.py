"""Configuración centralizada de la aplicación.

Carga y valida las variables de entorno necesarias usando pydantic-settings.
Falla con un error descriptivo al arrancar si falta alguna variable crítica.
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Esquema de configuración de la aplicación.

    Las credenciales de AWS (access_key_id, secret_access_key) son opcionales.
    Si no están presentes, boto3 usa la cadena de credenciales (env vars,
    .aws/credentials, IAM role, instance profile, etc.).
    El bucket S3 sigue siendo obligatorio.
    """

    app_env: str = "local"

    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_default_region: str = "us-east-1"
    aws_s3_bucket: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
