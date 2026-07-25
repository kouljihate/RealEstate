from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    GUEST = "guest"


class PropertyStatus(str, Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    SOLD = "sold"
    WITHDRAWN = "withdrawn"


class PropertyType(str, Enum):
    FARMLAND = "farmland"
    RANCH = "ranch"
    ORCHARD = "orchard"
    VINEYARD = "vineyard"
    PASTURE = "pasture"
    MIXED_USE = "mixed_use"


class MediaType(str, Enum):
    PHOTO = "photo"
    VIDEO = "video"


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    MAD = "MAD"
    EGP = "EGP"


class ListingStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    SOLD = "sold"
    EXPIRED = "expired"
