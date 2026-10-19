# Skeuomorphism

Use recognizable physical metaphors only where they clarify specialized controls; fidelity must not compromise standard web behavior.

- **Palette:** Light workbench `#E7E0D3`, foreground `#241F19`, primary `#8B3F24`, accent `#C58A36`, surface `#F7F0E4`, border `#766958`, focus `#005FCC`. Dark workbench `#1D1A17`, foreground `#F5EEE5`, surface `#312B25`, primary `#E69A75`, focus `#8CC8FF`.
- **Type:** Humanist sans for instructions; restrained slab or serif labels may support the physical metaphor. Numbers and form labels remain plain and legible.
- **Surfaces:** Material-inspired gradients, seams, inset wells, modest textures, and directional shadows. Use texture as decoration; never rasterize text or controls.
- **Components:** Dials, switches, meters, and trays require semantic HTML, keyboard equivalents, value labels, and familiar fallback controls. Standard forms remain visually related but conventional.
- **Interaction:** Movement follows the physical model with short, predictable travel. Hover reveals affordance; focus remains a modern visible ring. Disabled state visibly locks the control and exposes its status.
- **Responsive:** Replace intricate controls with simpler linear equivalents when space is tight. Maintain large hit areas and readable values.
- **Accessibility:** Every visual instrument needs textual state and screen-reader-operable controls. Do not rely on texture, lighting, or analog position alone.
- **Theme/performance:** Dark mode changes materials and lighting deliberately. Prefer CSS textures and small optimized assets; avoid audio, physics, or canvas unless requirements justify them. Respect reduced motion.

Representative preview: a focused control console combining one accessible rotary control, status meter, standard form, and action tray.
