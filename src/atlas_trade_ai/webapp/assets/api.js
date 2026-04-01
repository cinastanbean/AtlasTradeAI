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

export async function getAgentRuns() {
  return (await fetchJson("/api/agent-runs")).data;
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
