# How to write a great agents.md: Lessons from over 2,500 repositories

![rw-book-cover](https://github.blog/wp-content/uploads/2025/05/github-generic-wallpaper-rubber-duck-invertocat.png?fit=1920%2C1080)

## Metadata
- Author: [[Matt Nigh]]
- Full Title: How to write a great agents.md: Lessons from over 2,500 repositories
- Category: #articles
- Summary: GitHub's agents.md lets you create specialized AI agents (docs, tests, linting, etc.) by defining a persona, commands, and rules. Analysis of 2,500+ files shows the best agents are specific: include exact commands, tech stack, code examples, and clear boundaries. Start small, cover six core areas (commands, tests, structure, style, git, boundaries), and iterate.
- URL: https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/

## Full Document
![](https://github.blog/wp-content/uploads/2025/05/github-generic-wallpaper-rubber-duck-invertocat.png?w=1600)
We recently released a new [GitHub Copilot](https://github.com/features/copilot) feature: custom agents defined in `agents.md` files. Instead of one general assistant, you can now build a team of specialists: a `@docs-agent` for technical writing, a `@test-agent` for quality assurance, and a `@security-agent` for security analysis. Each `agents.md` file acts as an agent persona, which you define with frontmatter and custom instructions.

`agents.md` is where you define all the specifics: the agent’s persona, the exact tech stack it should know, the project’s file structure, workflows, and the explicit commands it can run. It’s also where you provide code style examples and, most importantly, set clear boundaries of what not to do.

**The challenge?** Most agent files fail because they’re too vague. “You are a helpful coding assistant” doesn’t work. “You are a test engineer who writes tests for React components, follows these examples, and never modifies source code” does.

I analyzed over 2,500 `agents.md` files across public repos to understand how developers were using `agents.md` files. The analysis showed a clear pattern of what works: provide your agent a specific job or persona, exact commands to run, well-defined boundaries to follow, and clear examples of good output for the agent to follow.

Here’s what the successful ones do differently.

#### What works in practice: Lessons from 2,500+ repos

My analysis of over 2,500 `agents.md` files revealed a clear divide between the ones that fail and the ones that work. The successful agents aren’t just vague helpers; they are specialists. Here’s what the best-performing files do differently:

* **Put commands early:** Put relevant executable commands in an early section: `npm test`, `npm run build`, `pytest -v`. Include flags and options, not just tool names. Your agent will reference these often.
* **Code examples over explanations:** One real code snippet showing your style beats three paragraphs describing it. Show what good output looks like.
* **Set clear boundaries:** Tell AI what it should never touch (e.g., secrets, vendor directories, production configs, or specific folders). “Never commit secrets” was the most common helpful constraint.
* **Be specific about your stack:** Say “React 18 with TypeScript, Vite, and Tailwind CSS” not “React project.” Include versions and key dependencies.
* **Cover six core areas:** Hitting these areas puts you in the top tier: commands, testing, project structure, code style, git workflow, and boundaries.

#### Example of a great agent.md file

Below is an example for adding a documentation `agent.md` persona in your repo to `.github/agents/[docs-agent.md](http://docs-agent.md)`:

```
---
name: docs_agent
description: Expert technical writer for this project
---

You are an expert technical writer for this project.

## Your role
- You are fluent in Markdown and can read TypeScript code
- You write for a developer audience, focusing on clarity and practical examples
- Your task: read code from `src/` and generate or update documentation in `docs/`

## Project knowledge
- **Tech Stack:** React 18, TypeScript, Vite, Tailwind CSS
- **File Structure:**
  - `src/` – Application source code (you READ from here)
  - `docs/` – All documentation (you WRITE to here)
  - `tests/` – Unit, Integration, and Playwright tests

## Commands you can use
Build docs: `npm run docs:build` (checks for broken links)
Lint markdown: `npx markdownlint docs/` (validates your work)

## Documentation practices
Be concise, specific, and value dense
Write so that a new developer to this codebase can understand your writing, don’t assume your audience are experts in the topic/area you are writing about.

## Boundaries
- ✅ **Always do:** Write new files to `docs/`, follow the style examples, run markdownlint
- ⚠️ **Ask first:** Before modifying existing documents in a major way
- 🚫 **Never do:** Modify code in `src/`, edit config files, commit secrets
```

* **States a clear role:** Defines who the agent is (expert technical writer), what skills it has (Markdown, TypeScript), and what it does (read code, write docs).
* **Executable commands:** Gives AI tools it can run (`npm run docs:build` and `npx markdownlint docs/`). Commands come first.
* **Project knowledge:** Specifies tech stack with versions (React 18, TypeScript, Vite, Tailwind CSS) and exact file locations.
* **Real examples:** Shows what good output looks like with actual code. No abstract descriptions.
* **Three-tier boundaries:** Set clear rules using always do, ask first, never do. Prevents destructive mistakes.

Pick one simple task. Don’t build a “general helper.” Pick something specific like:

Start minimal—you only need three things:

* **Agent name**: `test-agent`, `docs-agent`, `lint-agent`
* **Description**: “Writes unit tests for TypeScript functions”
* **Persona**: “You are a quality software engineer who writes comprehensive tests”

Copilot can also help generate one for you. Using your preferred IDE, open a new file at `.github/agents/test-agent.md` and use this prompt:

```
Create a test agent for this repository. It should:
- Have the persona of a QA software engineer.
- Write tests for this codebase
- Run tests and analyzes results
- Write to “/tests/” directory only
- Never modify source code or remove failing tests
- Include specific examples of good test structure
```

Copilot will generate a complete `agent.md` file with persona, commands, and boundaries based on your codebase. Review it, add in YAML frontmatter, adjust the commands for your project, and you’re ready to use `@test-agent`.

Consider asking Copilot to help generate `agent.md` files for the below agents. I’ve included examples with each of the agents, which should be changed to match the reality of your project.

One of your early agents should write documentation. It reads your code and generates API docs, function references, and tutorials. Give it commands like `npm run docs:build` and `markdownlint docs/` so it can validate its own work. Tell it to write to `docs/` and never touch `src/`.

* What it does: Turns code comments and function signatures into Markdown documentation
* Example commands: `npm run docs:build`, `markdownlint docs/`
* Example boundaries: Write to `docs/`, never modify source code

This one writes tests. Point it at your test framework (Jest, PyTest, Playwright) and give it the command to run tests. The boundary here is critical: it can write to `tests` but should never remove a test because it is failing and cannot be fixed by the agent.

* What it does: Writes unit tests, integration tests, and edge case coverage
* Example commands: `npm test`, `pytest -v`, `cargo test --coverage`
* Example boundaries: Write to `tests/`, never remove failing tests unless authorized by user

A fairly safe agent to create early on. It fixes code style and formatting but shouldn’t change logic. Give it commands that let it auto-fix style issues. This one’s low-risk because linters are designed to be safe.

* What it does: Formats code, fixes import order, enforces naming conventions
* Example commands: `npm run lint --fix`, `prettier --write`
* Example boundaries: Only fix style, never change code logic

This agent builds API endpoints. It needs to know your framework (Express, FastAPI, Rails) and where routes live. Give it commands to start the dev server and test endpoints. The key boundary: it can modify API routes but must ask before touching database schemas.

* What it does: Creates REST endpoints, GraphQL resolvers, error handlers
* Example commands: `npm run dev`, `curl localhost:3000/api`, `pytest tests/api/`
* Example boundaries: Modify routes, ask before schema changes

Handles builds and deployments to your local dev environment. Keep it locked down: only deploy to dev environments and require explicit approval. Give it build commands and deployment tools but make the boundaries very clear.

* What it does: Runs local or dev builds, creates Docker images
* Example commands: `npm run test`
* Example boundaries: Only deploy to dev, require user approval for anything with risk

```
---
name: your-agent-name
description: [One-sentence description of what this agent does]
---

You are an expert [technical writer/test engineer/security analyst] for this project.

## Persona
- You specialize in [writing documentation/creating tests/analyzing logs/building APIs]
- You understand [the codebase/test patterns/security risks] and translate that into [clear docs/comprehensive tests/actionable insights]
- Your output: [API documentation/unit tests/security reports] that [developers can understand/catch bugs early/prevent incidents]

## Project knowledge
- **Tech Stack:** [your technologies with versions]
- **File Structure:**
  - `src/` – [what's here]
  - `tests/` – [what's here]

## Tools you can use
- **Build:** `npm run build` (compiles TypeScript, outputs to dist/)
- **Test:** `npm test` (runs Jest, must pass before commits)
- **Lint:** `npm run lint --fix` (auto-fixes ESLint errors)

## Standards

Follow these rules for all code you write:

**Naming conventions:**
- Functions: camelCase (`getUserData`, `calculateTotal`)
- Classes: PascalCase (`UserService`, `DataController`)
- Constants: UPPER_SNAKE_CASE (`API_KEY`, `MAX_RETRIES`)

**Code style example:**
```typescript
// ✅ Good - descriptive names, proper error handling
async function fetchUserById(id: string): Promise<User> {
  if (!id) throw new Error('User ID required');
  
  const response = await api.get(`/users/${id}`);
  return response.data;
}

// ❌ Bad - vague names, no error handling
async function get(x) {
  return await api.get('/users/' + x).data;
}
Boundaries
- ✅ **Always:** Write to `src/` and `tests/`, run tests before commits, follow naming conventions
- ⚠️ **Ask first:** Database schema changes, adding dependencies, modifying CI/CD config
- 🚫 **Never:** Commit secrets or API keys, edit `node_modules/` or `vendor/`
```

Building an effective custom agent isn’t about writing a vague prompt; it’s about providing a specific persona and clear instructions.

My analysis of over 2,500 [`agents.md`](http://agents.md) files shows that the best agents are given a clear persona and, most importantly, a detailed operating manual. This manual must include executable commands, concrete code examples for styling, explicit boundaries (like files to never touch), and specifics about your tech stack.

When creating your own [`agents.md`](http://agents.md) cover the six core areas: Commands, testing, project structure, code style, git workflow, and boundaries. Start simple. Test it. Add detail when your agent makes mistakes. The best agent files grow through iteration, not upfront planning.

Now go forth and build your own custom agents to see how they level up your workflow first-hand!
