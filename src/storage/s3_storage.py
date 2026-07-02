"""Wrapper de infraestructura para AWS S3.

Encapsula todas las operaciones de red con boto3, aislando al resto del proyecto
de la SDK de AWS. Ninguna otra capa debe importar boto3 directamente.
"""

import boto3
import json
import logging
from botocore.exceptions import ClientError
from src.config import settings


class S3StorageService:
    """Cliente de S3 para leer y escribir el historial de gastos.

    Gestiona la conexión con AWS usando las credenciales inyectadas desde
    las variables de entorno a través de `config.py`. Todas las operaciones
    manejan sus excepciones de forma granular para que la capa superior
    reciba resultados predecibles sin exponer detalles de la SDK.
    """

    def __init__(self) -> None:
        """Inicializa el cliente boto3 con las credenciales del entorno.

        Las credenciales se leen desde `settings` (pydantic-settings), que a su vez
        las obtiene del archivo `.env`. Si alguna variable crítica falta, `Settings`
        lanza un error en el arranque de la aplicación.
        """
        self.botoClient = boto3.client(
            "s3",
            region_name=settings.aws_default_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )

    def read_file(self) -> list:
        """Lee y deserializa el historial de gastos desde S3.

        Descarga el objeto `historial.json` del bucket configurado, lo decodifica
        como UTF-8 y lo parsea como JSON.

        Returns:
            list[dict]: Lista de gastos deserializada. Retorna `[]` si el objeto
                no existe en S3 (`NoSuchKey`).

        Raises:
            ClientError: Re-lanza cualquier error de AWS que no sea `NoSuchKey`
                (ej: `AccessDenied`, throttling), para que la capa superior
                pueda manejarlo o loguearlo.
        """
        try:
            file = self.botoClient.get_object(
                Bucket=settings.aws_s3_bucket, Key="historial.json"
            )
            object_content = file["Body"].read().decode("utf-8")
            return json.loads(object_content)
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return []
            logging.error(f"Error al leer historial.json desde S3: {e}")
            raise e

    def save_file(self, data: list) -> bool:
        """Serializa y sube el historial de gastos a S3.

        Convierte `data` a JSON con indentación de 4 espacios y lo sube como
        `historial.json` usando `put_object`, que opera completamente en memoria
        sin escribir archivos temporales en disco.

        Args:
            data (list[dict]): Lista completa de gastos a persistir. Sobreescribe
                completamente el objeto existente en S3.

        Returns:
            bool: `True` si la operación fue exitosa, `False` si hubo un error
                de AWS (el error se logea antes de retornar).
        """
        try:
            json_string = json.dumps(data, indent=4)
            self.botoClient.put_object(
                Bucket=settings.aws_s3_bucket,
                Key="historial.json",
                Body=json_string,
                ContentType="application/json",
            )
            return True
        except ClientError as e:
            logging.error(f"Error al guardar historial.json en S3: {e}")
            return False
