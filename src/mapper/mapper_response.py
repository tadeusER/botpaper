

from models.paper_model import ArticleMetadata
from models.response_api import CambrigeResponse
from typing import List


def from_cambrige_response(response: CambrigeResponse) -> List['ArticleMetadata']:
    if not response.itemHits:
        raise ValueError("CambrigeResponse no tiene items")

    articles = []
    for item_hit in response.itemHits:
        item = item_hit.item
        article = ArticleMetadata(
            id=item.id,
            title=item.title,
            abstract=item.abstract,
            authors=item.authors,
        )
        articles.append(article)

    return articles