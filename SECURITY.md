# Security policy

3DGS Render is a Blender extension that executes Python at load time and ships bundled Python wheels (`open3d`, `scipy`, and others). A vulnerability in the addon can lead to arbitrary code execution in the user's Blender session and, through it, access to any file the user can read.

If you believe you've found a security issue, please **report it privately** — do not open a public GitHub issue.

## How to report

Use GitHub's **[Report a vulnerability](https://github.com/Kiri-Innovation/3dgs-render-blender-addon/security/advisories/new)** flow (Security tab → "Report a vulnerability"). This routes the report through a private security advisory that only the maintainers can see.

If GitHub's flow is unavailable to you, email the maintainer directly through their [GitHub profile](https://github.com/Hrsh-Venket).

## What to include

- A clear description of the issue and its impact.
- Reproduction steps or a proof-of-concept — ideally a small `.ply`, `.blend`, or Python snippet.
- The addon version and Blender version you observed it on.
- The operating system.

## What to expect

- **Acknowledgment**: within 7 days.
- **Assessment and fix window**: depends on severity, typically within 30 days for confirmed issues.
- **Disclosure**: coordinated with you. The advisory is published once a fix is available, crediting the reporter unless you request otherwise.

## Scope

In scope:

- Arbitrary code execution via crafted `.ply`, `.blend`, or geometry-node assets.
- Path traversal or arbitrary file read/write via import/export operators.
- Credential or token leakage from bundled dependencies.
- Vulnerabilities in the wheels the release ships.

Out of scope:

- Bugs that only crash Blender without leaking data or executing attacker-controlled code (please file these as regular bug reports).
- Issues in Blender itself — please report those to the [Blender project](https://developer.blender.org/).
- Issues in unrelated third-party addons.
