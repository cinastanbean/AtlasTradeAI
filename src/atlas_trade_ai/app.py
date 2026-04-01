from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from atlas_trade_ai.api.router import api_router

WEB_DIR = Path(__file__).resolve().parent / "web"
WEBAPP_DIR = Path(__file__).resolve().parent / "webapp"

app = FastAPI(
    title="AtlasTradeAI",
    version="0.1.0",
    description="Order-driven intelligent trade operating system skeleton",
)
app.include_router(api_router)
app.mount("/ui", StaticFiles(directory=WEBAPP_DIR, html=True), name="ui")


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "AtlasTradeAI",
        "message": "The engineering skeleton is running.",
    }


@app.get("/demo", response_class=HTMLResponse)
def demo() -> str:
    return """
    <html>
      <head>
        <title>AtlasTradeAI Demo</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 32px; background: #f7f7f5; color: #222; }
          h1 { margin-bottom: 8px; }
          .grid { display: grid; grid-template-columns: repeat(2, minmax(280px, 1fr)); gap: 16px; }
          .card { background: white; border-radius: 12px; padding: 16px; box-shadow: 0 2px 10px rgba(0,0,0,.06); }
          code { background: #f0f0ee; padding: 2px 6px; border-radius: 6px; }
        </style>
      </head>
      <body>
        <h1>AtlasTradeAI</h1>
        <p>这是一个订单驱动的智能贸易操作系统工程骨架演示页。</p>
        <div class="grid">
          <div class="card">
            <h3>核心入口</h3>
            <p><code>/api/overview/architecture</code></p>
            <p><code>/api/workbench/summary</code></p>
            <p><code>/api/orders</code></p>
          </div>
          <div class="card">
            <h3>事件与规则</h3>
            <p><code>/api/events</code></p>
            <p><code>/api/rules/events</code></p>
            <p><code>/api/rules/workflow</code></p>
          </div>
          <div class="card">
            <h3>Agent 与动作</h3>
            <p><code>/api/agents/follow-up/run</code></p>
            <p><code>/api/tasks</code></p>
            <p><code>/api/exceptions</code></p>
          </div>
          <div class="card">
            <h3>集成占位</h3>
            <p><code>/api/integrations</code></p>
            <p>纷享销客 CRM / 金蝶云星空 ERP / 钉钉</p>
          </div>
        </div>
      </body>
    </html>
    """


@app.get("/platform")
def platform() -> RedirectResponse:
    return RedirectResponse(url="/ui/index.html")


@app.get("/app")
def frontend_app() -> RedirectResponse:
    return RedirectResponse(url="/ui/index.html")


@app.get("/platform-legacy")
def legacy_platform() -> FileResponse:
    return FileResponse(WEB_DIR / "platform.html")
