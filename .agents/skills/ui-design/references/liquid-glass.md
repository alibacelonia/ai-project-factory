# Liquid Glass

Use layered translucent forms, soft specular highlights, and fluid geometry for premium interfaces, with a fully usable opaque fallback.

- **Palette:** Light background `#EAF4FF`, foreground `#10203A`, primary `#3867F4`, accent `#00AFC7`, surface `rgba(255,255,255,.68)`, border `rgba(255,255,255,.82)`, focus `#1747C9`. Dark background `#06111F`, foreground `#F4FAFF`, surface `rgba(12,31,51,.74)`, primary `#8EADFF`, accent `#5CE1EE`.
- **Type:** Neutral sans with semibold headings and comfortable body weight; avoid thin lettering through translucent layers.
- **Surfaces:** Irregular but controlled radii, layered alpha, edge highlights, subtle inner glow, and shallow refraction-like gradients. Establish opaque fallback tokens before feature-query enhancements.
- **Components:** Use liquid treatment for nav, key cards, sheets, and segmented controls. Inputs and tables need steadier, higher-opacity surfaces. Preserve native geometry and obvious labels.
- **Interaction:** Hover slightly shifts highlight position; pressed states compress depth. Focus is a solid ring independent of glass effects. Disabled surfaces flatten and retain readable text.
- **Responsive:** Reduce transparency, nested layers, blur, and floating overlap on smaller screens; keep sheets within safe viewport bounds.
- **Accessibility:** Contrast is evaluated against the composited result and worst underlying content. Do not use transparency to communicate selection.
- **Theme/performance:** Each theme has tuned alphas and borders; inherently complex areas may stay darker for readability. Limit `backdrop-filter`, avoid animating blur, use `@supports` fallbacks, and respect reduced motion.

Representative preview: subscription workspace with liquid navigation, premium plan cards, segmented billing control, and opaque checkout form.
