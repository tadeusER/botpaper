from abc import ABC
from typing import List

from models.paper_model import ArticleMetadata

class APIResponse(ABC):
    """Clase base para todas las respuestas."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

class APISuccessResponse(APIResponse):
    """Respuesta de éxito de la API."""
    def __init__(self, data: List[ArticleMetadata], status_code=200, message="Success"):
        super().__init__(status_code, message)
        self.data = data

    def __str__(self):
        articles_info = ", ".join(str(article) for article in self.data)
        return f"Success: [{articles_info}], Status Code: {self.status_code}, Message: {self.message}"

class APIErrorResponse(APIResponse):
    """Respuesta de error de la API."""
    def __init__(self, error_message, status_code=500, message="Error"):
        super().__init__(status_code, message)
        self.error_message = error_message

    def __str__(self):
        return f"Error: {self.error_message}, Status Code: {self.status_code}, Message: {self.message}"
