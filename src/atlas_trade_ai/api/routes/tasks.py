from __future__ import annotations

from fastapi import APIRouter, Query

from atlas_trade_ai.container import container
from atlas_trade_ai.schemas.common import ApiResponse, PageData
from atlas_trade_ai.schemas.task import TaskCreateRequest, TaskRead, TaskStatusUpdateRequest

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", response_model=ApiResponse[TaskRead])
def create_task(request: TaskCreateRequest) -> ApiResponse[TaskRead]:
    result = container.task_service.create_task(request.model_dump())
    return ApiResponse(data=TaskRead(**result))


@router.get("", response_model=ApiResponse[PageData[TaskRead]])
def list_tasks(
    assignee_id: str | None = Query(default=None),
    status: str | None = Query(default=None),
    page: int = 1,
    page_size: int = 20,
) -> ApiResponse[PageData[TaskRead]]:
    items = [
        TaskRead(**item)
        for item in container.task_service.list_tasks(assignee_id=assignee_id, status=status)
    ]
    return ApiResponse(
        data=PageData(items=items, total=len(items), page=page, page_size=page_size)
    )


@router.post("/{task_id}/status", response_model=ApiResponse[TaskRead])
def update_task_status(task_id: str, request: TaskStatusUpdateRequest) -> ApiResponse[TaskRead]:
    result = container.task_service.update_task_status(
        task_id=task_id,
        task_status=request.task_status,
        operator=request.operator,
    )
    return ApiResponse(data=TaskRead(**result))
