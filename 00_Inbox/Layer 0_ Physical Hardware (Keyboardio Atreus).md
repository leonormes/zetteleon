---
aliases: []
confidence: 
created: 2025-05-06T15:41:20Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T11:06:55Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [devex]
title: Layer 0_ Physical Hardware (Keyboardio Atreus)
type: permanent
uid: 
updated: 
version:
---

[[2025-05-06]]

I learnt that when you press a key on the keyboard a scancode is generated which is sent to the host computer which maps that scan code to a key code. The key you press doesn't produce the code for a specific symbol. The code refers to the key's physical location on the keyboard. It is the layout software that maps to the symbols! I guess this facilities remapping in software.

[[Blub Studies]]

## Scancode Generation

When you press a key, the keyboard's hardware (or firmware in the case of customisable keyboards like the Atreus) generates a unique number called a "scancode".

## Scancode Transmission

This scancode is then sent to the host computer.

### Physical Location, Not Symbol

Crucially, this scancode does not directly represent a character like 'A' or a symbol like '!'. Instead, the scancode typically signifies the physical position of the key that was pressed on the keyboard matrix (e.g., row 2, column 3).

## Host Interpretation (Scancode to Keycode)

The computer's operating system (OS) or its keyboard driver receives the scancode. The OS then often translates this device-dependent scancode into a more standardised, device-independent value known as a "keycode" or "virtual key code". This keycode is a more abstract representation of the key (e.g., "the key typically used for the letter A").

## Layout Software and Symbol Mapping

This is where the keyboard layout settings (e.g., UK English, US English, Dvorak, or custom layouts you might configure for your Atreus) come into play. The OS, using its keyboard layout software, maps the keycode (which originated from the positional scancode) to a specific character, symbol, or function. For example, the same scancode/keycode will produce 'Q' on a QWERTY layout but an 'A' on an AZERTY layout. Modifier keys like Shift, Ctrl, or Alt are also taken into account at this stage to determine the final symbol or action.

## Firmware Remapping (like on an Atreus with QMK/TMK)

Keyboards like the Atreus often allow you to change what scancode (or internal key event) is sent by a physical key press directly in the keyboard's firmware. This is a powerful way to remap keys before the information even reaches the OS.

## OS-Level Remapping

Even without firmware customisation, the operating system's keyboard layout settings allow you to change how keycodes are interpreted and mapped to symbols.
