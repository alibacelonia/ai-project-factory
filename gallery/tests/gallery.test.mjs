import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../../", import.meta.url);
const presetsUrl = new URL("templates/web-saas/template/frontend/design-system/presets.json", root);

test("gallery consumes the canonical 22-preset registry", async () => {
  const presets = JSON.parse(await readFile(presetsUrl, "utf8"));
  const app = await readFile(new URL("../app.js", import.meta.url), "utf8");
  assert.equal(presets.length, 22);
  assert.match(app, /templates\/web-saas\/template\/frontend\/design-system\/presets\.json/);
  for (const preset of presets) {
    assert.ok(preset.light.colors.focus);
    assert.ok(preset.dark.colors.focus);
    assert.ok(preset.capabilities.accessibility);
  }
});

test("gallery supports theme, layout, effects, viewports, screens, comparison, tokens, and YAML copy", async () => {
  const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
  for (const id of ["theme", "layout", "effect", "viewport", "screen", "compare", "tokens", "copy-config"]) {
    assert.match(html, new RegExp(`id="${id}"`));
  }
  assert.match(html, /styles\.css\.jinja/);
});

test("generated style sheet differentiates every registered preset", async () => {
  const presets = JSON.parse(await readFile(presetsUrl, "utf8"));
  const styles = await readFile(new URL("templates/web-saas/template/frontend/app/styles.css.jinja", root), "utf8");
  for (const preset of presets) assert.match(styles, new RegExp(`data-style="${preset.id}"`));
  assert.match(styles, /prefers-reduced-motion: reduce/);
  assert.match(styles, /@supports not \(backdrop-filter/);
});
