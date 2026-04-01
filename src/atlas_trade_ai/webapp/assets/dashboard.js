import {
  getAgentRuns,
  getScenarios,
  getWorkbench,
  runScenario,
} from "./api.js";

function renderKpis(summary) {
  const kpis = [
    ["客户数", summary.customer_count],
    ["订单数", summary.order_count],
    ["待处理任务", summary.pending_task_count],
    ["Agent 运行次数", summary.agent_run_count],
  ];
  document.querySelector("#kpis").innerHTML = kpis
    .map(
      ([label, value]) => `
      <div class="kpi-card">
        <div class="label">${label}</div>
        <div class="value">${value}</div>
      </div>
    `
    )
    .join("");
}

function renderProcessMap() {
  const nodes = [
    ["客户经营层", "Sales + CRM"],
    ["订单中枢层", "Order Core"],
    ["履约推进层", "Follow-up"],
    ["供应链执行层", "Supply Chain"],
    ["交付与合规层", "Logistics + Customs"],
    ["资金结算层", "Finance"],
    ["售后服务层", "Customer Service"],
  ];
  document.querySelector("#process-map").innerHTML = nodes
    .map(
      ([layer, title], index) => `
      <div class="process-node ${index === 1 ? "current" : ""}">
        <div class="node-layer">${layer}</div>
        <div class="node-title">${title}</div>
        <div class="node-desc">订单事件在这一层被识别、处理或推进。</div>
      </div>
    `
    )
    .join("");
}

function renderList(selector, items, renderItem) {
  document.querySelector(selector).innerHTML = items.map(renderItem).join("");
}

async function loadDashboard() {
  const [summary, runs, scenarios] = await Promise.all([
    getWorkbench(),
    getAgentRuns(),
    getScenarios(),
  ]);
  renderKpis(summary);
  renderProcessMap();
  renderList(
    "#high-risk-orders",
    summary.high_risk_orders,
    (item) => `
      <div class="list-card">
        <h3>${item.order_no}</h3>
        <p>${item.current_status || ""} / 风险等级 ${item.risk_level || "-"}</p>
      </div>
    `
  );
  renderList(
    "#recent-agent-runs",
    runs.slice(0, 6),
    (item) => `
      <div class="list-card">
        <h3>${item.agent_name}</h3>
        <p>订单 ${item.order_id || "-"} / 事件 ${item.trigger_event_type}</p>
      </div>
    `
  );
  document.querySelector("#scenario-list").innerHTML = scenarios
    .map(
      (item) => `
      <div class="scenario-item">
        <div>
          <strong>${item.name}</strong>
          <div>${item.description}</div>
        </div>
        <button data-scenario="${item.code}">运行场景</button>
      </div>
    `
    )
    .join("");

  document.querySelectorAll("[data-scenario]").forEach((button) => {
    button.addEventListener("click", async () => {
      const result = await runScenario(button.dataset.scenario);
      document.querySelector("#scenario-result").textContent = JSON.stringify(result, null, 2);
      await loadDashboard();
    });
  });
}

document.querySelector("#refresh-dashboard").addEventListener("click", loadDashboard);
loadDashboard();
