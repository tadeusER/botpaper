from abc import ABC

class APIResponse(ABC):
    """Clase base para todas las respuestas."""
    pass

class APISuccessResponse(APIResponse):
    """Respuesta de éxito de la API."""
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return f"Success: {self.data}"

class APIErrorResponse(APIResponse):
    """Respuesta de error de la API."""
    def __init__(self, error_message):
        self.error_message = error_message

    def __str__(self):
        return f"Error: {self.error_message}"