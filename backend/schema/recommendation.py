from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, ARRAY, Integer, JSON


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    address: str


class User(UserBase, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    purchases: List["PurchaseHistory"] = Relationship(back_populates="user")
    search_queries: List["SearchQuery"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None


class ItemBase(SQLModel):
    item_name: str
    category: str
    price: float
    brand: str
    color: str
    size: str
    image_url: str
    description: str


class Item(ItemBase, table=True):
    item_id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    purchases: List["PurchaseHistory"] = Relationship(back_populates="item")


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    item_id: int
    created_at: datetime
    updated_at: datetime


class ItemUpdate(SQLModel):
    item_name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None


class PurchaseHistoryBase(SQLModel):
    quantity: int
    purchase_date: datetime
    total_price: float


class PurchaseHistory(PurchaseHistoryBase, table=True):
    __tablename__ = "purchase_history"  # Add this line to specify the new table name
    purchase_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    item_id: int = Field(foreign_key="item.item_id")

    user: User = Relationship(back_populates="purchases")
    item: Item = Relationship(back_populates="purchases")


class PurchaseHistoryCreate(PurchaseHistoryBase):
    user_id: int
    item_id: int


class PurchaseHistoryRead(PurchaseHistoryBase):
    purchase_id: int
    user_id: int
    item_id: int


class SearchQueryBase(SQLModel):
    query_text: str


class SearchQuery(SearchQueryBase, table=True):
    __tablename__ = "search_query"
    query_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    result_item_ids: List[int] = Field(sa_column=Column(ARRAY(Integer)))
    # Alternatively, for non-PostgreSQL databases:
    # result_item_ids: List[int] = Field(sa_column=Column(JSON))

    user: User = Relationship(back_populates="search_queries")


class SearchQueryCreate(SearchQueryBase):
    user_id: int
    result_item_ids: List[int]


class SearchQueryRead(SearchQueryBase):
    query_id: int
    user_id: int
    created_at: datetime
    result_item_ids: List[int]
