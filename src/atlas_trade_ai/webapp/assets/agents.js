import { getAgentCatalog, getAgentRuns } from "./api.js";

async function renderAgents() {
  const [catalog, runs] = await Promise.all([getAgentCatalog(), getAgentRuns()]);
  document.querySelector("#agent-catalog").innerHTML = catalog
    .map(
      (item) => `
      <div class="list-card">
        <h3>${item.name}</h3>
        <p>Agent Key: ${item.agent_key}</p>
        <p>层级: ${item.layer}</p>
        <p>职责: ${item.description || "待补充"}</p>
      </div>
    `
    )
    .join("");

  document.querySelector("#agent-runs").innerHTML = runs
    .map(
      (item) => `
      <div class="list-card">
        <h3>${item.agent_name}</h3>
        <p>订单: ${item.order_id || "-"}</p>
        <p>事件: ${item.trigger_event_type}</p>
        <p>摘要: ${(item.output_result && item.output_result.summary) || "-"}</p>
      </div>
    `
    )
    .join("");
}

document.querySelector("#refresh-agents").addEventListener("click", renderAgents);
renderAgents();
