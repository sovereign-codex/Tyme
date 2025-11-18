const manifestPath = "../../chronicle/house_of_tyme_manifest.json";

async function loadManifest() {
  try {
    const res = await fetch(manifestPath);
    if (!res.ok) throw new Error(`Failed to load manifest: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error(err);
    return null;
  }
}

function createCard(title, description, badges = [], list = []) {
  const card = document.createElement("div");
  card.className = "card";
  const h3 = document.createElement("h3");
  h3.textContent = title;
  card.appendChild(h3);
  if (description) {
    const p = document.createElement("p");
    p.textContent = description;
    card.appendChild(p);
  }
  if (badges.length) {
    const wrap = document.createElement("div");
    badges.forEach((b) => {
      const span = document.createElement("span");
      span.className = "badge";
      span.textContent = b;
      wrap.appendChild(span);
    });
    card.appendChild(wrap);
  }
  if (list.length) {
    const ul = document.createElement("ul");
    list.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = item;
      ul.appendChild(li);
    });
    card.appendChild(ul);
  }
  return card;
}

function renderManifest(manifest) {
  if (!manifest) return;
  document.getElementById("tyme-core-binding").textContent = manifest.tyme_core;
  document.getElementById("codexnet-binding").textContent = manifest.codexnet;

  const scrollGrid = document.getElementById("scroll-layers-grid");
  manifest.public_scroll_layers.forEach((layer) => {
    const list = [
      `Entrypoints: ${layer.entrypoints.join(", ")}`,
      `CodexNet Hooks: ${layer.codexnet_hooks.join(", ")}`,
      `Tyme-Core Bridges: ${layer.tyme_core_bridges.join(", ")}`,
    ];
    scrollGrid.appendChild(createCard(layer.name, layer.focus, [], list));
  });

  const voiceGrid = document.getElementById("voice-grid");
  manifest.voice_of_tyme.forEach((channel) => {
    const badges = [channel.tone, channel.cadence];
    const list = [
      ...channel.prompts.map((p) => `Prompt: ${p}`),
      ...channel.delivery_modes.map((d) => `Delivery: ${d}`),
      ...channel.guardrails.map((g) => `Guardrail: ${g}`),
    ];
    voiceGrid.appendChild(createCard(channel.name, "Narrative channel", badges, list));
  });

  const planetaryGrid = document.getElementById("planetary-grid");
  manifest.planetary_ui_architecture.forEach((lane) => {
    const list = [
      `Pathways: ${lane.pathways.join(", ")}`,
      `Feedback: ${lane.feedback_signals.join(", ")}`,
      `Resilience: ${lane.resilience.join(", ")}`,
    ];
    planetaryGrid.appendChild(createCard(lane.name, lane.purpose, [], list));
  });

  const onboardingGrid = document.getElementById("onboarding-grid");
  manifest.initiate_onboarding_sequence.forEach((step) => {
    const list = [
      `Action: ${step.action}`,
      `Signals: ${step.signals.join(", ")}`,
      `Success: ${step.success_criteria.join(", ")}`,
    ];
    onboardingGrid.appendChild(createCard(step.phase, step.intent, [], list));
  });
}

loadManifest().then(renderManifest);
