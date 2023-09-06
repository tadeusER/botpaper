from typing import List
from typing import Any
from dataclasses import dataclass
import json

@dataclass
class Asset:
    id: str
    mimeType: str
    fileName: str
    fileSizeBytes: int
    smallThumbnail: SmallThumbnail
    mediumThumbnail: MediumThumbnail
    largeThumbnail: LargeThumbnail
    original: Original

    @staticmethod
    def from_dict(obj: Any) -> 'Asset':
        _id = str(obj.get("id"))
        _mimeType = str(obj.get("mimeType"))
        _fileName = str(obj.get("fileName"))
        _fileSizeBytes = int(obj.get("fileSizeBytes"))
        _smallThumbnail = SmallThumbnail.from_dict(obj.get("smallThumbnail"))
        _mediumThumbnail = MediumThumbnail.from_dict(obj.get("mediumThumbnail"))
        _largeThumbnail = LargeThumbnail.from_dict(obj.get("largeThumbnail"))
        _original = Original.from_dict(obj.get("original"))
        return Asset(_id, _mimeType, _fileName, _fileSizeBytes, _smallThumbnail, _mediumThumbnail, _largeThumbnail, _original)

@dataclass
class Author:
    orcid: str
    title: str
    firstName: str
    lastName: str
    institutions: List[Institution]

    @staticmethod
    def from_dict(obj: Any) -> 'Author':
        _orcid = str(obj.get("orcid"))
        _title = str(obj.get("title"))
        _firstName = str(obj.get("firstName"))
        _lastName = str(obj.get("lastName"))
        _institutions = [Institution.from_dict(y) for y in obj.get("institutions")]
        return Author(_orcid, _title, _firstName, _lastName, _institutions)

@dataclass
class BannerAsset:
    id: str
    mimeType: str
    fileName: str
    fileSizeBytes: int
    smallThumbnail: SmallThumbnail
    mediumThumbnail: MediumThumbnail
    largeThumbnail: LargeThumbnail
    original: Original

    @staticmethod
    def from_dict(obj: Any) -> 'BannerAsset':
        _id = str(obj.get("id"))
        _mimeType = str(obj.get("mimeType"))
        _fileName = str(obj.get("fileName"))
        _fileSizeBytes = int(obj.get("fileSizeBytes"))
        _smallThumbnail = SmallThumbnail.from_dict(obj.get("smallThumbnail"))
        _mediumThumbnail = MediumThumbnail.from_dict(obj.get("mediumThumbnail"))
        _largeThumbnail = LargeThumbnail.from_dict(obj.get("largeThumbnail"))
        _original = Original.from_dict(obj.get("original"))
        return BannerAsset(_id, _mimeType, _fileName, _fileSizeBytes, _smallThumbnail, _mediumThumbnail, _largeThumbnail, _original)

@dataclass
class Category:
    id: str
    name: str
    description: str

    @staticmethod
    def from_dict(obj: Any) -> 'Category':
        _id = str(obj.get("id"))
        _name = str(obj.get("name"))
        _description = str(obj.get("description"))
        return Category(_id, _name, _description)

@dataclass
class ContentType:
    id: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'ContentType':
        _id = str(obj.get("id"))
        _name = str(obj.get("name"))
        return ContentType(_id, _name)

@dataclass
class Event:
    id: str
    eventGroup: EventGroup
    title: str
    description: str
    location: str
    startDate: str
    endDate: str
    createdAt: str
    updatedAt: str
    bannerAsset: BannerAsset
    sponsors: List[Sponsor]
    url: str
    status: str

    @staticmethod
    def from_dict(obj: Any) -> 'Event':
        _id = str(obj.get("id"))
        _eventGroup = EventGroup.from_dict(obj.get("eventGroup"))
        _title = str(obj.get("title"))
        _description = str(obj.get("description"))
        _location = str(obj.get("location"))
        _startDate = str(obj.get("startDate"))
        _endDate = str(obj.get("endDate"))
        _createdAt = str(obj.get("createdAt"))
        _updatedAt = str(obj.get("updatedAt"))
        _bannerAsset = BannerAsset.from_dict(obj.get("bannerAsset"))
        _sponsors = [Sponsor.from_dict(y) for y in obj.get("sponsors")]
        _url = str(obj.get("url"))
        _status = str(obj.get("status"))
        return Event(_id, _eventGroup, _title, _description, _location, _startDate, _endDate, _createdAt, _updatedAt, _bannerAsset, _sponsors, _url, _status)

