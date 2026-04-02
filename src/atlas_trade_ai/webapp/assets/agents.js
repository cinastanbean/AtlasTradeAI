import {
  getAgentCatalog,
  getAgentMonitor,
  getAgentRunDetail,
  getAgentRuns,
  getFilteredAgentRuns,
} from "./api.js";

async function renderAgents(filters = {}) {
  const [catalog, runs, monitor] = await Promise.all([
    getAgentCatalog(),
    Object.keys(filters).length ? getFilteredAgentRuns(filters) : getAgentRuns(),
    getAgentMonitor(),
  ]);
  const kpis = [
    ["Agent 总数", monitor.agent_count],
    ["活跃 Agent", monitor.active_agent_count],
    ["累计运行记录", monitor.latest_runs.length],
  ];
  document.querySelector("#agent-kpis").innerHTML = kpis
    .map(
      ([label, value]) => `
      <div class="kpi-card">
        <div class="label">${label}</div>
        <div class="value">${value}</div>
      </div>
    `
    )
    .join("");

  document.querySelector("#agent-catalog").innerHTML = catalog
    .map(
      (item) => `
      <div class="list-card">
        <h3>${item.name}</h3>
        <p>Agent Key: ${item.agent_key}</p>
        <p>层级: ${item.layer}</p>
        <p>运行模式: ${item.execution_mode || "-"}</p>
        <p>智能类型: ${item.intelligence_type || "-"}</p>
        <p>订阅事件: ${(item.subscribed_events || []).join(" / ")}</p>
        <p>职责: ${item.description || "待补充"}</p>
      </div>
    `
    )
    .join("");

  document.querySelector("#agent-runs").innerHTML = runs
    .map(
      (item) => `
      <div class="list-card clickable-card" data-run-id="${item.run_id}">
        <h3>${item.agent_name}</h3>
        <p>订单: ${item.order_id || "-"}</p>
        <p>事件: ${item.trigger_event_type}</p>
        <p>摘要: ${(item.output_result && item.output_result.summary) || "-"}</p>
        <p>引擎: ${(item.output_result && item.output_result.engine && item.output_result.engine.provider) || "-"}</p>
      </div>
    `
    )
    .join("");

  document.querySelectorAll("[data-run-id]").forEach((item) => {
    item.addEventListener("click", async () => {
      const detail = await getAgentRunDetail(item.dataset.runId);
      document.querySelector("#agent-run-detail").textContent = JSON.stringify(detail, null, 2);
    });
  });

  document.querySelector("#agent-performance").innerHTML = (monitor.agent_cards || [])
    .map(
      (item) => `
      <div class="list-card">
        <h3>${item.name}</h3>
        <p>运行次数: ${item.run_count}</p>
        <p>技能: ${(item.skills || []).join(" / ")}</p>
        <p>引擎来源: ${(item.engine_providers || []).join(" / ") || "-"}</p>
        <p>最近事件: ${(item.last_run && item.last_run.trigger_event_type) || "-"}</p>
      </div>
    `
    )
    .join("");
}

document.querySelector("#refresh-agents").addEventListener("click", () => renderAgents());
document.querySelector("#apply-run-filters").addEventListener("click", () =>
  renderAgents({
    agent_name: document.querySelector("#filter-agent-name").value,
    event_type: document.querySelector("#filter-event-type").value,
    order_id: document.querySelector("#filter-order-id").value,
    engine_provider: document.querySelector("#filter-engine-provider").value,
  })
);
renderAgents();
