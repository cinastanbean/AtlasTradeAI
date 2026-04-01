import { getIntegrationSnapshot } from "./api.js";

function renderSections(selector, sections) {
  document.querySelector(selector).innerHTML = sections
    .map(
      (section) => `
      <div class="section-block">
        <h3>${section.section}</h3>
        ${section.items
          .slice(0, 5)
          .map((item) => `<pre class="code-block">${JSON.stringify(item, null, 2)}</pre>`)
          .join("")}
      </div>
    `
    )
    .join("");
}

async function renderSnapshots() {
  const [crm, erp, dingtalk] = await Promise.all([
    getIntegrationSnapshot("crm"),
    getIntegrationSnapshot("erp"),
    getIntegrationSnapshot("dingtalk"),
  ]);
  renderSections("#crm-sections", crm);
  renderSections("#erp-sections", erp);
  renderSections("#dingtalk-sections", dingtalk);
}

document.querySelector("#refresh-integrations").addEventListener("click", renderSnapshots);
renderSnapshots();
