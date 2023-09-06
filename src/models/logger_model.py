import logging

class LoggerConfig:
    def __init__(self, name: str, log_file: str, log_level: int = logging.INFO):
        """Inicializa el configurador del logger.

        Args:
        - name (str): Nombre del logger.
        - log_file (str): Ruta del archivo donde se guardarán los logs.
        - log_level (int, optional): Nivel de logging. Por defecto es logging.INFO.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Configura el handler para escribir logs en un archivo
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

        # Configura el handler para mostrar logs en la consola
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(stream_handler)

    def get_logger(self):
        """Retorna el logger configurado."""
        return self.logger