@dataclass
class EventGroup:
    id: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'EventGroup':
        _id = str(obj.get("id"))
        _name = str(obj.get("name"))
        return EventGroup(_id, _name)

@dataclass
class Funder:
    funderId: str
    name: str
    grantNumber: str
    url: str
    title: str

    @staticmethod
    def from_dict(obj: Any) -> 'Funder':
        _funderId = str(obj.get("funderId"))
        _name = str(obj.get("name"))
        _grantNumber = str(obj.get("grantNumber"))
        _url = str(obj.get("url"))
        _title = str(obj.get("title"))
        return Funder(_funderId, _name, _grantNumber, _url, _title)

@dataclass
class Institution:
    name: str
    country: str
    rorId: str

    @staticmethod
    def from_dict(obj: Any) -> 'Institution':
        _name = str(obj.get("name"))
        _country = str(obj.get("country"))
        _rorId = str(obj.get("rorId"))
        return Institution(_name, _country, _rorId)

@dataclass
class Item:
    id: str
    doi: str
    vor: str
    title: str
    abstract: str
    contentType: ContentType
    categories: List[Category]
    subject: Subject
    event: Event
    status: str
    statusDate: str
    funders: List[Funder]
    authors: List[Author]
    metrics: List[Metric]
    version: str
    versionRefs: List[VersionRef]
    submittedDate: str
    publishedDate: str
    approvedDate: str
    keywords: List[str]
    hasCompetingInterests: bool
    competingInterestsDeclaration: str
    gainedEthicsApproval: str
    suppItems: List[object]
    asset: Asset
    license: License
    webLinks: List[object]
    origin: str
    termsAcceptance: bool
    versionNote: str
    latestComments: List[object]
    commentsCount: int
    isLatestVersion: bool
    legacyId: str

    @staticmethod
    def from_dict(obj: Any) -> 'Item':
        _id = str(obj.get("id"))
        _doi = str(obj.get("doi"))
        _vor = str(obj.get("vor"))
        _title = str(obj.get("title"))
        _abstract = str(obj.get("abstract"))
        _contentType = ContentType.from_dict(obj.get("contentType"))
        _categories = [Category.from_dict(y) for y in obj.get("categories")]
        _subject = Subject.from_dict(obj.get("subject"))
        _event = Event.from_dict(obj.get("event"))
        _status = str(obj.get("status"))
        _statusDate = str(obj.get("statusDate"))
        _funders = [Funder.from_dict(y) for y in obj.get("funders")]
        _authors = [Author.from_dict(y) for y in obj.get("authors")]
        _metrics = [Metric.from_dict(y) for y in obj.get("metrics")]
        _version = str(obj.get("version"))
        _versionRefs = [VersionRef.from_dict(y) for y in obj.get("versionRefs")]
        _submittedDate = str(obj.get("submittedDate"))
        _publishedDate = str(obj.get("publishedDate"))
        _approvedDate = str(obj.get("approvedDate"))
        _keywords = [.from_dict(y) for y in obj.get("keywords")]
        _hasCompetingInterests = 
        _competingInterestsDeclaration = str(obj.get("competingInterestsDeclaration"))
        _gainedEthicsApproval = str(obj.get("gainedEthicsApproval"))
        _suppItems = [.from_dict(y) for y in obj.get("suppItems")]
        _asset = Asset.from_dict(obj.get("asset"))
        _license = License.from_dict(obj.get("license"))
        _webLinks = [.from_dict(y) for y in obj.get("webLinks")]
        _origin = str(obj.get("origin"))
        _termsAcceptance = 
        _versionNote = str(obj.get("versionNote"))
        _latestComments = [.from_dict(y) for y in obj.get("latestComments")]
        _commentsCount = int(obj.get("commentsCount"))
        _isLatestVersion = 
        _legacyId = str(obj.get("legacyId"))
        return Item(_id, _doi, _vor, _title, _abstract, _contentType, _categories, _subject, _event, _status, _statusDate, _funders, _authors, _metrics, _version, _versionRefs, _submittedDate, _publishedDate, _approvedDate, _keywords, _hasCompetingInterests, _competingInterestsDeclaration, _gainedEthicsApproval, _suppItems, _asset, _license, _webLinks, _origin, _termsAcceptance, _versionNote, _latestComments, _commentsCount, _isLatestVersion, _legacyId)

