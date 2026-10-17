# Operational scripts

`mod_overview.py` inventories local mods without fetching or executing project
code. Explicit workspace setup pins its runtime, view and catalog; generated
VS Code tasks open, refresh or watch the view. See [overview maintenance and
security](../docs/MOD-OVERVIEW.md). The watcher is the sole folder-open task;
all gameplay, deployment and publishing workflows remain manual.
This distribution intentionally does not invent a working SteamCMD publishing script or a remote SFTP log path. Use existing verified scripts in each repository. WinSCP diagnostics require a locally saved session and a host-key verification step. Do not paste credentials into command arguments or repository files. Read-only SFTP must be enforced at the server/account level where possible.
