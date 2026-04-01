from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "ok"
    data: T


class PageData(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int = 1
    page_size: int = 20


class IdStatusResponse(BaseModel):
    id: str
    status: str


class ArchitectureNode(BaseModel):
    name: str
    type: str
    description: str


class ArchitectureOverview(BaseModel):
    hub: ArchitectureNode
    layers: list[ArchitectureNode]
    modules: list[str]
    agents: list[str]
