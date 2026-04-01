import { getOrderDashboard, getOrderProgress } from "./api.js";

const query = new URLSearchParams(window.location.search);
const orderId = query.get("order_id") || "ord_001";

function renderCards(selector, items, renderer) {
  document.querySelector(selector).innerHTML = items.map(renderer).join("") || "<p>暂无数据</p>";
}

async function renderDetail() {
  const [dashboard, progress] = await Promise.all([
    getOrderDashboard(orderId),
    getOrderProgress(orderId),
  ]);
  document.querySelector("#detail-title").textContent = `${dashboard.order.order_no} 订单详情`;
  document.querySelector("#order-progress").innerHTML = progress.stages
    .map(
      (stage) => `
      <div class="process-node ${stage.state}">
        <div class="node-layer">${stage.layer}</div>
        <div class="node-title">${stage.status}</div>
        <div>${stage.state}</div>
      </div>
    `
    )
    .join("");

  renderCards(
    "#order-events",
    dashboard.events,
    (item) => `
      <div class="list-card">
        <h4>${item.event_type}</h4>
        <p>${item.event_time || "-"}</p>
      </div>
    `
  );
  renderCards(
    "#order-tasks",
    dashboard.tasks,
    (item) => `
      <div class="list-card">
        <h4>${item.task_title}</h4>
        <p>${item.priority} / ${item.task_status}</p>
      </div>
    `
  );
  renderCards(
    "#order-exceptions",
    dashboard.exceptions,
    (item) => `
      <div class="list-card">
        <h4>${item.exception_type}</h4>
        <p>${item.exception_level} / ${item.exception_status}</p>
      </div>
    `
  );
  renderCards(
    "#order-agent-runs",
    dashboard.agent_runs,
    (item) => `
      <div class="list-card">
        <h4>${item.agent_name}</h4>
        <p>${item.trigger_event_type}</p>
      </div>
    `
  );
}

renderDetail();
