const PRESETS_URL = "/templates/web-saas/template/frontend/design-system/presets.json";
const layouts = ["standard", "dashboard", "bento-grid", "editorial", "landing-page", "sidebar-application", "split-screen", "full-screen"];
const effects = ["none", "subtle-transitions", "aurora-gradients", "glass-surfaces", "kinetic-animation", "spatial-depth"];
const state = { presets: [], style: "minimalism", theme: "system", layout: "standard", effect: "subtle-transitions", viewport: "desktop", screen: "components", comparison: "glassmorphism" };

const byId = (id) => document.getElementById(id);
const controls = ["theme", "layout", "effect", "viewport", "screen", "comparison"];

function resolvedTheme() {
  return state.theme === "system" ? (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light") : state.theme;
}

function variablesFor(preset) {
  const tokens = preset[resolvedTheme()];
  return {
    "color-background": tokens.colors.background, "color-foreground": tokens.colors.foreground,
    "color-primary": tokens.colors.primary, "color-secondary": tokens.colors.secondary,
    "color-accent": tokens.colors.accent, "color-surface": tokens.colors.surface,
    "color-muted": tokens.colors.muted, "color-destructive": tokens.colors.destructive,
    "color-border": tokens.colors.border, "color-focus": tokens.colors.focus,
    "font-heading": tokens.typography.heading, "font-body": tokens.typography.body,
    "font-weight-heading": tokens.typography.weight, "letter-spacing-heading": tokens.typography.letter_spacing,
    "radius-surface": tokens.surface.radius, "border-width": tokens.surface.border_width,
    "shadow-surface": tokens.surface.shadow, "surface-opacity": tokens.surface.transparency,
    "backdrop-blur": tokens.surface.blur, "motion-duration": tokens.motion.duration,
    "motion-easing": tokens.motion.easing, "motion-hover": tokens.motion.hover,
  };
}

function previewMarkup(name) {
  return `<div class="ui-app-shell">
    <header class="ui-header"><a class="ui-brand" href="#">${name}</a><nav class="ui-nav" aria-label="Preview"><a href="#">Overview</a><a href="#">Projects</a><a href="#">Settings</a></nav><span class="ui-badge">Preview</span></header>
    <aside class="ui-sidebar"><p class="ui-eyebrow">Workspace</p><a aria-current="page" href="#">Dashboard</a><a href="#">Activity</a><a href="#">Settings</a></aside>
    <main class="ui-main">
      <section class="gallery-screen gallery-components ui-section" data-screen="components"><div class="ui-section-heading"><div><p class="ui-eyebrow">Actual primitives</p><h2>Component system</h2></div><div class="ui-tabs" role="tablist" aria-label="Example tabs"><button class="ui-tab" role="tab" aria-selected="true">Overview</button><button class="ui-tab" role="tab" aria-selected="false">Details</button></div></div><div class="ui-grid ui-grid--components"><article class="ui-card"><h3>Create project</h3><label>Name<input class="ui-input" value="Northstar" aria-label="Project name"></label><label>Plan<select class="ui-input ui-select" aria-label="Plan"><option>Professional</option></select></label><label>Notes<textarea class="ui-input ui-textarea" placeholder="What will you build?"></textarea></label><label class="ui-checkbox"><input type="checkbox" checked>Weekly report</label><button class="ui-button">Create</button> <button class="ui-button ui-button--secondary">Cancel</button></article><article class="ui-card"><h3>Project health</h3><div class="ui-table-wrap" tabindex="0"><table class="ui-table"><caption class="ui-sr-only">Project status</caption><thead><tr><th>Service</th><th>Status</th></tr></thead><tbody><tr><td>Web</td><td><span class="ui-badge">Ready</span></td></tr><tr><td>API</td><td>Building</td></tr></tbody></table></div><div class="ui-alert" role="status">All systems are healthy.</div><button class="ui-button" disabled>Disabled</button></article><article class="ui-card"><h3>Empty state</h3><section class="ui-empty"><strong>No invitations</strong><p>Invite a teammate when you are ready.</p></section><details class="ui-dropdown"><summary class="ui-button ui-button--quiet">Open menu</summary><div class="ui-dropdown__menu"><a href="#">View activity</a><button type="button">Duplicate</button></div></details><span class="ui-tooltip" tabindex="0"><span class="ui-badge">Focus me</span><span class="ui-tooltip__content" role="tooltip">Accessible tooltip</span></span></article></div></section>
      <section class="gallery-screen gallery-dashboard" data-screen="dashboard" hidden><div class="ui-section-heading"><div><p class="ui-eyebrow">Dashboard</p><h2>Performance at a glance</h2></div><button class="ui-button">New report</button></div><div class="ui-grid"><article class="ui-card"><span class="ui-eyebrow">Revenue</span><strong class="ui-stat">$84k</strong><small>+12% this month</small></article><article class="ui-card"><span class="ui-eyebrow">Active users</span><strong class="ui-stat">12.8k</strong><small>Across 14 teams</small></article><article class="ui-card"><span class="ui-eyebrow">Uptime</span><strong class="ui-stat">99.99%</strong><div class="ui-chart" role="img" aria-label="Uptime trend increasing"></div></article></div></section>
      <section class="gallery-screen gallery-landing" data-screen="landing" hidden><p class="ui-eyebrow">Built for momentum</p><h1>Make your next idea unmistakable.</h1><p class="ui-lede">A responsive landing-page sample that uses the current style, theme, layout, and effects.</p><div class="ui-actions"><button class="ui-button">Start building</button><button class="ui-button ui-button--secondary">See the system</button></div></section>
    </main></div>`;
}

function applyPreview(element, preset, isComparison = false) {
  const vars = variablesFor(preset);
  element.dataset.style = preset.id;
  element.dataset.theme = resolvedTheme();
  element.dataset.layout = state.layout;
  element.dataset.effects = state.effect;
  element.dataset.viewport = state.viewport;
  element.innerHTML = previewMarkup(preset.name);
  Object.entries(vars).forEach(([name, value]) => element.style.setProperty(`--${name}`, value));
  element.querySelectorAll(".gallery-screen").forEach((screen) => { screen.hidden = screen.dataset.screen !== state.screen; });
  if (!isComparison) byId("tokens").textContent = JSON.stringify({ style: preset.id, theme: resolvedTheme(), ...preset[resolvedTheme()] }, null, 2);
}

function renderStyleList(filter = "") {
  const needle = filter.trim().toLowerCase();
  const matches = state.presets.filter((item) => `${item.name} ${item.description} ${item.recommended_for.join(" ")}`.toLowerCase().includes(needle));
  byId("style-list").innerHTML = matches.map((item) => `<button class="gallery-style-option" type="button" role="option" data-id="${item.id}" aria-selected="${item.id === state.style}"><strong>${item.name}</strong><small>${item.recommended_for.join(" · ")}</small></button>`).join("");
  byId("style-list").querySelectorAll("button").forEach((button) => button.addEventListener("click", () => { state.style = button.dataset.id; const preset = currentPreset(); state.layout = preset.default_layout; byId("layout").value = state.layout; render(); }));
}

function currentPreset(id = state.style) { return state.presets.find((item) => item.id === id) ?? state.presets[0]; }
function yamlFor(preset) {
  const tokens = preset[resolvedTheme()];
  const animation = state.effect === "kinetic-animation" ? "kinetic" : state.effect === "none" && preset.id !== "kinetic-ui" ? "none" : "subtle";
  const glass = state.effect === "glass-surfaces";
  return `design:\n  enabled: true\n  style: ${preset.id}\n  layout: ${state.layout}\n  theme:\n    mode: ${state.theme}\n    palette: style-default\n    primary_color: "${tokens.colors.primary.slice(0, 7)}"\n    accent_color: "${tokens.colors.accent.slice(0, 7)}"\n  typography:\n    preset: style-default\n    scale: default\n  surfaces:\n    border_radius: medium\n    shadow_intensity: medium\n    transparency: ${glass ? "medium" : "none"}\n    blur_intensity: ${glass ? "medium" : "none"}\n  effects:\n    animation: ${animation}\n    enhancements: [${state.effect}]\n  responsive:\n    mobile: true\n    tablet: true\n    desktop: true\n  accessibility:\n    target: WCAG-2.2-AA\n    reduced_motion: true`;
}

function render() {
  const preset = currentPreset();
  byId("style-id").textContent = preset.id;
  byId("style-name").textContent = preset.name;
  byId("style-description").textContent = `${preset.description} Recommended for ${preset.recommended_for.join(" and ")}. ${preset.theme_behavior}`;
  applyPreview(byId("preview"), preset);
  const comparing = byId("compare").checked;
  byId("compare-field").hidden = !comparing;
  byId("comparison-preview").hidden = !comparing;
  if (comparing) applyPreview(byId("comparison-preview"), currentPreset(state.comparison), true);
  renderStyleList(byId("filter").value);
}

async function start() {
  const response = await fetch(PRESETS_URL);
  if (!response.ok) throw new Error(`Could not load presets (${response.status})`);
  state.presets = await response.json();
  for (const layout of layouts) byId("layout").add(new Option(layout.replaceAll("-", " "), layout));
  for (const effect of effects) byId("effect").add(new Option(effect.replaceAll("-", " "), effect));
  for (const preset of state.presets) byId("comparison").add(new Option(preset.name, preset.id));
  controls.forEach((id) => byId(id).addEventListener("change", (event) => { state[id] = event.target.value; render(); }));
  byId("filter").addEventListener("input", (event) => renderStyleList(event.target.value));
  byId("compare").addEventListener("change", render);
  byId("copy-config").addEventListener("click", async () => {
    await navigator.clipboard.writeText(yamlFor(currentPreset()));
    byId("copy-status").textContent = "Copied compatible design configuration.";
  });
  state.style = state.presets.some((item) => item.id === state.style) ? state.style : state.presets[0].id;
  const first = currentPreset(); state.layout = first.default_layout; byId("layout").value = state.layout;
  byId("theme").value = state.theme; byId("effect").value = state.effect; byId("viewport").value = state.viewport; byId("screen").value = state.screen; byId("comparison").value = state.comparison;
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { if (state.theme === "system") render(); });
  render();
}

start().catch((error) => { byId("style-name").textContent = "Gallery failed to load"; byId("style-description").textContent = error.message; });
