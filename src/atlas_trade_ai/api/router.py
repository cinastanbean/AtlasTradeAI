from __future__ import annotations

from fastapi import APIRouter

from atlas_trade_ai.api.routes import (
    agents,
    customers,
    events,
    exceptions,
    integrations,
    notifications,
    orders,
    overview,
    rules,
    tasks,
    workbench,
)


api_router = APIRouter()
api_router.include_router(overview.router)
api_router.include_router(customers.router)
api_router.include_router(orders.router)
api_router.include_router(tasks.router)
api_router.include_router(exceptions.router)
api_router.include_router(events.router)
api_router.include_router(agents.router)
api_router.include_router(notifications.router)
api_router.include_router(workbench.router)
api_router.include_router(integrations.router)
api_router.include_router(rules.router)
