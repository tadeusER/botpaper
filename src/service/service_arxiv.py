import urllib.parse
import urllib.request
import feedparser

class ArxivAPI:
    """
    Clase que proporciona una interfaz para buscar artículos en el repositorio de arXiv.

    Args:
        max_results (int): El número máximo de resultados que se deben devolver por búsqueda.

    Attributes:
        BASE_URL (str): La URL base para la API de arXiv.
        valid_search_types (list): Una lista de tipos de búsqueda válidos.
    
    Methods:
        is_valid_search_type(search_type): Comprueba si un tipo de búsqueda es válido.
        construct_query(queries, search_types, operators): Construye una consulta de búsqueda a partir de una lista de consultas, tipos de búsqueda y operadores.
        search(queries, search_types, operators): Realiza una búsqueda en el repositorio de arXiv y devuelve una lista de artículos que coinciden con la consulta.

    """

    BASE_URL = ("http://export.arxiv.org/api/query?"
                "search_query={}&sortBy=lastUpdatedDate&sortOrder=ascending&max_results={}")
    valid_search_types = ["ti", "au", "abs", "co", "jr", "cat", "rn", "id", "all"]

    def __init__(self, max_results=10):
        """
        Inicializa una nueva instancia de la clase ArxivAPI.

        Args:
            max_results (int): El número máximo de resultados que se deben devolver por búsqueda.
        """
        self.max_results = max_results

    def is_valid_search_type(self, search_type):
        """
        Comprueba si un tipo de búsqueda es válido.

        Args:
            search_type (str): El tipo de búsqueda a comprobar.

        Returns:
            bool: True si el tipo de búsqueda es válido, False en caso contrario.
        """
        return search_type in self.valid_search_types

    def construct_query(self, queries, search_types, operators):
        """
        Construye una consulta de búsqueda a partir de una lista de consultas, tipos de búsqueda y operadores.

        Args:
            queries (list): Una lista de consultas de búsqueda.
            search_types (list): Una lista de tipos de búsqueda correspondientes a las consultas.
            operators (list): Una lista de operadores booleanos que se utilizarán para combinar las consultas.

        Returns:
            str: La consulta de búsqueda construida.
        
        Raises:
            ValueError: Si se proporciona un tipo de búsqueda no válido.
        """
        if not all([self.is_valid_search_type(st) for st in search_types]):
            raise ValueError("Invalid search type provided.")

        # Convert queries and search_types to lowercase.
        queries = [q.lower() for q in queries]
        search_types = [st.lower() for st in search_types]

        combined_queries = []
        for i, (query, search_type) in enumerate(zip(queries, search_types)):
            combined_query = "{}:{}".format(search_type, query)
            combined_queries.append(combined_query)

            if i < len(queries) - 1:
                combined_queries.append(operators[i])
        
        return '+'.join(combined_queries)

    def search(self, queries, search_types, operators=None):
        """
        Realiza una búsqueda en el repositorio de arXiv y devuelve una lista de artículos que coinciden con la consulta.

        Args:
            queries (list): Una lista de consultas de búsqueda.
            search_types (list): Una lista de tipos de búsqueda correspondientes a las consultas.
            operators (list): Una lista de operadores booleanos que se utilizarán para combinar las consultas. Por defecto, se utiliza "AND" para todas las combinaciones.

        Returns:
            list: Una lista de diccionarios que representan los artículos que coinciden con la consulta. Cada diccionario contiene los siguientes campos: "title", "summary", "published" y "link".
        
        Raises:
            ValueError: Si se proporciona un tipo de búsqueda no válido.
        """
        if operators is None:
            operators = ["AND"] * (len(queries) - 1)
        constructed_query = self.construct_query(queries, search_types, operators)
        url = self.BASE_URL.format(constructed_query, self.max_results)
        response = urllib.request.urlopen(url)
        feed = feedparser.parse(response.read().decode('utf-8'))

        articles = []
        for entry in feed.entries:
            articles.append({
                "title": entry.title,
                "summary": entry.summary,
                "published": entry.published,
                "link": entry.link
            })
        
        return articles

if __name__ == "__main__":
    api = ArxivAPI(max_results=20)

    # Example of combining author and title search
    results_combined = api.search(["Rovs", "AUV"], ["all", "all"], ["OR"])
    for paper in results_combined:
        print(paper)