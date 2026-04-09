---
title: "You said Persona: You are an expert research analy..."
source: "https://gemini.google.com/app/89dc5cbb2fd56c94"
captured: "2026-04-09T13:33:13+01:00 2026-04-09T13:33:13+01:00"
status: "processing"
tags:
  - "input"
type: "head"
---


### Analysis of "Attention Residuals" Research by the Kimi Team

**Core Thesis** The foundational argument of the research is that standard residual connections—the "shortcuts" used in modern neural networks to prevent signal loss—are architecturally flawed for extremely deep models. By replacing these additive connections with a depth-wise attention mechanism (Attention Residuals), a model can selectively retrieve information from any previous layer. This prevents signal dilution, stabilises gradients, and allows for significantly deeper architectures that exhibit superior multi-step reasoning.

**Filtered Substance: Technical Deconstruction** The content identifies three primary technical shifts from current Transformer architectures:

1. **From Additive to Selective Integration:** Current models use , where is the original signal and is the layer's output. This creates a cumulative "pile" of data where early information is buried. The proposed architecture uses Query-Key-Value (QKV) vectors across the depth dimension. Each layer "queries" previous layers to extract only the relevant features required for its specific computation.
2. **Addressing Signal Dilution:** In standard deep networks, the magnitude of the signal grows as it passes through layers, requiring later layers to produce "louder" (higher magnitude) outputs to influence the final result. Attention residuals keep the signal bounded and stable, ensuring that the learning signal (gradient) is distributed more evenly during training.
3. **Infrastructure Optimisation (Block Attention):** To maintain compatibility with "pipeline parallelism" (splitting a model across multiple GPUs/servers), the researchers introduced "Block Attention Residuals." This allows layers within a specific hardware node to use full attention residuals, while maintaining traditional linear communication between different nodes to avoid excessive inter-server data traffic.

**Grounding in Reality** While the video frames this as a "cure for AI amnesia," the concept is an architectural refinement of established principles.

- **Residual Connections:** Introduced by He et al. (ResNet, 2015), these are the industry standard. The Kimi team is essentially evolving the "identity shortcut" into a "learned shortcut."
- **Novelty vs. Iteration:** The idea of "attention over depth" or "dense connections" is not entirely new; DenseNets (2017) previously explored connecting every layer to every other layer via concatenation. The novelty here lies in applying Transformer-style QKV attention specifically to the residual path in Large Language Models (LLMs) and solving the associated scaling/infrastructure bottlenecks for distributed training.
- **Performance Claims:** The 1.25x compute efficiency and the 7.5-point jump in GPQA (graduate-level reasoning) are significant but represent incremental optimisation rather than a fundamental shift in how AI "thinks." The comparison to the human brain is speculative rhetoric; the system remains a mathematical optimisation of signal propagation.

**The Verdict**

- **Signal-to-Noise Ratio:** 35% Signal / 65% Noise
- **Assessment:** The informational density is moderate. The core technical contribution—replacing additive residuals with attention-based selection—is a rigorous and valuable architectural advancement. However, the presentation is heavily padded with lengthy analogies (chefs, soup, buffets), historical recaps of basic AI concepts, a three-minute commercial for an unrelated video tool, and anthropomorphic comparisons to human neuroplasticity. The practical value for researchers and engineers is high, as it provides a viable path toward training deeper, more stable models with better reasoning capabilities.
