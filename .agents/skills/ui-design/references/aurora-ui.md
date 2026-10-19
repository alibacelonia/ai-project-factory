# Aurora UI

Use soft spectral gradients behind restrained content surfaces to signal imaginative AI and creative products.

- **Palette:** Light background `#F7F9FF`, foreground `#111827`, primary `#6366F1`, secondary `#8B5CF6`, accent `#22D3EE`, surface `rgba(255,255,255,.88)`, border `#CBD5E1`, focus `#4338CA`. Dark background `#070B1A`, foreground `#F8FAFC`, surface `rgba(15,23,42,.88)`, primary `#A5B4FC`, accent `#67E8F9`.
- **Type:** Clean geometric sans; confident headings, relaxed body line-height, monospace only for model or code metadata.
- **Surfaces:** Large blurred gradient fields belong behind content, never behind text without a stable surface. Use 16–20px cards, faint borders, and soft elevation.
- **Components:** Calm solid buttons, high-opacity forms, clear cards, conversation panels, and data tables. Aurora color may mark selected or generative states but not errors.
- **Interaction:** Hover shifts border and highlight subtly; short gradient movement may accompany a deliberate action. Focus is static and high contrast. Disabled controls use a quiet solid surface and retain readable labels.
- **Responsive:** Simplify gradient count and blur radius on mobile; avoid fixed blobs that cause overflow or obscure controls.
- **Accessibility:** Test surfaces against every gradient position. Status and generated content need explicit labels; do not encode confidence through hue alone.
- **Theme/performance:** Light uses pale atmospherics; dark uses restrained luminous fields. Render gradients in CSS, cap blur layers, animate transforms/opacity only, and remove ambient animation for reduced motion.

Representative preview: AI workspace with atmospheric canvas, stable prompt form, output card, source list, and clear state indicators.
