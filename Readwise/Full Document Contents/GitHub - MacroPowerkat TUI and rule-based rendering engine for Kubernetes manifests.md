# GitHub - MacroPower/kat: TUI and rule-based rendering engine for Kubernetes manifests

![rw-book-cover](https://repository-images.githubusercontent.com/985006485/88ebf1db-a672-41fb-9895-405a412535ec)

## Metadata
- Author: [[https://github.com/MacroPower/]]
- Full Title: GitHub - MacroPower/kat: TUI and rule-based rendering engine for Kubernetes manifests
- Category: #articles
- Summary: Kat is a terminal tool that helps you render and browse Kubernetes manifests using generators like Helm and Kustomize. It offers live reloading, error handling, and customizable profiles to fit different projects. You can easily navigate resources, run validations, and add custom commands for a smooth development experience.
- URL: https://github.com/MacroPower/kat

## Full Document
### MacroPower/kat

Open more actions menu

[![](https://github.com/MacroPower/kat/raw/main/docs/assets/logo.svg)](https://github.com/MacroPower/kat#)
### kat

[![Go Reference](https://camo.githubusercontent.com/df80bd0296ef3a401b25b4f6cadd36b13619a09dd857ee2b0139063951596b64/68747470733a2f2f706b672e676f2e6465762f62616467652f6769746875622e636f6d2f6d6163726f706f7765722f6b61742e737667)](https://pkg.go.dev/github.com/macropower/kat)
[![Go Report Card](https://camo.githubusercontent.com/de009ec729152a8e59fd91af35bab6e7bfe04dad10c5371396a96c9170e1b63f/68747470733a2f2f676f7265706f7274636172642e636f6d2f62616467652f6769746875622e636f6d2f6d6163726f706f7765722f6b6174)](https://goreportcard.com/report/github.com/macropower/kat)
[![](https://camo.githubusercontent.com/c9e53edd0c3488bb70d2f2805e661909ac1e4a81109343af8b0c3887d5288abc/68747470733a2f2f636f6465636f762e696f2f67682f6d6163726f706f7765722f6b61742f67726170682f62616467652e7376673f746f6b656e3d34544e59544c32575856)](https://codecov.io/gh/macropower/kat)
[![GitHub Downloads](https://camo.githubusercontent.com/ebedfa125c7247bc56b9f544673b1875d852968f1a3f878566f2d0364c39395b/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f646f776e6c6f6164732f6d6163726f706f7765722f6b61742f746f74616c)](https://github.com/MacroPower/kat#-installation)
[![Latest tag](https://camo.githubusercontent.com/9bacd106f276d172b298441110a569d5b5c7ce5fa00e29073cee16889a165c27/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f762f7461672f6d6163726f706f7765722f6b61743f6c6162656c3d76657273696f6e26736f72743d73656d766572)](https://github.com/MacroPower/kat#-installation)
[![License](https://camo.githubusercontent.com/54a32b841acd97de41421c6d3628d1b783994bd273f13ed353f5f1714554fcbf/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f6d6163726f706f7765722f6b6174)](https://github.com/macropower/kat/blob/main/LICENSE)
`kat` automatically invokes manifest generators like `helm` or `kustomize`, and provides a persistent, navigable view of rendered resources, with support for live reloading, integrated validation, and more.

It is made of two main components, which can be used together or independently:

1. A **rule-based engine** for automatically rendering and validating manifests
2. A **terminal UI** for browsing and debugging rendered Kubernetes manifests

Together, these deliver a seamless development experience that maintains context and focus while iterating on Helm charts, Kustomize overlays, and other manifest generators.

[![](https://github.com/MacroPower/kat/raw/main/docs/assets/demo.gif)](https://github.com/MacroPower/kat/blob/main/docs/assets/demo.gif)
  [![demo.gif](https://github.com/MacroPower/kat/raw/main/docs/assets/demo.gif)](https://github.com/MacroPower/kat/blob/main/docs/assets/demo.gif)  

❤️ Made with [bubble tea](https://github.com/charmbracelet/bubbletea), [chroma](https://github.com/alecthomas/chroma/), and [other amazing libraries](https://github.com/MacroPower/kat#-dependencies).

#### ✨ Features

**🔍️ Manifest browsing**

* Navigate hundreds of resources with fuzzy search and filtering
* View individual resources in your terminal with syntax highlighting

**⚡️ Live reload**

* Monitor source files with `--watch` for automatic re-rendering
* Maintain your current context between reloads so you don't lose your place
* Highlight changes with diff visualization between renders

**🐛 Error handling**

* Surface rendering and validation errors as overlays
* Works with reload; fix source files and watch errors disappear instantly

**🧪 Tool integration**

* Define profiles for any manifest generator (Helm, Kustomize, CUE, KCL, Jsonnet, etc.)
* Run tools like `kubeconform` or `kyverno` automatically on rendered manifests
* Chain multiple tools together with pre and post-render hooks

**🎯 Project detection**

* Select your defined profiles automatically using CEL expressions
* Match projects based on file contents, structure, or naming patterns

**🔌 Plugin system**

* Add custom keybind-triggered commands for your specific workflows
* Execute dry-runs, deployments, or any custom tooling without leaving kat

**🎨 Fully customizable**

* Choose from any available Chroma themes, or define your own
* Remap any keybinding to match your preferences

#### 📦 Installation

>  Note: The default `kat` configuration contains references to `helm`, `kustomize`, and `yq`. If you want to use `kat` with these tools, you will need to install them separately.
> 
>  

##### Homebrew

```
brew install macropower/tap/kat
```

##### Go

```
go install github.com/macropower/kat/cmd/kat@latest
```

##### Docker

Docker images are published to [ghcr.io/macropower](https://github.com/MacroPower/kat/pkgs/container/kat).

All images are configured with `WORKDIR=/data`, so you can mount your current directory there to run `kat` against your local files.

Run the latest alpine image:

```
docker run -it -v .:/data -e TERM=$TERM ghcr.io/macropower/kat:latest-alpine
```

The default config is located at `/config/kat/config.yaml`, and you can override it by mounting your own configuration file at that path.

There is also a scratch image that contains only the `kat` binary, which is useful when you want to build your own image (which I generally recommend doing):

```
FROM alpine:latest
COPY --from=ghcr.io/macropower/kat:latest /kat /usr/local/bin/kat
# Add whatever customization you need here.
ENTRYPOINT ["/usr/local/bin/kat"]
```

##### Nix

You can install `kat` using my [NUR](https://github.com/MacroPower/nur-packages).

With `nix-env`:

```
nix-env -iA kat -f https://github.com/macropower/nur-packages/archive/main.tar.gz
```

With `nix-shell`:

```
nix-shell -A kat https://github.com/macropower/nur-packages/archive/main.tar.gz
```

With your `flake.nix`:

```
{
  inputs = {
    macropower.url = "github:macropower/nur-packages";
  };
  # Reference the package as `inputs.macropower.packages.<system>.kat`
}
```

With [`devbox`](https://www.jetify.com/docs/devbox/):

```
devbox add github:macropower/nur-packages#kat
```

##### GitHub CLI

```
gh release download -R macropower/kat -p "kat_$(uname -s)_$(uname -m).tar.gz" -O - | tar -xz
```

And then move `kat` to a directory in your `PATH`.

##### Curl

```
curl -s https://api.github.com/repos/macropower/kat/releases/latest | \
  jq -r ".assets[] |
    select(.name | test(\"kat_$(uname -s)_$(uname -m).tar.gz\")) |
    .browser_download_url" | \
  xargs curl -L | tar -xz
```

And then move `kat` to a directory in your `PATH`.

##### Manual

You can download binaries from [releases](https://github.com/macropower/kat/releases).

#### 🔏 Verification

You can verify the authenticity and integrity of `kat` releases.

See [verification](https://github.com/MacroPower/kat/blob/main/docs/verification.md) for more details.

#### 🚀 Usage

Show help:

```
kat --help
```

Render a project in the current directory:

```
kat
```

Render a project and enable watch (live reloading):

```
kat -w
```

Render a project in a specific directory:

```
kat ./example/helm
```

Render a project in a specific directory using the `ks` profile:

```
kat ./example/kustomize ks
```

Render a project with custom profile arguments:

```
kat ./example/helm -- -g -f prod-values.yaml

kat ./example/kustomize ks -- --enable-helm
```

Render a project with command passthrough:

```
kat ./example/helm task -- helm:render
```

Read from stdin (disables rendering engine):

```
cat ./example/kustomize/resources.yaml | kat -
```

Send output to a file (disables TUI):

```
kat ./example/helm > manifest.yaml
```

#### ⚙️ Configuration

When you first run `kat`, it will attempt to add default configuration files to `$XDG_CONFIG_HOME/kat/` (or `~/.config/kat/`). This configuration allows you to customize the behavior of `kat`, such as the UI style, keybindings, rules for project detection, and profiles for rendering different types of projects.

Note that JSON schemas are also included in the configuration directory, which can be used by your editor's YAML language server.

>  Some of the default behavior around loading configuration can be overridden with command line flags or environment variables. See `kat --help` for details.
> 
>  

Over time, the default configuration may change, and the schema is currently still evolving. If you want to reset your configuration to the latest defaults, you can use `kat --write-config`, which will move your existing configuration to a backup file and generate a new default configuration.

>  You can find the default configuration file as well as JSON schemas in [pkg/config](https://github.com/MacroPower/kat/blob/main/pkg/config).
> 
>  

#### 🛠️ Rules and Profiles

You can customize how `kat` detects and renders different types of projects using **rules** and **profiles** in the configuration file. This system uses [CEL (Common Expression Language)](https://cel.dev/) expressions to provide flexible file matching and processing.

##### 🎯 Rules

**Rules determine which profile should be used.** Each rule contains:

* `match` (required): A CEL expression that returns `true` if the rule should be applied
* `profile` (required): The name of the profile to use when this rule matches

Rules use boolean CEL expressions with access to:

* `files` (list): All file paths in the directory
* `dir` (string): The directory path being processed

```
rules:
  - # Select the Helm profile if any Helm chart files exist
    match: >-
      files.exists(f, pathBase(f) in ["Chart.yaml", "Chart.yml"])
    profile: helm

  - # Select the Kustomize profile if any Kustomization files exist
    match: >-
      files.exists(f, pathBase(f) in ["kustomization.yaml", "kustomization.yml"])
    profile: ks

  - # Fallback: select the YAML profile if any YAML files exist
    match: >-
      files.exists(f, pathExt(f) in [".yaml", ".yml"])
    profile: yaml
```

##### 🎭 Profiles

**Profiles define how to render projects.** They can be automatically selected by rules, or manually specified when `kat` is invoked. Each profile contains:

* `command` (required): The command to execute
* `args`: Arguments to pass to the command
* `extraArgs`: Arguments that can be overridden from the CLI
* `env`: List of environment variables for the command
* `envFrom`: List of sources for environment variables
* `source`: Define which files to watch for changes (when watch is enabled)
* `ui`: UI configuration overrides
* `hooks`: Initialization and rendering hooks
	+ `init` hooks are executed once when `kat` is initialized
	+ `preRender` hooks are executed before the profile's command is run
	+ `postRender` hooks are executed after the profile's command has run, and are provided the rendered output via stdin
* `plugins`: Custom commands that can be executed on-demand with keybinds
	+ `description` (required): Human-readable description of what the plugin does
	+ `keys` (required): Array of key bindings that trigger the plugin
	+ `command` (required): The command to execute
	+ `args`: Arguments to pass to the command

Profile `source` expressions use list-returning CEL expressions with the same variables as rules.

```
profiles:
  helm:
    command: helm
    args: [template, .]
    extraArgs: [-g]
    source: >-
      files.filter(f, pathExt(f) in [".yaml", ".yml", ".tpl"])
    envFrom:
      - callerRef:
          pattern: "^HELM_.+"
    ui:
      theme: dracula
    hooks:
      init:
        - command: helm
          args: [version, --short]
      preRender:
        - command: helm
          args: [dependency, build]
          envFrom:
            - callerRef:
                pattern: "^HELM_.+"
      postRender:
        # Pass the rendered manifest via stdin to `kubeconform`.
        - command: kubeconform
          args: [-strict, -summary]
    plugins:
      dry-run:
        command: helm
        args: [install, ., -g, --dry-run]
        envFrom:
          - callerRef:
              pattern: "^HELM_.+"
        description: invoke helm dry-run
        keys:
          - code: ctrl+r
            alias: ⌃r

  ks:
    command: kustomize
    args: [build, .]
    source: >-
      files.filter(f, pathExt(f) in [".yaml", ".yml"])
    env:
      - name: KUSTOMIZE_ENABLE_ALPHA_COMMANDS
        value: "true"
    ui:
      compact: true
      theme: tokyonight-storm
    hooks:
      init:
        - command: kustomize
          args: [version]
```

##### 🧩 CEL Functions

`kat` provides custom CEL functions for file path operations:

* `pathBase(string)`: Returns the filename (e.g., `"Chart.yaml"`)
* `pathExt(string)`: Returns the file extension (e.g., `".yaml"`)
* `pathDir(string)`: Returns the directory path
* `yamlPath(file, path)`: Reads a YAML file and extracts a value using a JSONPath expression

You can combine these with CEL's built-in functions like `exists()`, `filter()`, `in`, `contains()`, `matches()`, and logical operators.

Example:

```
rules:
  - match: >-
      files.exists(f,
        pathBase(f) == "Chart.yaml" &&
        yamlPath(f, "$.apiVersion") == "v2")
    profile: helm

profiles:
  helm:
    command: helm
    args: [template, .]
    extraArgs: [-g]
    source: >-
      files.filter(f,
        pathExt(f) in [".yaml", ".yml", ".tpl"])
```

For more details on CEL expressions and examples, see the [CEL documentation](https://github.com/MacroPower/kat/blob/main/docs/CEL.md).

##### 🔥 DRY Configuration

The `kat` configuration supports YAML [anchor nodes](https://yaml.org/spec/1.2.2/#692-node-anchors), [alias nodes](https://yaml.org/spec/1.2.2/#71-alias-nodes), and [merge keys](https://yaml.org/type/merge.html). You can define common settings once and reuse them across the configuration.

```
profiles:
  ks: &ks
    command: kustomize
    args: [build, .]
    source: >-
      files.filter(f, pathExt(f) in [".yaml", ".yml"])
    hooks:
      postRender:
        - &kubeconform
          command: kubeconform
          args: [-strict, -summary]

  ks-helm:
    <<: *ks
    args: [build, ., --enable-helm]

  helm:
    command: helm
    args: [template, .]
    extraArgs: [-g]
    source: >-
      files.filter(f, pathExt(f) in [".yaml", ".yml", ".tpl"])
    envFrom:
      - callerRef:
          pattern: "^HELM_.+"
    hooks:
      postRender:
        - *kubeconform
```

>  ❤️ Thanks to [goccy/go-yaml](https://github.com/goccy/go-yaml).
> 
>  

##### 📖 Examples

**Default config** - By default, `kat` includes a configuration that supports `helm`, `kustomize`, and generic YAML files. This is a great starting point for writing your own custom config:

* See [`pkg/config/config.yaml`](https://github.com/MacroPower/kat/blob/main/pkg/config/config.yaml) for the default configuration.

**Support for custom tools** - You can add support for other languages/tools like [`kcl`](https://www.kcl-lang.io/), [`jsonnet`](https://jsonnet.org/), [`flux-local`](https://github.com/allenporter/flux-local), [`cue`](https://cuelang.org/), and so on:

```
rules:
  - match: >-
      files.exists(f, pathExt(f) == ".k")
    profile: kcl
profiles:
  kcl:
    command: kcl
    args: [run, .]
    source: >-
      files.filter(f, pathExt(f) == ".k")
    envFrom:
      - callerRef:
          pattern: "^KCL_.+"
```

**Content-based detection** - Match based on file content, not just names:

```
rules:
  - # Match Helm v3 specifically
    match: >-
      files.exists(f,
        pathBase(f) == "Chart.yaml" &&
        yamlPath(f, "$.apiVersion") == "v2")
    profile: helm-v3
  - # Match Kubernetes resources with specific API versions
    match: >-
      files.exists(f,
        pathExt(f) in [".yaml", ".yml"] &&
        yamlPath(f, "$.apiVersion") in ["apps/v1", "v1"])
    profile: yaml
```

**Using Task** - If you use [`task`](https://taskfile.dev), you can use your tasks in the `kat` config:

```
rules:
  - match: >-
      files.exists(f, pathBase(f) in ["Taskfile.yml", "Taskfile.yaml"])
    profile: task
profiles:
  task:
    command: task
    args: [render]
    source: >-
      files.filter(f, pathExt(f) in [".yaml", ".yml"])
    hooks:
      postRender:
        - command: task
          args: [validate]
```

>  Note that you should write your `task` to:
> 
>  * Output the rendered manifest to stdout, and anything else to stderr.
> * Tolerate being called from any directory in the project.
> 	+ E.g., instead of `./folder`, use `{{joinPath .ROOT_DIR "folder"}}`.
> * Not require any additional arguments to run.
> 	+ You can reference `{{.USER_WORKING_DIR}}` to obtain the path that the user invoked `kat` from/with.
> 	+ E.g., `vars: { PATH: "{{.PATH | default .USER_WORKING_DIR}}" }`
> 
>  If you are concerned about safety (i.e. accidentally calling a task defined by someone else), you can consider not including a rule for `task` and only allowing it to be invoked manually via the CLI args, or you could write a more narrow match expression (e.g. `f.contains("/my-org/")`).
> 
>  

#### 🌈 Themes

[![Themes](https://github.com/MacroPower/kat/raw/main/docs/assets/themes.gif)](https://github.com/MacroPower/kat/blob/main/docs/assets/themes.gif)
  [![Themes](https://github.com/MacroPower/kat/raw/main/docs/assets/themes.gif)](https://github.com/MacroPower/kat/blob/main/docs/assets/themes.gif)  

Configure a theme with `--ui-theme`, `KAT_UI_THEME`, or via config:

```
ui:
  theme: "dracula"
```

You can optionally set different themes for different profiles:

```
profiles:
  helm:
    ui:
      theme: "dracula"
      # ...
  ks:
    ui:
      theme: "tokyonight-storm"
      # ...
```

We use [Chroma](https://github.com/alecthomas/chroma/) for theming, so you can use any styles from the [Chroma Style Gallery](https://xyproto.github.io/splash/docs/).

You can also add your own themes in the config:

```
ui:
  theme: "my-custom-theme"
  themes:
    my-custom-theme:
      styles:
        background: "#abb2bf bg:#282c34"
        punctuation: "#abb2bf"
        keyword: "#c678dd"
        name: "bold #e06c75"
        comment: "italic #8b949e"
        commentSpecial: "bold italic #8b949e"
        # ...
```

Chroma uses the same syntax as Pygments. Define `ui.themes.[name].styles` as a map of Pygments [Tokens](https://pygments.org/docs/tokens/) to [Styles](http://pygments.org/docs/styles/). You can then reference any theme in `ui.theme` (or by using the corresponding flag / env var).

#### 🔍️ Similar Tools

These projects provided a lot of inspiration (and snippets) for `kat`:

* [k9s](https://github.com/derailed/k9s) - *A terminal UI to interact with your Kubernetes clusters.*
* [bat](https://github.com/sharkdp/bat) - *A `cat(1)` clone with wings.*
* [task](https://github.com/go-task/task) - *A task runner for Go.*
* [glow](https://github.com/charmbracelet/glow) - *Render markdown on the CLI, with pizzazz!*
* [soft-serve](https://github.com/charmbracelet/soft-serve) - *The mighty, self-hostable Git server for the command line.*
* [wishlist](https://github.com/charmbracelet/wishlist) - *The SSH directory.*
* [viddy](https://github.com/sachaos/viddy) - *A modern `watch` command.*

#### ❤️ Dependencies

`kat` is built on top of a number of libraries. Here are some of its key dependencies:

* [charmbracelet/bubbletea](https://github.com/charmbracelet/bubbletea) - *A powerful TUI framework for Go.*
	+ ...plus many other fantastic libraries from [*charm*](https://github.com/charmbracelet)
* [alecthomas/chroma](https://github.com/alecthomas/chroma) - *A general-purpose syntax highlighter in pure Go.*
* [google/cel-go](https://github.com/google/cel-go) - *A fast, portable, and safe expression evaluation engine.*
* [goccy/go-yaml](https://github.com/goccy/go-yaml) - *YAML support for Go.*
* [fsnotify](https://github.com/fsnotify/fsnotify) - *Cross-platform filesystem notifications.*
* [invopop/jsonschema](https://github.com/invopop/jsonschema) - *JSON Schema generation.*
* [santhosh-tekuri/jsonschema](https://github.com/santhosh-tekuri/jsonschema) - *JSON Schema validation.*
* And [more](https://github.com/MacroPower/kat/blob/main/go.mod).
