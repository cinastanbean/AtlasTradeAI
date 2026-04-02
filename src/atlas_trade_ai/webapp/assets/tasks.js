import { getTaskOwnerView, updateTaskStatus } from "./api.js";

async function renderTasks() {
  const data = await getTaskOwnerView();
  const kpis = [
    ["负责人数量", data.owner_count],
    ["未完成任务", data.open_task_count],
    ["升级任务数", data.escalation_task_count],
  ];
  document.querySelector("#task-kpis").innerHTML = kpis
    .map(
      ([label, value]) => `
      <div class="kpi-card">
        <div class="label">${label}</div>
        <div class="value">${value}</div>
      </div>
    `
    )
    .join("");

  document.querySelector("#owner-view").innerHTML = (data.owners || [])
    .map(
      (owner) => `
      <div class="list-card">
        <h3>${owner.assignee_name}</h3>
        <p>${owner.role}</p>
        <p>待处理: ${owner.pending_count} / 高优先级: ${owner.high_priority_count} / 升级任务: ${owner.escalation_task_count}</p>
        ${(owner.tasks || [])
          .slice(0, 5)
          .map(
            (task) => `
            <div class="inline-card">
              <strong>${task.task_title}</strong>
              <div>${task.priority} / ${task.task_status}</div>
              <button data-complete="${task.task_id}">标记完成</button>
            </div>
          `
          )
          .join("")}
      </div>
    `
    )
    .join("");

  document.querySelector("#escalation-task-view").innerHTML = (data.escalation_tasks || [])
    .map(
      (task) => `
      <div class="list-card">
        <h3>${task.task_title}</h3>
        <p>负责人: ${task.assignee_id || "-"}</p>
        <p>${task.priority} / ${task.task_status}</p>
        <p>${task.task_description || "-"}</p>
        <button data-complete="${task.task_id}">标记完成</button>
      </div>
    `
    )
    .join("");

  document.querySelectorAll("[data-complete]").forEach((button) => {
    button.addEventListener("click", async () => {
      await updateTaskStatus(button.dataset.complete, "已完成", "tasks_ui");
      await renderTasks();
    });
  });
}

document.querySelector("#refresh-tasks").addEventListener("click", renderTasks);
renderTasks();
