from __future__ import annotations

from pydantic import BaseModel


class ContactRead(BaseModel):
    contact_id: str
    contact_name: str
    phone: str | None = None


class CustomerRead(BaseModel):
    customer_id: str
    customer_name: str
    customer_level: str | None = None
    business_type: str
    owner_id: str | None = None
    country_or_region: str | None = None
    payment_terms: str | None = None
    contacts: list[ContactRead] = []
