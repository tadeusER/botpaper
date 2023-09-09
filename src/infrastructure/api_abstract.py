from abc import ABC, abstractmethod
from typing import List, Union

from models.api_model import APIErrorResponse, APIResponse, APISuccessResponse

class APIExtraction(ABC):

    @abstractmethod
    def search(self, queries, search_types, operators=None) -> APIResponse:
        pass

    @abstractmethod
    def is_valid_search_type(self, search_type) -> bool:
        pass

    @abstractmethod
    def construct_query(self, queries, search_types, operators) -> str:
        pass

    @abstractmethod
    def is_valid_sort_value(self, value) -> bool:
        pass

    @abstractmethod
    def search_multiple_terms(self, terms) -> Union[APISuccessResponse, APIErrorResponse]:
        pass
