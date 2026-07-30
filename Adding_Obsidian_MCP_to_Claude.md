# Adding Obsidian MCP Server to Claude

## Overview
This guide walks you through setting up the Obsidian Model Context Protocol (MCP) server to connect your Obsidian vault with Claude. This integration allows Claude to read, search, and interact with your Obsidian notes directly.

## Prerequisites
- Claude Desktop app installed
- Node.js installed (v16 or higher recommended)
- An Obsidian vault
- Basic familiarity with JSON configuration files

## Installation Steps

### 1. Install the Obsidian MCP Server

Open your terminal and install the server globally using npm:

```bash
npm install -g @modelcontextprotocol/server-obsidian
```

### 2. Locate Your Claude Configuration File

The Claude configuration file location varies by operating system:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

If the file doesn't exist, create it.

### 3. Configure the MCP Server

Edit your `claude_desktop_config.json` file to add the Obsidian MCP server configuration:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-obsidian",
        "/path/to/your/obsidian/vault"
      ]
    }
  }
}
```

**Important**: Replace `/path/to/your/obsidian/vault` with the actual path to your Obsidian vault.

#### Example Paths:
- **macOS**: `/Users/yourusername/Documents/ObsidianVault`
- **Windows**: `C:\\Users\\YourUsername\\Documents\\ObsidianVault`
- **Linux**: `/home/yourusername/Documents/ObsidianVault`

### 4. Restart Claude Desktop

Close Claude Desktop completely and reopen it for the changes to take effect.

## Verifying the Connection

After restarting Claude, you can verify the connection by asking Claude to:
- List files in your vault
- Search for specific notes
- Read the contents of a note

Example prompts:
- "How many files are in my Obsidian vault?"
- "Search my vault for notes about [topic]"
- "Show me the contents of [note name]"

## Available Features

Once connected, Claude can:

1. **List Files**: View all files and directories in your vault
2. **Read Notes**: Access the full content of any note
3. **Search**: 
   - Simple text search across all notes
   - Complex searches using JsonLogic queries
4. **Modify Notes**:
   - Append content to existing notes
   - Patch content at specific locations (headings, blocks, frontmatter)
5. **Manage Files**: Create and delete notes
6. **Periodic Notes**: Access daily, weekly, monthly, quarterly, and yearly notes
7. **Recent Changes**: View recently modified files

## Troubleshooting

### Server Not Starting
- Verify Node.js is installed: `node --version`
- Check that the npm package is installed: `npm list -g @modelcontextprotocol/server-obsidian`
- Ensure the vault path in the config is correct and has no typos

### Claude Can't Access Vault
- Confirm the vault path uses the correct format for your OS
- On Windows, ensure backslashes are escaped: `C:\\Users\\...`
- Check file permissions on your vault directory

### Configuration Not Taking Effect
- Ensure the JSON file is valid (use a JSON validator)
- Completely quit Claude Desktop (not just close the window)
- Check for syntax errors in the configuration file

### Permission Issues
- Ensure Claude has read/write permissions to your vault directory
- On macOS, you may need to grant Claude Full Disk Access in System Preferences

## Advanced Configuration

### Multiple Vaults
You can configure multiple Obsidian vaults by adding additional entries:

```json
{
  "mcpServers": {
    "obsidian-personal": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-obsidian",
        "/path/to/personal/vault"
      ]
    },
    "obsidian-work": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-obsidian",
        "/path/to/work/vault"
      ]
    }
  }
}
```

### Environment Variables
You can use environment variables in your configuration for portable setups:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-obsidian",
        "${OBSIDIAN_VAULT_PATH}"
      ]
    }
  }
}
```

## Security Considerations

- The MCP server has full read/write access to your vault
- Claude can read all notes in the connected vault
- Claude can modify, create, and delete files if instructed
- Review any destructive operations before confirming
- Consider using a separate vault for sensitive information

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Obsidian MCP Server Repository](https://github.com/modelcontextprotocol/servers)
- [Claude Desktop Documentation](https://claude.ai/desktop)

## Notes

- Changes made through Claude are immediately reflected in your Obsidian vault
- The server runs locally on your machine
- No data is sent to external servers except Claude's API for processing
- The connection is established each time Claude Desktop starts

---

*Last Updated: October 24, 2025*
