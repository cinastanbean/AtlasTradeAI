import { getOrders } from "./api.js";

const columns = [
  "已确认",
  "执行中",
  "待发货",
  "运输 / 交付中",
  "待回款",
];

function badge(level) {
  return `<span class="badge ${level || ""}">${level || "unknown"}</span>`;
}

async function renderOrders() {
  const orders = await getOrders();
  const html = columns
    .map((status) => {
      const filtered = orders.filter((item) => item.current_status === status);
      return `
        <div class="kanban-column">
          <h2>${status}</h2>
          ${filtered
            .map(
              (item) => `
              <a class="order-card" href="/ui/order-detail.html?order_id=${item.order_id}">
                <div>${badge(item.risk_level)}${item.business_type}</div>
                <h3>${item.order_no}</h3>
                <p>${item.customer_name}</p>
                <p>${item.sub_status || "-"}</p>
                <p>计划交付 ${item.planned_delivery_date || "-"}</p>
              </a>
            `
            )
            .join("") || "<p>暂无订单</p>"}
        </div>
      `;
    })
    .join("");
  document.querySelector("#order-kanban").innerHTML = html;
}

document.querySelector("#refresh-orders").addEventListener("click", renderOrders);
renderOrders();
