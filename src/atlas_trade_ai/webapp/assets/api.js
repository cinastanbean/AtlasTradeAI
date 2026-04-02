export async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

export async function getWorkbench() {
  return (await fetchJson("/api/workbench/summary")).data;
}

export async function getEscalations() {
  return (await fetchJson("/api/workbench/escalations")).data;
}

export async function getCompositeRisks() {
  return (await fetchJson("/api/workbench/composite-risks")).data;
}

export async function getSlaOverdue(nowIso = null) {
  const suffix = nowIso ? `?now_iso=${encodeURIComponent(nowIso)}` : "";
  return (await fetchJson(`/api/workbench/sla-overdue${suffix}`)).data;
}

export async function getOrders() {
  return (await fetchJson("/api/orders")).data.items;
}

export async function getOrderDashboard(orderId) {
  return (await fetchJson(`/api/dashboard/orders/${orderId}`)).data;
}

export async function getOrderProgress(orderId) {
  return (await fetchJson(`/api/orders/${orderId}/progress`)).data;
}

export async function getAgentCatalog() {
  return (await fetchJson("/api/agents/catalog")).data;
}

export async function getAgentMonitor() {
  return (await fetchJson("/api/agents/monitor")).data;
}

export async function getAgentRuns() {
  return (await fetchJson("/api/agent-runs")).data;
}

export async function getFilteredAgentRuns(params = {}) {
  const search = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      search.set(key, String(value));
    }
  });
  const suffix = search.toString() ? `?${search.toString()}` : "";
  return (await fetchJson(`/api/agent-runs${suffix}`)).data;
}

export async function getAgentRunDetail(runId) {
  return (await fetchJson(`/api/agent-runs/${runId}`)).data;
}

export async function getScenarios() {
  return (await fetchJson("/api/demo/scenarios")).data;
}

export async function runScenario(code) {
  return (await fetchJson(`/api/demo/scenarios/${code}/run`, { method: "POST" })).data;
}

export async function getIntegrations() {
  return (await fetchJson("/api/integrations")).data;
}

export async function getIntegrationSnapshot(system) {
  return (await fetchJson(`/api/integrations/${system}`)).data;
}

export async function getTaskOwnerView() {
  return (await fetchJson("/api/tasks/owners")).data;
}

export async function updateTaskStatus(taskId, taskStatus, operator = "ui") {
  return (
    await fetchJson(`/api/tasks/${taskId}/status`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task_status: taskStatus, operator }),
    })
  ).data;
}
