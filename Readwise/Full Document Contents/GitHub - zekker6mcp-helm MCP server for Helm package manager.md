# GitHub - zekker6/mcp-helm: MCP server for Helm package manager

![rw-book-cover](https://opengraph.githubassets.com/03622cf8070d7e8e6f7deff9047659a934d754f5aee6a068f1281dbec739bf46/zekker6/mcp-helm)

## Metadata
- Author: [[https://github.com/zekker6/]]
- Full Title: GitHub - zekker6/mcp-helm: MCP server for Helm package manager
- Category: #articles
- Summary: MCP Helm server helps AI assistants access Helm charts without installing Helm locally. It provides tools to list charts, get chart versions, values, contents, and dependencies. You can use it via Docker, pre-built binaries, or build from source.
- URL: https://github.com/zekker6/mcp-helm

## Full Document
### zekker6/mcp-helm

Open more actions menu

### MCP Helm Server

An MCP (Model Context Protocol) server that provides tools for interacting with Helm repositories and charts. This server enables AI assistants to query Helm repositories, retrieve chart information, and access chart values without requiring local Helm installation.

The purpose of using MCP for Helm is to avoid making up format of `values.yaml` and contents of the charts when working with LLMs. Instead, the server provides a standardized way to access this information, making it easier for AI assistants to interact with Helm charts and repositories.

This MCP server is and will be providing tools for working with Helm repositories only. If you need to work with other Kubernetes resources, consider using a separate MCP server that provides tools for Kubernetes resources.

#### Features

The MCP Helm server provides the following tools:

* **list\_repository\_charts** - Lists all charts available in a Helm repository
* **get\_latest\_version\_of\_chart** - Retrieves the latest version of a specific chart
* **get\_chart\_values** - Retrieves the values file for a chart (latest version or specific version)
* **get\_chart\_contents** - Retrieves the contents of a chart (including templates, values, and metadata).
* **get\_chart\_dependencies** - Retrieves the dependencies of a chart as defined in its `Chart.yaml` file.

#### Try without installation

There is a publicly available instance of the MCP Helm server that you can use to test the features without installing it: <https://mcp-helm.zekker.dev/sse>

#### Installation

##### Run with docker

You can run the MCP Helm server using Docker. This is the easiest way to get started without needing to install Go or build from source.

```
docker run -d --name mcp-helm -p 8012:8012 --command ghcr.io/zekker6/mcp-helm:v0.0.5 -mode=sse
```

Note that the `--mode=sse` flag is used to enable Server-Sent Events mode, which used by MCP clients to connect. Alternatively, you can use `-mode=http` to enable Streamable HTTP mode.

##### Via pre-build binary

Download binary from the [releases page](https://github.com/zekker6/mcp-helm/releases).

Example for Linux x86\_64 (note that other architectures and platforms are also available):

```
latest=$(curl -s https://api.github.com/repos/zekker6/mcp-helm/releases/latest | grep 'tag_name' | cut -d\" -f4)
wget https://github.com/zekker6/mcp-helm/releases/download/$latest/mcp-helm_Linux_x86_64.tar.gz
tar axvf mcp-helm_Linux_x86_64.tar.gz
```

##### Via Mise

Mise ([mise-en-place](https://mise.jdx.dev/)) is a development environment setup tool.

```
mise i ubi:zekker6/mcp-helm@latest
```

##### Install with Go

>  Note: Go 1.24.3 is required.
> 
>  

```
go install github.com/zekker6/mcp-helm/cmd/mcp-helm@latest
```

##### Build from Source

>  Note: Go 1.24.3 is required.
> 
>  

1. Clone the repository:

 
```
git clone https://github.com/zekker6/mcp-helm.git
cd mcp-helm
```
2. Build the binary:

 
```
go build -o mcp-helm ./cmd/mcp-helm
```
3. Run the server:

 
```
./mcp-helm
```

#### Configuration

Configure your MCP client to connect to this server. The server implements the standard MCP protocol for tool discovery and execution.

#### Roadmap

* Add more tools
	+ List all charts in a repository
	+ Get latest version of the chart
	+ Get values for chart
	+ Get values for the latest version of the chart
	+ Extract full chart content
	+ Extract dependant charts from Charts.yaml
	+ Extract images used in chart
* Support using private registries
	+ Add a way to provide credentials
