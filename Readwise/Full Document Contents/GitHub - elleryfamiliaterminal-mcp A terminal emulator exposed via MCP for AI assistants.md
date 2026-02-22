# GitHub - elleryfamilia/terminal-mcp: A terminal emulator exposed via MCP for AI assistants

![rw-book-cover](https://opengraph.githubassets.com/04ca0194e7b2d34d48e08b5c0f3b63e4dac1e9ed0e40b9038f91de9a0caee5f5/elleryfamilia/terminal-mcp)

## Metadata
- Author: [[https://github.com/elleryfamilia/]]
- Full Title: GitHub - elleryfamilia/terminal-mcp: A terminal emulator exposed via MCP for AI assistants
- Category: #articles
- Summary: Terminal MCP lets AI assistants see and control your terminal in real-time. It works on macOS, Linux, and Windows using a simple API and supports many terminal features. You can install it with npm and use it to automate or debug terminal tasks easily.
- URL: https://github.com/elleryfamilia/terminal-mcp

## Full Document
### elleryfamilia/terminal-mcp

main

Go to file

Code

Open more actions menu

[![Terminal MCP](https://github.com/elleryfamilia/terminal-mcp/raw/main/logo.png)](https://github.com/elleryfamilia/terminal-mcp/blob/main/logo.png)
**Let AI see and interact with your terminal.**

Terminal MCP gives LLMs a shared view of your terminal session. Perfect for debugging CLIs and TUI applications in real-time, or letting AI drive terminal-based tools autonomously.

#### Install

```
npm install -g @ellery/terminal-mcp
```

Or via install script:

```
curl -fsSL https://raw.githubusercontent.com/elleryfamilia/terminal-mcp/main/install.sh | bash
```

#### Features

* **Full Terminal Emulation**: Uses xterm.js headless for accurate VT100/ANSI emulation
* **Cross-Platform PTY**: Native pseudo-terminal support via node-pty (macOS, Linux, Windows)
* **MCP Protocol**: Implements Model Context Protocol for AI assistant integration
* **Simple API**: Four intuitive tools for complete terminal control

#### Installation

```
# Install dependencies
npm install

# Build
npm run build
```

#### Usage

##### MCP Configuration

Add to your MCP client settings:

```
{
  "mcpServers": {
    "terminal": {
      "command": "terminal-mcp"
    }
  }
}
```

With custom options:

```
{
  "mcpServers": {
    "terminal": {
      "command": "terminal-mcp",
      "args": ["--cols", "100", "--rows", "30", "--shell", "/bin/zsh"]
    }
  }
}
```

##### Command-Line Options

```
terminal-mcp [OPTIONS]

Options:
  --cols <number>   Terminal width in columns (default: 120)
  --rows <number>   Terminal height in rows (default: 40)
  --shell <path>    Shell to use (default: $SHELL or bash)
  --help, -h        Show help message

```

#### MCP Tools

##### `type`

Send text input to the terminal.

```
{
  "name": "type",
  "arguments": {
    "text": "echo hello"
  }
}
```

##### `sendKey`

Send special keys or key combinations.

```
{
  "name": "sendKey",
  "arguments": {
    "key": "Enter"
  }
}
```

Supported keys:

* Basic: `Enter`, `Tab`, `Escape`, `Backspace`, `Delete`
* Arrow: `ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight`
* Navigation: `Home`, `End`, `PageUp`, `PageDown`, `Insert`
* Function: `F1` through `F12`
* Control: `Ctrl+A` through `Ctrl+Z`, `Ctrl+C`, `Ctrl+D`, etc.

##### `getContent`

Get the terminal buffer as plain text.

```
{
  "name": "getContent",
  "arguments": {
    "visibleOnly": false
  }
}
```

##### `takeScreenshot`

Capture the terminal state with cursor position and dimensions.

```
{
  "name": "takeScreenshot",
  "arguments": {}
}
```

#### Architecture

```
MCP Client (Claude Code, etc.)
    │ STDIO (JSON-RPC)
    ▼
Terminal MCP Server (Node.js)
    ├── MCP SDK (@modelcontextprotocol/sdk)
    ├── Terminal Emulator (@xterm/headless)
    └── PTY Manager (node-pty)
            │
            ▼
        Shell Process (bash, zsh, etc.)

```

#### Example Session

```
# Type a command
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"type","arguments":{"text":"ls -la"}}}

# Send Enter key
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"sendKey","arguments":{"key":"Enter"}}}

# Get the output
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"getContent","arguments":{}}}
```

#### Development

##### Project Structure

```
terminal-mcp/
├── src/
│   ├── index.ts              # Entry point with CLI
│   ├── server.ts             # MCP server setup
│   ├── terminal/
│   │   ├── index.ts          # Exports
│   │   ├── session.ts        # PTY + xterm integration
│   │   └── manager.ts        # Session lifecycle
│   ├── tools/
│   │   ├── index.ts          # Tool registry
│   │   ├── type.ts           # type tool
│   │   ├── sendKey.ts        # sendKey tool
│   │   ├── getContent.ts     # getContent tool
│   │   └── screenshot.ts     # takeScreenshot tool
│   └── utils/
│       └── keys.ts           # Key code mappings
├── docs/                     # Documentation
├── package.json
└── tsconfig.json

```

##### Building

```
npm run build    # Compile TypeScript
npm run dev      # Run with tsx (development)
```

#### Documentation

See the [docs](https://github.com/elleryfamilia/terminal-mcp/blob/main/docs) folder for detailed documentation:

* [Overview](https://github.com/elleryfamilia/terminal-mcp/blob/main/docs/index.md)
* [Installation](https://github.com/elleryfamilia/terminal-mcp/blob/main/docs/installation.md)
* [Tools Reference](https://github.com/elleryfamilia/terminal-mcp/blob/main/docs/tools.md)
* [Configuration](https://github.com/elleryfamilia/terminal-mcp/blob/main/docs/configuration.md)
* [Examples](https://github.com/elleryfamilia/terminal-mcp/blob/main/docs/examples.md)
* [Architecture](https://github.com/elleryfamilia/terminal-mcp/blob/main/docs/architecture.md)

#### Requirements

* Node.js 18.0.0 or later
* Build tools for native module compilation (node-pty)

#### License

MIT
