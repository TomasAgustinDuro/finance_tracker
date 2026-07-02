"""Configuración centralizada de la aplicación.

Carga y valida las variables de entorno necesarias usando pydantic-settings.
Falla con un error descriptivo al arrancar si falta alguna variable crítica.
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Esquema de configuración de la aplicación.

    Todas las variables marcadas sin valor por defecto son obligatorias.
    Si no están presentes en el archivo .env o en el entorno, pydantic
    lanza un ValidationError al iniciar la aplicación.
    """

    app_env: str = "local"
    app_port: int = 8000

    aws_access_key_id: str
    aws_secret_access_key: str
    aws_default_region: str = "us-east-1"
    aws_s3_bucket: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
