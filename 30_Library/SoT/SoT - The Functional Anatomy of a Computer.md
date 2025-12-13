## 5. Bridging Man and Machine (Peripherals)

A computer that calculates but cannot communicate is theoretically valid but practically useless.

-   **Input (Command):** Keyboard/Mouse/Touchscreen.
-   **Output (Result):** Monitor/Speaker/Haptics.
-   **The Loop:** User Input -> OS -> CPU -> RAM -> Output.

### The Input Translation Layer (Keyboard Architecture)
When a user presses a key, the computer does not receive a letter (e.g., "A"). It receives a coordinate. The translation from **Physical Action** to **Digital Symbol** happens in distinct layers:

1.  **Hardware (Scancode):** The keyboard firmware generates a `Scancode` based on the key's physical location on the matrix (e.g., Row 2, Column 3). It knows *where* you pressed, not *what* you pressed.
2.  **Driver/OS (Keycode):** The OS receives the Scancode and maps it to a standardized `Keycode` (e.g., "Key 0x04"). This is still abstract.
3.  **Layout Software (Symbol):** The OS applies a "Locale/Layout" (e.g., QWERTY, Dvorak) to map the `Keycode` to a final `Symbol` or `Action`.
    -   *Implication:* Remapping can happen at the **Firmware Level** (sending a different Scancode, e.g., via QMK on an Atreus) or at the **OS Level** (interpreting the Keycode differently).

---