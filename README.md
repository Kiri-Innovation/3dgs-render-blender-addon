# 3DGS Render for Blender

Free, open-source tools for importing, editing, animating and rendering 3D Gaussian Splats in Blender.

Created by [KIRI Engine](https://www.kiriengine.app/) and moving into community-led maintenance.

<img width="1280" height="720" alt="3DGS Render for Blender" src="https://github.com/user-attachments/assets/1e0e669a-6505-47dd-83ed-bb39403c12dc" />

[Download releases](https://github.com/Kiri-Innovation/3dgs-render-blender-addon/releases) · [Written guide](https://www.kiriengine.app/3d-tools/3dgs-render) · [Video tutorials](https://www.youtube.com/@3D-Tools-by-KIRI-Engine)

> [!NOTE]
> **Community maintenance and documentation status:** 3DGS Render was created and originally maintained by KIRI Engine. The project is now moving toward community-led development, with trusted community maintainers reviewing contributions and preparing releases. KIRI Engine will remain the repository owner and project steward, but will no longer be the sole day-to-day maintainer.
>
> Community development may move faster than KIRI Engine's written documentation and YouTube tutorials. For version-specific features, compatibility and known issues, check any notes attached to the release you installed, ask the community or play around!

## What 3DGS Render does

3DGS Render brings Gaussian Splatting content into a familiar Blender workflow. It can help you:

- Import and view 3DGS `.ply` files in Blender.
- Edit splats using Blender selections, modifiers, cropping and colour tools.
- Switch between an editable mesh-based workflow and a faster render workflow.
- Render Gaussian Splats and composite them with native Blender scene elements.
- Create sampled Eevee shadow proxies so splats can cast approximate shadows onto Blender meshes. *(Experimental.)*
- Create proxy-based animation and bake rigged splat sequences. *(Experimental.)*
- Bake lighting information into splats. *(Experimental.)*
- Export edited 3DGS files and animated `.ply` sequences.
- Convert supported mesh data into 3DGS output.

Some features are experimental and may behave differently across scenes, GPUs, operating systems and Blender versions. Back up important project files before testing any release.

## Download and compatibility

The [GitHub Releases page](https://github.com/Kiri-Innovation/3dgs-render-blender-addon/releases) is the source of truth for current downloads, supported Blender versions, changes, known issues and fixes.

Contributions merged into `main` may not always be promptly packaged as releases. Most Blender users should wait for a stable release unless they are helping with development and understand how to assemble and package the required dependencies.

## Installation

1. Open the [GitHub Releases page](https://github.com/Kiri-Innovation/3dgs-render-blender-addon/releases).
2. Open the release that matches your Blender version and operating system.
3. Download the packaged add-on `.zip` from **Assets**. Do not extract it.
4. In Blender, open **Edit → Preferences → Get Extensions**.
5. Open the menu in the upper-right and choose **Install from Disk**.
6. Select the downloaded ZIP and confirm the installation.
7. Open the **3D Viewport**, press **N**, and select the **3DGS Render** tab.

The add-on is also available as a free download on [Superhive](https://superhivemarket.com/products/3dgs-render-by-kiri-engine). Superhive is a convenient download mirror; new community betas may appear on GitHub first.

## Getting started

For the full workflow, use the [written guide](https://www.kiriengine.app/3d-tools/3dgs-render) and [KIRI Engine video tutorials](https://www.youtube.com/@3D-Tools-by-KIRI-Engine).

For a basic import:

1. Open the add-on from the Blender **N-panel**.
2. Select **Edit** as the active mode.
3. Open the **Import** menu.
4. Import a supported 3DGS `.ply` file.
5. Use **Edit** mode for selections, modifiers and other changes, or switch to **Render** mode for rendering workflows.

Names, controls and available features may differ between releases.

In **Render** mode, each Gaussian-splat proxy follows Blender's normal visibility controls. Use the Outliner **eye** or **monitor** controls to show or hide a splat in the live viewport. Use its **camera/render** control to include or exclude it from offline stills and animations. Render-disabled collections and animated render-visibility values are also respected.

Gaussian-splat proxies can also be duplicated with Blender's normal **Shift+D** workflow. Each copy is rendered with its own transform, visibility and animation, and a duplicate created from a Blender mesh source keeps its independent placement when source transforms are refreshed. Each copy is currently packed as another complete set of splats on the GPU, so VRAM use, sorting work and render cost increase with every duplicate. Use duplicates carefully with large scans.

When using **GS to Mesh Shadows (Eevee)**, rebuilding creates one unselectable shadow-proxy object for each Gaussian-splat source. Each proxy is parented to its source so it follows the source transform. **Total Max Cards** is a single scene-wide sampling budget shared between all of those proxies.

## Getting help and reporting problems

3DGS Render is free, open-source and community-maintained. KIRI Engine hosts the repository but does not guarantee direct technical support, compatibility updates or response times.

- Use [GitHub Issues](https://github.com/Kiri-Innovation/3dgs-render-blender-addon/issues) for reproducible bugs.
- Use the [KIRI Engine Discord thread](https://discord.com/channels/952917583659667517/1289563910390812723) for informal conversation and general questions. Please record confirmed bugs and technical findings on GitHub so they remain findable by all contributors.

When reporting a bug, include:

- Add-on version and download source.
- Blender version.
- Operating system.
- GPU model and driver, where relevant.
- A concise description of the expected and actual result.
- Exact reproduction steps.
- Console output, screenshots or a short video.
- A minimal `.blend` or sample `.ply` when it can be shared safely.

## Contributing

Contributions are welcome from Blender developers, 3DGS researchers, technical artists, testers, documentation writers and users.

The add-on was originally generated as a large monolithic script using Serpens for Blender.

Community contributor and maintainer [@Hrsh-Venket](https://github.com/Hrsh-Venket) ([X profile](https://x.com/Eric4rthurBlair)) refactored it into focused modules under `src/`, making the project much easier to understand and extend. Many thanks to him for helping make this a true open-source project.

## Development and release notes

The `main` branch contains ongoing development and may not always be ready for production use.

## Recent community contributions

- [@Hrsh-Venket](https://github.com/Hrsh-Venket) ([X profile](https://x.com/Eric4rthurBlair)): modular codebase refactor and bake-performance work, including GPU-assisted spherical-harmonic rotation, binding caching and background cache writes, as well as improved deformation quality at joints when using proxy rigging
- ([#59](https://github.com/Kiri-Innovation/3dgs-render-blender-addon/pull/59), [#60](https://github.com/Kiri-Innovation/3dgs-render-blender-addon/pull/60)).
- [@punk-kaos](https://github.com/punk-kaos): Blender 5.2 compatibility, real-time relighting and real-time mesh-shadow support
-  ([#61](https://github.com/Kiri-Innovation/3dgs-render-blender-addon/pull/61)).

Thank you to everyone who has contributed code, testing, bug reports, documentation and artwork. See the full [contributor history](https://github.com/Kiri-Innovation/3dgs-render-blender-addon/graphs/contributors).

## Project stewardship

3DGS Render was initiated and maintained by KIRI Engine as a free tool for the 3D community. KIRI Engine is now stepping back from regular maintenance and updates so that the project can grow through community leadership.

KIRI Engine will continue to host and steward the repository. Trusted community maintainers may triage issues, review and merge pull requests, prepare releases and help guide the roadmap. Maintainers are volunteers and do not have guaranteed working hours or response times.

If you are interested in helping maintain the project, open a GitHub discussion or contact the current maintainers with your relevant Blender/Python experience and the areas you would like to support.

## License

See [LICENSE](./LICENSE) for the repository's license terms.
