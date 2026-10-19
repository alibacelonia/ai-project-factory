# Claymorphism

Use friendly, inflated forms for playful consumer workflows without turning every element into a toy.

- **Palette:** Light background `#FFF6ED`, foreground `#2D2438`, primary `#7C5CFC`, secondary `#FF9F68`, accent `#38C7A2`, surface `#FFFDFC`, focus `#4B32D0`. Dark background `#211A2A`, foreground `#FFF8F0`, surface `#30263A`, primary `#B9A5FF`, accent `#62E4C1`.
- **Type:** Rounded sans such as Nunito Sans or system fallback; bold compact headings and highly legible body copy. Avoid novelty faces for forms.
- **Surfaces:** 20–32px radii, soft outer shadows, a small inner highlight, thick shapes, and generous spacing. Reserve inflated depth for cards and key controls; keep long content flat.
- **Components:** Pill buttons, chunky toggles, illustrated empty states, compact cards, and inputs with clear borders. Tables should become simple lists/cards, not bubbly cells.
- **Interaction:** Hover increases highlight and lifts 2px; press compresses without large scaling. Focus uses a crisp contrasting ring outside the clay shadow; disabled controls lose depth and saturation.
- **Responsive:** Reduce radii and card padding, preserve touch targets, and collapse clusters into linear flows. Decorative blobs must not cause overflow.
- **Accessibility:** Use dark text and explicit boundaries despite pastel surfaces. Communicate errors through message, icon, and `aria-describedby`; never through shape alone.
- **Theme/performance:** Dark mode uses rich matte clay, not luminous plastic. Build with gradients and shadows, cap shadow layers, avoid animated filters, and honor reduced motion.

Representative preview: friendly onboarding card with progress, pill action, clear input, status badge, and illustrated empty state.
