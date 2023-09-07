"""
Módulo que contiene la implementación de la clase ArxivAPI, que permite realizar búsquedas en el repositorio de artículos científicos arXiv.

La clase ArxivAPI implementa la interfaz APIExtraction y proporciona los siguientes métodos públicos:
- is_valid_search_type(search_type): verifica si un tipo de búsqueda es válido.
- construct_query(queries, search_types, operators): construye una consulta a partir de una lista de términos de búsqueda, tipos de búsqueda y operadores.
- search(queries, search_types, operators=None): realiza una búsqueda en arXiv a partir de una lista de términos de búsqueda, tipos de búsqueda y operadores.
- search_multiple_terms(terms): realiza una búsqueda en arXiv a partir de una lista de términos de búsqueda, combinando los resultados.
- is_valid_sort_value(value): verifica si un valor de ordenación es válido.

Además, el módulo define las siguientes clases:
- APIResponse: clase base para las respuestas de la API.
- APISuccessResponse(APIResponse): clase para las respuestas exitosas de la API.
- APIErrorResponse(APIResponse): clase para las respuestas de error de la API.
"""

from typing import List, Union
import urllib.parse
import urllib.request
import feedparser
from infrastructure.api_abstract import APIExtraction
from models.api_model import APIResponse, APISuccessResponse, APIErrorResponse
from models.paper_model import ArticleMetadata

class ArxivAPI(APIExtraction):
    """
    Clase que representa una API para extraer información de artículos científicos de arXiv.

    Atributos:
    ----------
    BASE_URL : str
        URL base de la API.
    valid_search_types : List[str]
        Lista de tipos de búsqueda válidos.
    max_results : int
        Número máximo de resultados a obtener por búsqueda.
    """

    BASE_URL = ("http://export.arxiv.org/api/query?"
                "search_query={}&sortBy=lastUpdatedDate&sortOrder=ascending&max_results={}")
    valid_search_types = ["ti", "au", "abs", "co", "jr", "cat", "rn", "id", "all"]

    def __init__(self, max_results=10):
        self.max_results = max_results

    def is_valid_search_type(self, search_type):
        """_summary_
        Verifica si el tipo de búsqueda proporcionado es válido.

        Parámetros:
        -----------
        search_type : str
            Tipo de búsqueda a verificar.

        Retorna:
        --------
        bool
            True si el tipo de búsqueda es válido, False en caso contrario.
        """
        return search_type in self.valid_search_types

    def construct_query(self, queries, search_types, operators):
        """_summary_
        Construye una consulta para la API de arXiv a partir de las consultas, tipos de búsqueda y operadores proporcionados.

        Parámetros:
        -----------
        queries : List[str]
            Lista de consultas a realizar.
        search_types : List[str]
            Lista de tipos de búsqueda correspondientes a cada consulta.
        operators : List[str]
            Lista de operadores a utilizar entre cada consulta.

        Retorna:
        --------
        str
            Consulta construida a partir de las consultas, tipos e búsqueda y operadores proporcionados.
        """
        if not all([self.is_valid_search_type(st) for st in search_types]):
            raise ValueError("Invalid search type provided.")
        queries = [q.lower() for q in queries]
        search_types = [st.lower() for st in search_types]
        combined_queries = []
        for i, (query, search_type) in enumerate(zip(queries, search_types)):
            combined_query = "{}:{}".format(search_type, query)
            combined_queries.append(combined_query)
            if i < len(queries) - 1:
                combined_queries.append(operators[i])
        return '+'.join(combined_queries)

    def search(self, queries, search_types, operators=None) -> APIResponse:
        """_summary_
        Realiza una búsqueda en la API de arXiv y devuelve una respuesta de la API con la información de los artículos encontrados.

        Parámetros:
        -----------
        queries : List[str]
            Lista de consultas a realizar.
        search_types : List[str]
            Lista de tipos de búsqueda correspondientes a cada consulta.
        operators : Optional[List[str]], default=None
            Lista de operadores a utilizar entre cada consulta. Si no se proporciona, se utiliza "AND" como operador por defecto.

        Retorna:
        --------
        APIResponse
            Respuesta de la API con la información de los artículos encontrados.
        """
        if operators is None:
            operators = ["AND"] * (len(queries) - 1)
        try:
            constructed_query = self.construct_query(queries, search_types, operators)
            url = self.BASE_URL.format(constructed_query, self.max_results)
            response = urllib.request.urlopen(url)
            feed = feedparser.parse(response.read().decode('utf-8'))
            articles = []
            for entry in feed.entries:
                articles.append(ArticleMetadata(entry.title, entry.summary, entry.published, entry.link))
            return APISuccessResponse(data=articles)
        except Exception as e:
            return APIErrorResponse(error_message=str(e))

    def search_multiple_terms(self, terms) -> Union[List[APIResponse], APIErrorResponse]:
        """_summary_
        Realiza una búsqueda en la API de arXiv para cada término proporcionado y devuelve una lista de respuestas de la API con la información de los artículos encontrados.

        Parámetros:
        -----------
        terms : List[str]
            Lista de términos a buscar.

        Retorna:
        --------
        Union[List[APIResponse], APIErrorResponse]
            Lista de respuestas de la API con la información de los artículos encontrados, o una respuesta de error si no se encontraron resultados para ningún término.
        """
        combined_articles = []
        for term in terms:
            response = self.search([term], ["all"])
            if isinstance(response, APISuccessResponse):
                combined_articles.extend(response.data)
        if combined_articles:
            return combined_articles
        else:
            return APIErrorResponse(error_message="No results found for any term.")


if __name__ == "__main__":
    api = ArxivAPI(max_results=20)
    results_combined = api.search(["Rovs", "AUV"], ["all", "all"], ["OR"])
    if isinstance(results_combined, APISuccessResponse):
        for paper in results_combined.data:
            print(paper)
    else:
        print(f"Error: {results_combined.error_message}")