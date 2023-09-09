import requests
from typing import List, Union
import urllib.parse
from infrastructure.api_abstract import APIExtraction

from models.api_model import APIErrorResponse, APIResponse, APISuccessResponse
from models.paper_model import ArticleMetadata

class XploreAPI(APIExtraction):
    BASE_URL = "https://ieeexploreapi.ieee.org/api/v1/search/articles?"
    VALID_PARAMETERS = [
        "abstract", "affiliation", "article_number", "article_title", "author",
        "d-au", "doi", "d-publisher", "d-pubtype", "d-year", "end_date",
        "facet", "index_terms", "isbn", "issn", "is_number", "meta_data",
        "publication_title", "publication_year", "querytext", "start_date",
        "thesaurus_terms"
    ]
    VALID_FILTERS = {
        "content_type": [
            "Books", "Conferences", "Courses", "Early Access", "Journals", 
            "Journals,Magazines", "Magazines", "Standards"
        ],
        "end_year": None,  # To be validated for number
        "open_access": ["True", "False"],
        "publication_number": None,  # To be validated for number
        "publisher": [
            "Alcatel-Lucent", "AGU", "BIAI", "CSEE", "IBM", "IEEE", "IET", 
            "MITP", "Morgan & Claypool", "SMPTE", "TUP", "VDE"
        ],
        "start_year": None  # To be validated for number
    }
    VALID_SORTING_PAGING = {
        "max_records": (1, 200),  # Range for max_records
        "sort_field": ["article_number", "article_title", "publication_title"],
        "sort_order": ["asc", "desc"],
        "start_record": None  # To be validated for number
    }
    def __init__(self, api_access_key: str):
        self.api_access_key = api_access_key
    def _validate_parameters(self, params: dict) -> bool:
        if "article_number" in params and len(params) > 1:
            return False
        # Add other validation checks as necessary
        return True
    def _validate_filters(self, filters: dict) -> bool:
        for key, value in filters.items():
            valid_values = self.VALID_FILTERS.get(key, None)
            if valid_values is None:
                continue
            if value not in valid_values:
                return False
        return True
    def _validate_sorting_paging(self, sort_paging: dict) -> bool:
        for key, value in sort_paging.items():
            valid_values = self.VALID_SORTING_PAGING.get(key, None)
            
            if key == "max_records":
                if not (self.VALID_SORTING_PAGING["max_records"][0] <= value <= self.VALID_SORTING_PAGING["max_records"][1]):
                    return False
            elif valid_values is None:
                continue
            elif isinstance(valid_values, list) and value not in valid_values:
                return False
        return True
    def search(self, queries, search_types, operators=None)->APIResponse:
        try:
            constructed_query = self.construct_query(queries, search_types, operators)
            response = requests.get(constructed_query)
            response = response.json()
            articles = []
            for item in response["articles"]:
                try:
                    article = ArticleMetadata(
                        title=item["title"],
                        summary=item["abstract"],
                        published=item["publication_date"],
                        link=item["html_url"]  # Asume que el DOI puede ser utilizado como enlace, modifica según sea necesario
                    )
                    articles.append(article)
                except Exception as e:
                    print(f"Error mapping article: {str(e)}")
                    

            return APISuccessResponse(data=articles)
        except Exception as e:
            return APIErrorResponse(error_message=str(e))
    
    def is_valid_search_type(self, search_type) -> bool:
        # Implement the logic to determine if the given search_type is valid for IEEE Xplore API
        valid_search_types = ["some_valid_type1", "some_valid_type2"]  # Replace with actual valid types
        return search_type in valid_search_types
    def form_boolean_query(self, x: str, y: str, operator: str) -> str:
        """
        Forms a boolean query string for the provided terms and operator.

        Args:
        - x: First term.
        - y: Second term.
        - operator: Boolean operator (AND, OR, NOT).

        Returns:
        - Formed query string.
        """
        if operator not in ["AND", "OR", "NOT"]:
            raise ValueError("Invalid boolean operator. Use AND, OR, or NOT.")
        
        # URL encode the terms
        x_encoded = urllib.parse.quote(x)
        y_encoded = urllib.parse.quote(y)

        return f"({x_encoded}{operator}{y_encoded})"
    
    def search_with_boolean(self, x: str, y: str, operator: str, filters: dict = None, sorting_paging: dict = None) -> str:
        boolean_query = self.form_boolean_query(x, y, operator)
        
        parameters = {"querytext": boolean_query}
        return self.construct_query(parameters, filters, sorting_paging)
    def construct_query(self, parameters: dict, filters: dict = None, sorting_paging: dict = None) -> str:
        if not self._validate_parameters(parameters):
            raise ValueError("Invalid combination of parameters.")
        if filters and not self._validate_filters(filters):
            raise ValueError("Invalid filter values.")
        if sorting_paging and not self._validate_sorting_paging(sorting_paging):
            raise ValueError("Invalid sorting or paging values.")
        
        # Convert parameters, filters, and sorting/paging dictionary to URL format
        url_parts = [f"{key}={value}" for key, value in parameters.items()]
        if filters:
            url_parts.extend([f"{key}={value}" for key, value in filters.items()])
        if sorting_paging:
            url_parts.extend([f"{key}={value}" for key, value in sorting_paging.items()])
        
        # Adding the API key to the parameters
        url_parts.append(f"apikey={self.api_access_key}")
        
        return self.BASE_URL + '&'.join(url_parts)

    def is_valid_sort_value(self, value) -> bool:
        # Implement the logic to determine if the given sort value is valid for IEEE Xplore API
        valid_sort_values = ["some_valid_value1", "some_valid_value2"]  # Replace with actual valid values
        return value in valid_sort_values
    def search_multiple_terms(self, terms: List[str]) -> Union[APISuccessResponse, APIErrorResponse]:
        responses = []
        for term in terms:
            query_parameters = {"querytext": term}  # Assuming the term is the main query text
            response = self.search(query_parameters, {}, {})  # Assuming the latter two are empty dictionaries
            if isinstance(response, APISuccessResponse):
                responses.extend(response.data)
        if responses:
            return APISuccessResponse(data=responses)
        else:
            return APIErrorResponse(error_message="No results found for any term.")
if __name__ == "__main__":
    # Replace this with your actual API key
    YOUR_API_KEY = "api key test"
    
    explorer = XploreAPI(YOUR_API_KEY)

    # Let's define multiple search terms
    terms_to_search = ["robot", "IA", "automation", "machine learning"]

    # Using the search_multiple_terms method
    responses = explorer.search_multiple_terms(terms_to_search)

    # Display the results
    for term, response in zip(terms_to_search, responses):
        print(f"Search Results for '{term}':\n", response)