@dataclass
class ItemHit:
    item: Item

    @staticmethod
    def from_dict(obj: Any) -> 'ItemHit':
        _item = Item.from_dict(obj.get("item"))
        return ItemHit(_item)

@dataclass
class LargeThumbnail:
    url: str

    @staticmethod
    def from_dict(obj: Any) -> 'LargeThumbnail':
        _url = str(obj.get("url"))
        return LargeThumbnail(_url)

@dataclass
class License:
    id: str
    name: str
    description: str
    url: str

    @staticmethod
    def from_dict(obj: Any) -> 'License':
        _id = str(obj.get("id"))
        _name = str(obj.get("name"))
        _description = str(obj.get("description"))
        _url = str(obj.get("url"))
        return License(_id, _name, _description, _url)

@dataclass
class MediumThumbnail:
    url: str

    @staticmethod
    def from_dict(obj: Any) -> 'MediumThumbnail':
        _url = str(obj.get("url"))
        return MediumThumbnail(_url)

@dataclass
class Metric:
    description: str
    value: int

    @staticmethod
    def from_dict(obj: Any) -> 'Metric':
        _description = str(obj.get("description"))
        _value = int(obj.get("value"))
        return Metric(_description, _value)

@dataclass
class Original:
    url: str

    @staticmethod
    def from_dict(obj: Any) -> 'Original':
        _url = str(obj.get("url"))
        return Original(_url)

@dataclass
class CambrigeResponse:
    totalCount: int
    itemHits: List[ItemHit]

    @staticmethod
    def from_dict(obj: Any) -> 'CambrigeResponse':
        _totalCount = int(obj.get("totalCount"))
        _itemHits = [ItemHit.from_dict(y) for y in obj.get("itemHits")]
        return CambrigeResponse(_totalCount, _itemHits)

@dataclass
class SmallThumbnail:
    url: str

    @staticmethod
    def from_dict(obj: Any) -> 'SmallThumbnail':
        _url = str(obj.get("url"))
        return SmallThumbnail(_url)

@dataclass
class Sponsor:
    id: str
    url: str
    text: str
    asset: Asset

    @staticmethod
    def from_dict(obj: Any) -> 'Sponsor':
        _id = str(obj.get("id"))
        _url = str(obj.get("url"))
        _text = str(obj.get("text"))
        _asset = Asset.from_dict(obj.get("asset"))
        return Sponsor(_id, _url, _text, _asset)

@dataclass
class Subject:
    id: str
    name: str
    description: str

    @staticmethod
    def from_dict(obj: Any) -> 'Subject':
        _id = str(obj.get("id"))
        _name = str(obj.get("name"))
        _description = str(obj.get("description"))
        return Subject(_id, _name, _description)

@dataclass
class VersionRef:
    version: str
    itemId: str
    legacyId: str

    @staticmethod
    def from_dict(obj: Any) -> 'VersionRef':
        _version = str(obj.get("version"))
        _itemId = str(obj.get("itemId"))
        _legacyId = str(obj.get("legacyId"))
        return VersionRef(_version, _itemId, _legacyId)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# CambrigeResponse = CambrigeResponse.from_dict(jsonstring)
