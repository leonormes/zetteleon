# GitHub - lirantal/repolyze: Analyze a git source code repository for health signals and project vitals · GitHub

![rw-book-cover](https://repository-images.githubusercontent.com/1212187905/f5c72666-8adc-42c2-b75a-db2e0eb281c9)

## Metadata
- Author: [[https://github.com/lirantal/]]
- Full Title: GitHub - lirantal/repolyze: Analyze a git source code repository for health signals and project vitals · GitHub
- Category: #articles
- Summary: Repolyze is a tool that analyzes git repositories for health and project status. It runs with Node.js and git, and can be used via command line or npx. The project is open source and maintained by Liran Tal under the Apache-2.0 License.
- URL: https://github.com/lirantal/repolyze

## Full Document
### lirantal/repolyze

main

Go to file

Code

Open more actions menu

###  repolyze

Analyze a git source code repository for health signals and project vitals

[![npm version](https://camo.githubusercontent.com/1bb31a4d2241201abb290f2dbff2d78763dd9d237c262fa5b65b5ef0a771d750/68747470733a2f2f62616467656e2e6e65742f6e706d2f762f7265706f6c797a65)](https://www.npmjs.com/package/repolyze)
[![license](https://camo.githubusercontent.com/436a8c234be550a13272fc9570a5949e7e6c4bff674369b5f7dc84731483e18f/68747470733a2f2f62616467656e2e6e65742f6e706d2f6c6963656e73652f7265706f6c797a65)](https://www.npmjs.com/package/repolyze)
[![downloads](https://camo.githubusercontent.com/1a530e492965456f47da8d582a298eaa2966efef27ad1570dc060d0d345b6ca3/68747470733a2f2f62616467656e2e6e65742f6e706d2f64742f7265706f6c797a65)](https://www.npmjs.com/package/repolyze)
[![build](https://github.com/lirantal/repolyze/workflows/CI/badge.svg)](https://github.com/lirantal/repolyze/actions?workflow=CI)
[![codecov](https://camo.githubusercontent.com/104c0ff63d554ecf18d463a9c214342b523821b84c466bc72fa02b165be52d8f/68747470733a2f2f62616467656e2e6e65742f636f6465636f762f632f6769746875622f6c6972616e74616c2f7265706f6c797a65)](https://app.codecov.io/gh/lirantal/repolyze)
[![Responsible Disclosure Policy](https://camo.githubusercontent.com/217b90adaa9648578e80cd3568a08b984a3ec76295d6dcbac1f13108faf4a3f0/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f53656375726974792d526573706f6e7369626c65253230446973636c6f737572652d79656c6c6f772e737667)](https://github.com/lirantal/repolyze/blob/main/SECURITY.md)
[![repolyze screenshot](https://github.com/lirantal/repolyze/raw/main/.github/repolyze-screenshot.png)](https://github.com/lirantal/repolyze/blob/main/.github/repolyze-screenshot.png)
#### Usage

Analyze the current directory as a git repository and print JSON (for tooling or AI agents):

```
npx repolyze --json .
```

Analyze another path:

```
npx repolyze --json /path/to/repo
```

Verbose mode (prints `git` invocations to stderr):

```
npx repolyze --verbose .
```

Help:

```
npx repolyze --help
```

When the package is installed globally, use the `repolyze` command the same way (for example `repolyze --json .`).

#### Screenshots

[![Bugs and security hotspots screenshot](https://github.com/lirantal/repolyze/raw/main/.github/repolyze-bugs-and-security-hotspots.png)](https://github.com/lirantal/repolyze/blob/main/.github/repolyze-bugs-and-security-hotspots.png)
[![Contributors screenshot](https://github.com/lirantal/repolyze/raw/main/.github/repolyze-contributors.png)](https://github.com/lirantal/repolyze/blob/main/.github/repolyze-contributors.png)
#### Requirements

* [Node.js](https://nodejs.org/) v24 or newer
* [`git`](https://git-scm.com/) available on your `PATH`

#### Install

Install globally (pick your package manager):

```
npm install -g repolyze
pnpm add -g repolyze
```

Or run **without** installing, using `npx` (downloads the package for that invocation):

```
npx repolyze --help
```

#### Credits & References

The default signals this tool collects mirror the git workflow described by **Maciej Piechowski** in *[The Git Commands I Run Before Reading Any Code](https://piechowski.io/post/git-commands-before-reading-code/)*. See [docs/repository-analysis.md](https://github.com/lirantal/repolyze/blob/main/docs/repository-analysis.md) for command-by-command notes, caveats, and the same attribution in context.

References:

* [fallow-rs](https://github.com/fallow-rs/fallow) - Static analysis for source code health based on git

#### Contributing

Please consult [CONTRIBUTING](https://github.com/lirantal/repolyze/blob/main/.github/CONTRIBUTING.md) for guidelines on contributing to this project.

**Developing this repo locally** (running from source, tests, build): see [DEVELOPMENT.md](https://github.com/lirantal/repolyze/blob/main/DEVELOPMENT.md).

#### Author

**repolyze** © [Liran Tal](https://github.com/lirantal), Released under the [Apache-2.0](https://github.com/lirantal/repolyze/blob/main/LICENSE) License.
