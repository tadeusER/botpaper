

from models.paper_model import ArticleMetadata
from models.response_api import CambrigeResponse


def from_cambrige_response(response: CambrigeResponse) -> 'ArticleMetadata':
    if not response.itemHits or len(response.itemHits) == 0:
        raise ValueError("CambrigeResponse no tiene items")

    item = response.itemHits[0].item
    return ArticleMetadata(
        id=item.id,
        title=item.title,
        abstract=item.abstract,
        authors=item.authors,
        # ... mapea otros campos según lo necesites
    )