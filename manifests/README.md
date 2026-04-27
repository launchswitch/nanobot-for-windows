# winget Manifests for nanobot

This directory contains winget manifest files for publishing [nanobot](https://github.com/HKUDS/nanobot) to the [Windows Package Manager (winget)](https://learn.microsoft.com/en-us/windows/package-manager/).

## How to submit

1. Fork [microsoft/winget-pkgs](https://github.com/microsoft/winget-pkgs)
2. Copy the manifests into `manifests/h/HKUDS/nanobot/<version>/`
3. Create a pull request against `microsoft/winget-pkgs`

## Current status

The manifest uses the Python/PyPI installer approach. Before submitting:
- Replace the `PackageVersion` with the actual release version
- Generate SHA256 hashes for the PyPI wheel
- Test locally with `winget install --manifest manifests/`

## Prerequisites for Windows users

- Python >= 3.11 (or [uv](https://github.com/astral-sh/uv))
- Node.js >= 18 (only needed for WhatsApp channel)

## Alternative install methods

```powershell
# Via uv (recommended)
uv tool install nanobot-ai

# Via pip
pip install nanobot-ai

# Via winget (once published)
winget install HKUDS.nanobot
```
