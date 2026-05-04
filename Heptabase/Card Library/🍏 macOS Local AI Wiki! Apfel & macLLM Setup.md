## 🍏 macOS Local AI Wiki: Apfel & macLLM Setup

### 1\. Prerequisites

Before starting, ensure your hardware and software meet the requirements for Apple Intelligence:

- Hardware: Mac with Apple Silicon (M1 chip or later).

- Operating System: macOS 26 (Tahoe) or later.

- Storage: At least 7 GB of free space for model downloads.

- Language: Siri and Device language must be set to a supported language (e.g., English UK/US).

### 2\. Enabling Apple Intelligence

The on-device models are only accessible once Apple Intelligence is active.

1. Open System Settings.

2. Navigate to Apple Intelligence & Siri.

3. Click Turn on Apple Intelligence.

4. Wait for the model assets to finish downloading (ensure you are connected to Wi-Fi and power).

---

### 3\. Installing Apfel (The System Model Bridge)

apfel allows you to use the built-in 3B system model from the terminal or as a server for other apps like Obsidian.

#### Installation

Open your Terminal and run the following Homebrew commands:

Bash

```
# Add the repository
brew tap Arthur-Ficial/tap

# Install the apfel tool
brew install apfel
```

#### Essential Commands

- Test Prompt: `apfel "What is the capital of England?"`

- Interactive Chat: `apfel --chat`

- Start API Server: `apfel --serve` (Runs a local server at `http://localhost:11434/v1`).

---

### 4\. Installing macLLM (The Agentic AI Tool)

macLLM is a desktop tool that can search your Obsidian vault, summarize the clipboard, and run multi-step tasks.

#### Installation

macLLM uses the uv package manager for speed and dependency management.

1. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

2. Clone & Run macLLM:

    Bash

```
git clone https://github.com/appenz/macLLM.git
cd macLLM
uv run -m macllm
```

#### Configuration

1. Hotkey: Press `⌥ Space` (Option + Space) to toggle the macLLM window.

2. Environment Variables: Create a `.env` file in the macLLM folder to add your API keys (e.g., `GEMINI_API_KEY` or `OPENAI_API_KEY`) if you want to use external models alongside the local ones.