---
aliases: []
conformant: true
prodos:
  kind: concept
  lifecycle: stable
created: 2025-02-07T12:57:55+00:00
modified: 2026-09-03T09:34:44.439605+00:00
permalink: llmeon/30-library/100-zettelkasten/knowledge-related-biases
tags:
  - knowledge
  - TheHuman/Cognition/bias
title: Knowledge-Related Biases
type: concept
---
Knowledge-related biases are cognitive distortions where our possession (or lack) of information prevents objective assessment and communication. These fall under the broader umbrella of [[MOC - Cognitive Biases]] [extends:: [[MOC - Cognitive Biases]]].

## Curse of Knowledge

- **Definition:** The inability to imagine not knowing what you already know.
- **Software Context:**
  - Creating overly complex solutions.
  - Writing insufficient documentation.
  - Assuming system knowledge in new team members ("This code is self-documenting").

The Curse of Knowledge directly fuels the "Illusion of Clarity" during communication, where the speaker assumes the listener shares their rich context—a dynamic unpacked in [[SoT - Communication & Misunderstanding (The Experiential Filter)]] [implements:: [[SoT - Communication & Misunderstanding (The Experiential Filter)]]].

## Dunning-Kruger Effect

- **Definition:** Overestimating ability when knowledge is limited.
- **Software Context:**
  - Junior developers taking on overly complex tasks.
  - Teams underestimating system complexity.
  - Oversimplifying architectural decisions ("How hard could building a distributed system be?").

See [[SoT - Dunning-Kruger Effect]] [extends:: [[SoT - Dunning-Kruger Effect]]] for the core model and mechanism.

## Illusion of Explanatory Depth (IoED)

Believing you understand how a complex system works better than you actually do, until you are forced to explain its causal mechanisms. See [[SoT - Illusion of Explanatory Depth (IoED)]] [extends:: [[SoT - Illusion of Explanatory Depth (IoED)]]] for a deep dive.

## Mitigation

The primary countermeasure to these biases is [[SoT - Metacognitive Calibration]] [depends_on:: [[SoT - Metacognitive Calibration]]], which forces the individual to actively test their confidence against reality.
