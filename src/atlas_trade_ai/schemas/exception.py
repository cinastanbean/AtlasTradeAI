from __future__ import annotations

from pydantic import BaseModel


class ExceptionCreateRequest(BaseModel):
    exception_type: str
    exception_level: str
    related_order_id: str | None = None
    source_event_id: str | None = None
    owner_id: str | None = None
    suggestion: str | None = None


class ExceptionRead(BaseModel):
    exception_id: str
    exception_type: str
    exception_level: str
    related_order_id: str | None = None
    exception_status: str
