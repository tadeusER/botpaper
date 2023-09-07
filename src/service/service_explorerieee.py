from typing import List, Union
import requests
from infrastructure.api_abstract import APIExtraction
from models.api_model import APIResponse, APISuccessResponse, APIErrorResponse
from models.paper_model import ArticleMetadata
import math


class XploreAPI(APIExtraction):

    BASE_URL = "https://ieeexploreapi.ieee.org/api/v1/search/articles?querytext={}&format=json&apikey={}&max_records={}&start_record={}"
    valid_search_types = ["title", "author", "abstract", "year"]

    def __init__(self, api_access_key='', max_results=10):
        self.api_access_key = api_access_key
        self.max_results = max_results

    def is_valid_search_type(self, search_type):
        return search_type in self.valid_search_types

    def construct_query(self, queries, search_types, operators):
        if not all([self.is_valid_search_type(st) for st in search_types]):
            raise ValueError("Invalid search type provided.")
        combined_queries = []
        for i, (query, search_type) in enumerate(zip(queries, search_types)):
            combined_query = "{}:{}".format(search_type, query)
            combined_queries.append(combined_query)
            if i < len(queries) - 1:
                combined_queries.append(operators[i])
        return '+'.join(combined_queries)

    def search(self, queries, search_types, operators=None) -> APIResponse:
        if operators is None:
            operators = ["AND"] * (len(queries) - 1)
        try:
            constructed_query = self.construct_query(queries, search_types, operators)
            url = self.BASE_URL.format(constructed_query, self.api_access_key, self.max_results, 1)
            response = requests.get(url)
            data = response.json()

            total_records = data['total_records']
            pages = math.ceil(total_records / self.max_results)
            articles = []

            for page in range(pages):
                start_record = 1 + (page * self.max_results)
                url = self.BASE_URL.format(constructed_query, self.api_access_key, self.max_results, start_record)
                response = requests.get(url)
                page_data = response.json()
                for entry in page_data["articles"]:
                    articles.append(ArticleMetadata(
                        entry["title"],
                        entry["abstract"],
                        entry["publication_date"],
                        entry["pdf_url"]
                    ))

            return APISuccessResponse(data=articles)
        except Exception as e:
            return APIErrorResponse(error_message=str(e))
    def search_multiple_terms(self, terms) -> Union[List[APIResponse], APIErrorResponse]:
        """
        Realiza una búsqueda en la API de Xplore para cada término proporcionado y devuelve una lista de respuestas 
        de la API con la información de los artículos encontrados.

        Parámetros:
        -----------
        terms : List[str]
            Lista de términos a buscar.

        Retorna:
        --------
        Union[List[APIResponse], APIErrorResponse]
            Lista de respuestas de la API con la información de los artículos encontrados, o una respuesta 
            de error si no se encontraron resultados para ningún término.
        """
        combined_articles = []
        for term in terms:
            response = self.search([term], ["all"])  # Here ["all"] is a general search. You might want to adjust this.
            if isinstance(response, APISuccessResponse):
                combined_articles.extend(response.data)
        if combined_articles:
            return combined_articles
        else:
            return APIErrorResponse(error_message="No results found for any term.")
if __name__ == "__main__":
    api = XploreAPI(max_results=20)
    results_combined = api.search(["Machine Learning", "Smith"], ["title", "author"], ["OR"])
    if isinstance(results_combined, APISuccessResponse):
        for paper in results_combined.data:
            print(paper)
    else:
        print(f"Error: {results_combined.error_message}")
