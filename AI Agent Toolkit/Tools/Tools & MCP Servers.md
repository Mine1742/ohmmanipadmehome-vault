#aiagent #claudecode

[[AI Agent Toolkit Hub]]

Claude Code's built-in tools (Read, Edit, Bash, Grep, Glob, WebFetch, etc.) don't need setup. This note tracks *added* capability: MCP servers connected to projects, and any custom scripts you invoke as ad-hoc tools via Bash.

## MCP servers in use

| Server | Scope (this vault / global / project) | What it's for | Config location |
|--------|----------------------------------------|----------------|------------------|
| _(none configured yet)_ | | | |

Project-level MCP servers are declared in a `.mcp.json` at the project root. User-level (available everywhere) servers are configured in Claude Code's global settings, not per-project.

See [[Adding_Obsidian_MCP_to_Claude]] for the Obsidian MCP server setup specifically (Claude Desktop config, not Claude Code).

## Custom scripts used as tools

Notes on any one-off scripts you rely on Claude Code to invoke via `Bash` (not full MCP tools, just useful enough to remember exist) — e.g. anything in [[DevOps Hub]] or [[Powershell Hub]] that you point an agent at regularly.

| Script | Location | Purpose |
|--------|----------|---------|
| _(none logged yet)_ | | |
