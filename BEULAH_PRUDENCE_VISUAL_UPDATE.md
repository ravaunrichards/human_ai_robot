# Beulah and Prudence visual update

## Implemented in this overlay
- Replaced the generic illustrated avatar with the product-listing reference photo for Beulah.
- Added an on-screen Beulah / Prudence selector that switches the visible reference photo, name, accessible description, and status label.
- Kept the existing conversation UI, voice controls, provider status checks, shared-history polling, and simulation-only safety state.
- Kept the update additions-only; no GitHub repository or Render service was modified.

## Reference image sources
- Beulah: https://novabeige.com/cdn/shop/files/Beige_Minimalist_New_Heels_Collection_Instagram_Post_-_2025-08-29T214646.686.jpg?v=1756496922&width=416
- Prudence: https://novabeige.com/cdn/shop/files/ITD133-07.jpg?v=1756500789&width=416

The images are loaded from the vendor's website at runtime because this build environment could not download the image bytes directly. Internet access is therefore required to display them; if the vendor changes or removes these URLs, the images may stop loading. The package does not contain local copies of the photos.

## Not implemented by this update
- Animated/3D characters, lip-sync, facial expressions, or body animation.
- A configured live AI provider or API credentials. The existing backend still requires a valid server-side API key and enabled model.
- Deployment to GitHub, Render, or any external service.

## Verification performed
- `node --check overlay/web/app.js`: passed.
- `unzip -t human_ai_robot_beulah_prudence_visual.zip`: passed.
- Browser-based end-to-end rendering and remote image loading were not verified in this environment.
